from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from .coding import SYSTEM_PROMPT, ClaudeLawCoder, build_prompt, flatten_result
from .costs import estimate_cost
from .metrics import prepare_state_domain, scenario_effects, simulate_all
from .retrieval import render_passages, retrieve_passages
from .reviews import apply_reviews
from .schema import LawRecord
from .settings import (
    CODING_MAX_OUTPUT_TOKENS,
    PROJECT_ROOT,
    load_domain_roles,
    load_domains,
    max_spend,
    model_name,
)
from .source_fetch import fetch_source
from .sources import read_manifest, resolve_text_path, validate_sources

OPTIONAL_LAW_FIELDS = {
    "enactment_date",
    "effective_date",
    "amends_law_id",
    "inactive_from_date",
    "superseded_by_law_id",
}


def _law_from_row(row: dict[str, str]) -> LawRecord:
    cleaned = {
        key: (None if key in OPTIONAL_LAW_FIELDS and not value else value)
        for key, value in row.items()
    }
    return LawRecord.model_validate(cleaned)


def command_validate_sources(args: argparse.Namespace) -> int:
    manifest = read_manifest(args.manifest)
    report = validate_sources(manifest)
    print(report.to_string(index=False))
    missing = int((~report["text_exists"]).sum())
    print(f"\n{len(report)} manifest records; {missing} source texts missing")
    return 1 if missing else 0


def command_fetch_sources(args: argparse.Namespace) -> int:
    manifest = read_manifest(args.manifest)
    rows = manifest.head(args.limit) if args.limit else manifest
    receipt_dir = Path(args.receipt_dir)
    failures: list[str] = []
    for row in rows.to_dict(orient="records"):
        output = resolve_text_path(row["local_text_path"])
        receipt = receipt_dir / f"{row['law_id']}.json"
        try:
            result = fetch_source(
                law_id=row["law_id"],
                url=row["primary_source_url"],
                source_format=row["source_format"],
                output_path=output,
                receipt_path=receipt,
                minimum_characters=args.minimum_characters,
            )
            print(
                f"{result.law_id}: {result.text_characters:,} characters; "
                f"sha256 {result.text_sha256[:12]}"
            )
        except Exception as exc:  # noqa: BLE001 - report every failed source in bulk collection
            failures.append(row["law_id"])
            print(f"ERROR {row['law_id']}: {exc}")
    print(f"\nFetched {len(rows) - len(failures)} of {len(rows)} sources")
    return 1 if failures else 0


def _coding_inputs(
    manifest: pd.DataFrame, limit: int | None = None
) -> list[tuple[LawRecord, str, str]]:
    rows = manifest.head(limit) if limit else manifest
    inputs: list[tuple[LawRecord, str, str]] = []
    domains = load_domains()
    for raw in rows.to_dict(orient="records"):
        law = _law_from_row(raw)
        path = resolve_text_path(law.local_text_path)
        if not path.exists():
            continue
        source_text = path.read_text(encoding="utf-8")
        passages = render_passages(retrieve_passages(source_text, domains))
        if passages:
            inputs.append((law, source_text, SYSTEM_PROMPT + build_prompt(law, passages)))
    return inputs


def command_estimate_cost(args: argparse.Namespace) -> int:
    manifest = read_manifest(args.manifest)
    inputs = _coding_inputs(manifest, args.limit)
    if not inputs:
        print("No local statute text is ready. Add text files at the manifest paths first.")
        return 1
    estimate = estimate_cost(
        [item[2] for item in inputs],
        args.model,
        output_tokens_each=args.output_tokens,
        batch=args.batch,
    )
    print(json.dumps(estimate.__dict__, indent=2))
    return 0


