from __future__ import annotations

from collections.abc import Iterable, Mapping
from datetime import date

import numpy as np
import pandas as pd

CARVEOUT_DOMAINS = {"child_safety", "infrastructure", "government_use"}
REVIEWED_STATUSES = {"verified", "revised"}


def _text_series(frame: pd.DataFrame, column: str) -> pd.Series:
    if column not in frame.columns:
        return pd.Series("", index=frame.index, dtype="string")
    return frame[column].fillna("").astype(str).str.strip()


def _boolean_series(frame: pd.DataFrame, column: str) -> pd.Series:
    raw = _text_series(frame, column).str.lower()
    if raw.eq("").all():
        return pd.Series(False, index=frame.index, dtype=bool)
    mapped = raw.map({"true": True, "false": False, "1": True, "0": False, "": False})
    invalid = mapped.isna()
    if invalid.any():
        values = sorted(raw.loc[invalid].unique())
        raise ValueError(f"{column} contains invalid boolean values: {values}")
    return mapped.astype(bool)


def _iso_dates(raw: pd.Series, label: str) -> pd.Series:
    present = raw.ne("")
    parsed = pd.to_datetime(raw.where(present), format="%Y-%m-%d", errors="coerce")
    invalid = present & parsed.isna()
    if invalid.any():
        values = sorted(raw.loc[invalid].unique())
        raise ValueError(f"{label} must use ISO YYYY-MM-DD dates: {values}")
    return parsed


def _filter_snapshot(
    data: pd.DataFrame,
    analysis_date: str | date | None,
) -> pd.DataFrame:
    if analysis_date is None:
        return data

    try:
        snapshot = pd.Timestamp(analysis_date).normalize()
    except (TypeError, ValueError) as exc:
        raise ValueError("analysis_date must be a valid date") from exc

    row_start = _text_series(data, "effective_date")
    law_start = _text_series(data, "law_effective_date")
    start_raw = row_start.mask(row_start.eq(""), law_start)

    mixed_dates = _boolean_series(data, "mixed_effective_dates")
    positive = data["covered"].astype(bool)
    missing_mixed = positive & mixed_dates & row_start.eq("")
    if missing_mixed.any():
        laws = sorted(_text_series(data.loc[missing_mixed], "law_id").unique())
        raise ValueError(
            "Mixed-effective-date laws require an obligation-level effective_date before analysis: "
            f"{laws}"
        )

    missing_start = positive & start_raw.eq("")
    if missing_start.any():
        laws = sorted(_text_series(data.loc[missing_start], "law_id").unique())
        raise ValueError(f"Positive obligations are missing an operative start date: {laws}")

    start_dates = _iso_dates(start_raw, "effective_date")

    row_end = _text_series(data, "inactive_from_date")
    law_end = _text_series(data, "law_inactive_from_date")
    end_raw = row_end.mask(row_end.eq(""), law_end)
    end_dates = _iso_dates(end_raw, "inactive_from_date")

    active = start_dates.le(snapshot) & (end_dates.isna() | snapshot.lt(end_dates))
    return data.loc[~positive | active].copy()


def prepare_state_domain(
    codings: pd.DataFrame,
    states: pd.DataFrame,
    include_unreviewed: bool = False,
    domains: Iterable[str] | None = None,
    analysis_date: str | date | None = None,
) -> pd.DataFrame:
    required = {"state", "domain", "covered", "strength", "review_status"}
    missing = required.difference(codings.columns)
    if missing:
        raise ValueError(f"Coding data missing columns: {sorted(missing)}")
    if not {"state", "weight"}.issubset(states.columns):
        raise ValueError("State universe requires state and weight columns")

    data = codings.copy()
    if not include_unreviewed:
        data = data[data["review_status"].isin(REVIEWED_STATUSES)]
    data["strength"] = pd.to_numeric(data["strength"], errors="raise")
    data["covered"] = (
        data["covered"]
        .astype(str)
        .str.lower()
        .map({"true": True, "false": False, "1": True, "0": False})
        .fillna(data["covered"].astype(bool))
    )
    data = _filter_snapshot(data, analysis_date)

    domain_values = sorted(set(domains or codings["domain"].dropna().unique()))
    if not domain_values:
        raise ValueError("No obligation domains found")

    unknown = set(data["domain"].dropna().unique()).difference(domain_values)
    if unknown:
        raise ValueError(f"Coding data contains domains outside the fixed universe: {sorted(unknown)}")

    grid = pd.MultiIndex.from_product(
        [states["state"].unique(), domain_values], names=["state", "domain"]
    ).to_frame(index=False)
    collapsed = (
        data[data["covered"]]
        .groupby(["state", "domain"], as_index=False)["strength"]
        .max()
    )
    grid = grid.merge(collapsed, on=["state", "domain"], how="left")
    grid["strength"] = grid["strength"].fillna(0).astype(int)
    grid = grid.merge(states[["state", "weight"]], on="state", how="left", validate="many_to_one")
    if grid["weight"].isna().any() or (grid["weight"] < 0).any():
        raise ValueError("Every state needs a nonnegative weight")
    return grid


