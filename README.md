# Federal Floor or Federal Ceiling?

## The Coverage and Fragmentation Effects of Preempting State AI Laws

An empirical U.S. AI federalism project measuring which public protections would be preserved, displaced, or standardized under alternative federal preemption frameworks.

> **Research status:** pre-analysis design stage. The repository contains a preregistration-ready protocol, source manifest, validation rules, simulation code, and synthetic tests. It does **not** yet report findings from the completed statutory universe.

## Question

Would federal preemption reduce regulatory fragmentation without removing important state-level protections?

The project compares three policy regimes:

| Regime | Policy rule | Quantity estimated |
|---|---|---|
| Current state system | Enacted state protections remain in force | Coverage and heterogeneity observed in coded statutes |
| Federal ceiling | Covered state obligations are displaced | Protections removed and requirements standardized |
| Federal floor | A national minimum applies; stronger state rules remain | National coverage gained while state protections are preserved |

## Why this question now

The White House's March 20, 2026 legislative framework calls for a uniform national AI policy and warns that conflicting state rules could undermine innovation. Executive Order 14365, issued December 11, 2025, directs federal officials to evaluate and challenge certain state AI laws while preserving specified categories such as child safety, AI infrastructure, and state procurement. At the same time, states continue to legislate across consumer protection, health, children, automated decisions, and frontier AI.

Primary institutional sources:

- [White House national AI legislative framework, March 20, 2026](https://www.whitehouse.gov/releases/2026/03/president-donald-j-trump-unveils-national-ai-legislative-framework/)
- [Executive Order 14365, December 11, 2025](https://www.whitehouse.gov/presidential-actions/2025/12/eliminating-state-law-obstruction-of-national-artificial-intelligence-policy/)
- [NCSL Artificial Intelligence Legislation Database](https://www.ncsl.org/financial-services/artificial-intelligence-legislation-database)

## Empirical design

The primary sample is the universe of enacted U.S. state AI statutes from January 1, 2023 through the frozen collection date. Introduced but unenacted bills form a separate appendix and never enter the primary protection estimates.

The coding unit is:

`state × law × enforceable obligation × regulated actor × sector × effective year`

Each obligation is linked to the controlling statutory text, section or page, source URL, coder, confidence score, and human-review status. Claude produces structured first-pass labels only. A human reviewer verifies every retained label against the primary text.

### Primary outcomes

1. **Protection coverage:** share of the U.S. population or relevant employment covered by an enforceable obligation.
2. **Regulatory heterogeneity:** dispersion in obligation presence and strength across states. This is not labeled a compliance-cost estimate.
3. **Preemption exposure:** protection coverage removed under a defined federal-ceiling scenario.
4. **Preservation under a floor:** coverage retained when a federal minimum coexists with stronger state protections.

The project is descriptive and counterfactual. It does not estimate causal effects of regulation on innovation, compliance spending, safety, or welfare.

## Policy domains

The codebook covers impact assessments, model evaluation, human oversight, notice, explanation or appeal, antidiscrimination, incident reporting, frontier-model safety, child protection, health restrictions, government procurement, enforcement authority, private rights of action, penalties, exemptions, and effective dates.

## Reproducible workflow

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# 1. Validate the source manifest and local statute texts
uaf validate-sources --manifest config/source_manifest.csv

# 2. Estimate API cost before making any call
uaf estimate-cost --manifest config/source_manifest.csv

# 3. Run a small synchronous pilot
export ANTHROPIC_API_KEY="your-key-here"
uaf code-laws --manifest config/source_manifest.csv --limit 10 --max-spend 1.00

# 4. Review model labels, apply adjudications, then build estimates
uaf apply-reviews
uaf analyze --codings data/processed/codings_reviewed.csv

# 5. Run tests
pytest
```

The API runner defaults to Claude Haiku 4.5, hashes every request, reuses cached responses, estimates cost before submission, and stops at a user-set spending ceiling. The full run should use Anthropic's Batch API after the pilot passes review.

## Research safeguards

- Freeze the source universe and analysis plan before full coding.
- Use primary legal text for final labels. NCSL supplies discovery metadata, not final legal interpretation.
- Require a quotation and section reference for each positive code.
- Double-code at least 20% of statutes and report agreement by domain.
- Resolve disagreements without showing reviewers the simulated policy result.
- Report low-frequency domains and missing source text explicitly.
- Publish every scenario definition. Do not treat the broad-preemption simulation as a prediction of judicial outcomes.

## Repository structure

```text
config/                 policy domains, sources, and scenario parameters
data/                   raw-text instructions and generated outputs
docs/                   research design, codebook, and policy scenarios
src/us_ai_federalism/   ingestion, coding, validation, metrics, and figures
tests/                  synthetic unit and integration tests
tools/                  reproducible command-line helpers
```

## Author

Sriramkrishnan (Raam) Nandhakumar

## License

Code is released under the MIT License. Statutory text and third-party source material remain subject to their original terms.