def command_code_laws(args: argparse.Namespace) -> int:
    manifest = read_manifest(args.manifest)
    inputs = _coding_inputs(manifest, args.limit)
    if not inputs:
        print("No local statute text is ready. Add text files at the manifest paths first.")
        return 1
    preflight = estimate_cost(
        [item[2] for item in inputs],
        args.model,
        output_tokens_each=CODING_MAX_OUTPUT_TOKENS,
    )
    if preflight.usd > args.max_spend:
        raise RuntimeError(
            f"Estimated cost ${preflight.usd:.4f} exceeds the ${args.max_spend:.2f} ceiling"
        )
    print(
        f"Coding {len(inputs)} laws with {args.model}; conservative maximum estimate "
        f"${preflight.usd:.4f}"
    )
    coder = ClaudeLawCoder(args.model, args.max_spend)
    coding_rows: list[dict[str, object]] = []
    usage_rows: list[dict[str, object]] = []
    for law, source_text, _ in inputs:
        result, usage = coder.code(law, source_text)
        coding_rows.extend(flatten_result(law, result, args.model))
        usage_rows.append({"law_id": law.law_id, **usage})
        print(f"{law.law_id}: {len(result.obligations)} labels; ${usage.get('cost_usd', 0):.4f}")

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(coding_rows).to_csv(output, index=False)
    usage_output = output.with_name(f"{output.stem}_usage.csv")
    pd.DataFrame(usage_rows).to_csv(usage_output, index=False)
    print(f"Wrote unreviewed labels to {output}")
    print("Human review is required before analysis.")
    return 0


def _read_floor_config(path: str | Path | None) -> dict[str, int] | None:
    if path is None:
        return None
    frame = pd.read_csv(path)
    required = {"domain", "minimum_strength"}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"Federal floor config missing columns: {sorted(missing)}")
    if frame["domain"].duplicated().any():
        duplicates = sorted(frame.loc[frame["domain"].duplicated(), "domain"].unique())
        raise ValueError(f"Federal floor config has duplicate domains: {duplicates}")
    return {
        str(row.domain): int(row.minimum_strength)
        for row in frame[["domain", "minimum_strength"]].itertuples(index=False)
    }


def _attach_temporal_manifest(codings: pd.DataFrame, manifest: pd.DataFrame) -> pd.DataFrame:
    if "law_id" not in codings.columns:
        raise ValueError("Coding data requires law_id for temporal analysis")
    missing_laws = sorted(set(codings["law_id"]) - set(manifest["law_id"]))
    if missing_laws:
        raise ValueError(f"Coding data contains law_id values absent from manifest: {missing_laws}")

    temporal = manifest[
        ["law_id", "effective_date", "inactive_from_date", "mixed_effective_dates"]
    ].rename(
        columns={
            "effective_date": "law_effective_date",
            "inactive_from_date": "law_inactive_from_date",
        }
    )
    return codings.merge(temporal, on="law_id", how="left", validate="many_to_one")


def command_analyze(args: argparse.Namespace) -> int:
    from .plotting import plot_coverage

    codings = pd.read_csv(args.codings)
    manifest = read_manifest(args.manifest)
    codings = _attach_temporal_manifest(codings, manifest)
    states = pd.read_csv(args.states)
    if args.weight_column not in states.columns:
        raise ValueError(f"State universe has no {args.weight_column!r} column")
    states = states[["state", args.weight_column]].rename(columns={args.weight_column: "weight"})
    if states["weight"].isna().any():
        raise ValueError(
            f"Fill every {args.weight_column} value before using that weighting scheme"
        )

    domain_universe = list(load_domains())
    roles = load_domain_roles()
    role_lookup = {domain: role for role, domains in roles.items() for domain in domains}
    grid = prepare_state_domain(
        codings,
        states,
        args.include_unreviewed,
        domains=domain_universe,
        analysis_date=args.analysis_date,
    )
    floor_strengths = _read_floor_config(args.floor_config)
    estimates_all = simulate_all(
        grid,
        floor_strength=args.floor_strength,
        floor_strengths=floor_strengths,
    )
    estimates_all["domain_role"] = estimates_all["domain"].map(role_lookup)

    substantive = estimates_all[estimates_all["domain_role"] == "substantive"].copy()
    effects = scenario_effects(substantive)
    effects["domain_role"] = "substantive"
    legal_structure = estimates_all[estimates_all["domain_role"] != "substantive"].copy()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    substantive.to_csv(output_dir / "scenario_estimates.csv", index=False)
    effects.to_csv(output_dir / "scenario_effects.csv", index=False)
    legal_structure.to_csv(output_dir / "legal_structure_estimates.csv", index=False)
    estimates_all.to_csv(output_dir / "scenario_estimates_all_domains.csv", index=False)
    plot_coverage(substantive, args.figure)
    print(f"Analysis snapshot: {args.analysis_date}")
    print(f"Wrote substantive protection estimates to {output_dir / 'scenario_estimates.csv'}")
    print(f"Wrote enforcement/scope diagnostics to {output_dir / 'legal_structure_estimates.csv'}")
    print(f"Wrote figure to {args.figure}")
    if floor_strengths is not None:
        print(f"Used domain-specific federal floor from {args.floor_config}")
    if args.include_unreviewed:
        print("WARNING: output includes unreviewed model labels and is not a research finding.")
    return 0