def _validated_floor_map(floor_strengths: Mapping[str, int]) -> dict[str, int]:
    output: dict[str, int] = {}
    for domain, strength in floor_strengths.items():
        value = int(strength)
        if value not in {0, 1, 2, 3}:
            raise ValueError(f"Federal floor for {domain!r} must be 0, 1, 2, or 3")
        output[str(domain)] = value
    return output


def apply_scenario(
    state_domain: pd.DataFrame,
    scenario: str,
    floor_strength: int = 1,
    ceiling_domains: Iterable[str] | None = None,
    floor_strengths: Mapping[str, int] | None = None,
) -> pd.DataFrame:
    frame = state_domain.copy()
    all_domains = set(frame["domain"].unique())
    selected = set(ceiling_domains or all_domains)
    unknown_selected = selected.difference(all_domains)
    if unknown_selected:
        raise ValueError(f"Scenario selects unknown domains: {sorted(unknown_selected)}")

    if scenario == "current":
        pass
    elif scenario == "broad_ceiling":
        frame.loc[frame["domain"].isin(selected), "strength"] = 0
    elif scenario == "eo14365_carveouts":
        displaced = frame["domain"].isin(selected.difference(CARVEOUT_DOMAINS))
        frame.loc[displaced, "strength"] = 0
    elif scenario == "federal_floor":
        if floor_strengths is not None:
            floor_map = _validated_floor_map(floor_strengths)
            unknown_floor = set(floor_map).difference(all_domains)
            if unknown_floor:
                raise ValueError(f"Federal floor contains unknown domains: {sorted(unknown_floor)}")
            targets = frame["domain"].map(floor_map).fillna(0).astype(int)
            frame["strength"] = np.maximum(frame["strength"], targets)
        else:
            if floor_strength not in {1, 2, 3}:
                raise ValueError("floor_strength must be 1, 2, or 3")
            covered = frame["domain"].isin(selected)
            frame.loc[covered, "strength"] = np.maximum(
                frame.loc[covered, "strength"], floor_strength
            )
    else:
        raise ValueError(f"Unknown scenario: {scenario}")
    frame["scenario"] = scenario
    return frame


def summarize_scenario(frame: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, float | str]] = []
    for (scenario, domain), group in frame.groupby(["scenario", "domain"]):
        weights = group["weight"].to_numpy(dtype=float)
        strengths = group["strength"].to_numpy(dtype=float)
        denominator = weights.sum()
        if denominator <= 0:
            raise ValueError("Scenario weights must sum to a positive value")
        mean_strength = float(np.average(strengths, weights=weights))
        variance = float(np.average((strengths - mean_strength) ** 2, weights=weights))
        coverage = float(np.average(strengths >= 1, weights=weights))
        rows.append(
            {
                "scenario": scenario,
                "domain": domain,
                "coverage": coverage,
                "mean_strength": mean_strength,
                "strength_variance": variance,
                "binary_heterogeneity": 2 * coverage * (1 - coverage),
                "states_covered": int((strengths >= 1).sum()),
            }
        )
    return pd.DataFrame(rows)


def simulate_all(
    state_domain: pd.DataFrame,
    floor_strength: int = 1,
    ceiling_domains: Iterable[str] | None = None,
    floor_strengths: Mapping[str, int] | None = None,
) -> pd.DataFrame:
    scenarios = ["current", "broad_ceiling", "eo14365_carveouts", "federal_floor"]
    outputs = [
        summarize_scenario(
            apply_scenario(
                state_domain,
                scenario,
                floor_strength=floor_strength,
                ceiling_domains=ceiling_domains,
                floor_strengths=floor_strengths,
            )
        )
        for scenario in scenarios
    ]
    return pd.concat(outputs, ignore_index=True)


def scenario_effects(estimates: pd.DataFrame) -> pd.DataFrame:
    current = estimates[estimates["scenario"] == "current"].set_index("domain")
    rows = []
    measures = ["coverage", "mean_strength", "strength_variance", "binary_heterogeneity"]
    for scenario in sorted(set(estimates["scenario"]) - {"current"}):
        comparison = estimates[estimates["scenario"] == scenario].set_index("domain")
        joined = current[measures].join(
            comparison[measures],
            lsuffix="_current",
            rsuffix="_scenario",
        )
        joined["coverage_change"] = joined["coverage_scenario"] - joined["coverage_current"]
        joined["strength_change"] = (
            joined["mean_strength_scenario"] - joined["mean_strength_current"]
        )
        joined["heterogeneity_change"] = (
            joined["strength_variance_scenario"] - joined["strength_variance_current"]
        )
        joined["binary_heterogeneity_change"] = (
            joined["binary_heterogeneity_scenario"]
            - joined["binary_heterogeneity_current"]
        )
        joined["scenario"] = scenario
        rows.append(joined.reset_index())
    return pd.concat(rows, ignore_index=True)
