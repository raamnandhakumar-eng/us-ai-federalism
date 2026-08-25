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
from .settings import PROJECT_ROOT, load_domains, max_spend, model_name
from .sources import read_manifest, resolve_text_path, validate_sources


def _law_from_row(row: dict[str, str]) -> LawRecord:
    optional = {"enactment_date", "effective_date", "amends_law_id"}
    cleaned = {
        key: (None if key in optional and not value else value) for key, value in row.items()
    }
    return LawRecord.model_validate(cleaned)


def command_validate_sources(args: argparse.Namespace) -> int:
    manifest = read_manifest(args.manifest)
    report = validate_sources(manifest)
    print(report.to_string(index=False))
    missing = int((~report["text_exists"]).sum())
    print(f"\n{len(report)} manifest records; {missing} source texts missing")
    return 1 if missing else 0


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
    preflight = estimate_cost([item[2] for item in inputs], args.model, output_tokens_each=2200)
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


def command_analyze(args: argparse.Namespace) -> int:
    from .plotting import plot_coverage

    codings = pd.read_csv(args.codings)
    states = pd.read_csv(args.states)
    if args.weight_column not in states.columns:
        raise ValueError(f"State universe has no {args.weight_column!r} column")
    states = states[["state", args.weight_column]].rename(columns={args.weight_column: "weight"})
    if states["weight"].isna().any():
        raise ValueError(
            f"Fill every {args.weight_column} value before using that weighting scheme"
        )
    grid = prepare_state_domain(codings, states, args.include_unreviewed)
    estimates = simulate_all(grid, args.floor_strength)
    effects = scenario_effects(estimates)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    estimates.to_csv(output_dir / "scenario_estimates.csv", index=False)
    effects.to_csv(output_dir / "scenario_effects.csv", index=False)
    plot_coverage(estimates, args.figure)
    print(f"Wrote estimates to {output_dir}")
    print(f"Wrote figure to {args.figure}")
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

    estimate = subparsers.add_parser("estimate-cost")
    estimate.add_argument("--manifest", default=PROJECT_ROOT / "config" / "source_manifest.csv")
    estimate.add_argument("--model", default=model_name())
    estimate.add_argument("--limit", type=int)
    estimate.add_argument("--output-tokens", type=int, default=1800)
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
    analyze.add_argument("--states", default=PROJECT_ROOT / "config" / "state_universe.csv")
    analyze.add_argument("--weight-column", default="weight")
    analyze.add_argument("--floor-strength", type=int, default=1)
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