def command_apply_reviews(args: argparse.Namespace) -> int:
    codings = pd.read_csv(args.codings)
    reviews = pd.read_csv(args.reviews)
    reviewed = apply_reviews(codings, reviews)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    reviewed.to_csv(output, index=False)
    counts = reviewed["review_status"].value_counts().to_dict()
    print(f"Wrote adjudicated coding data to {output}")
    print(json.dumps(counts, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="uaf", description="U.S. AI federalism research pipeline")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate-sources")
    validate.add_argument("--manifest", default=PROJECT_ROOT / "config" / "source_manifest.csv")
    validate.set_defaults(func=command_validate_sources)

    fetch = subparsers.add_parser("fetch-sources")
    fetch.add_argument("--manifest", default=PROJECT_ROOT / "config" / "source_manifest.csv")
    fetch.add_argument("--limit", type=int)
    fetch.add_argument("--minimum-characters", type=int, default=2_000)
    fetch.add_argument(
        "--receipt-dir", default=PROJECT_ROOT / "data" / "interim" / "source_receipts"
    )
    fetch.set_defaults(func=command_fetch_sources)

    estimate = subparsers.add_parser("estimate-cost")
    estimate.add_argument("--manifest", default=PROJECT_ROOT / "config" / "source_manifest.csv")
    estimate.add_argument("--model", default=model_name())
    estimate.add_argument("--limit", type=int)
    estimate.add_argument("--output-tokens", type=int, default=CODING_MAX_OUTPUT_TOKENS)
    estimate.add_argument("--batch", action="store_true")
    estimate.set_defaults(func=command_estimate_cost)

    code = subparsers.add_parser("code-laws")
    code.add_argument("--manifest", default=PROJECT_ROOT / "config" / "source_manifest.csv")
    code.add_argument("--model", default=model_name())
    code.add_argument("--limit", type=int)
    code.add_argument("--max-spend", type=float, default=max_spend())
    code.add_argument(
        "--output", default=PROJECT_ROOT / "data" / "processed" / "codings_unreviewed.csv"
    )
    code.set_defaults(func=command_code_laws)

    review = subparsers.add_parser("apply-reviews")
    review.add_argument(
        "--codings", default=PROJECT_ROOT / "data" / "processed" / "codings_unreviewed.csv"
    )
    review.add_argument("--reviews", default=PROJECT_ROOT / "data" / "raw" / "review_template.csv")
    review.add_argument(
        "--output", default=PROJECT_ROOT / "data" / "processed" / "codings_reviewed.csv"
    )
    review.set_defaults(func=command_apply_reviews)

    analyze = subparsers.add_parser("analyze")
    analyze.add_argument(
        "--codings", default=PROJECT_ROOT / "data" / "processed" / "codings_reviewed.csv"
    )
    analyze.add_argument("--manifest", default=PROJECT_ROOT / "config" / "source_manifest.csv")
    analyze.add_argument("--states", default=PROJECT_ROOT / "config" / "state_universe.csv")
    analyze.add_argument("--analysis-date", required=True, help="Snapshot date in YYYY-MM-DD format")
    analyze.add_argument("--weight-column", default="weight")
    analyze.add_argument("--floor-strength", type=int, default=1)
    analyze.add_argument(
        "--floor-config",
        help="CSV with domain,minimum_strength columns; overrides --floor-strength",
    )
    analyze.add_argument("--include-unreviewed", action="store_true")
    analyze.add_argument("--output-dir", default=PROJECT_ROOT / "data" / "processed")
    analyze.add_argument("--figure", default=PROJECT_ROOT / "figures" / "coverage_scenarios.png")
    analyze.set_defaults(func=command_analyze)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    raise SystemExit(args.func(args))


if __name__ == "__main__":
    main()
