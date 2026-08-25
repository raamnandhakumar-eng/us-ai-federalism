# Confirmatory design lock

**Freeze date:** 2026-08-25  
**Status:** locked before the full-corpus coding run

This file records the analysis choices that may not be changed in response to full-corpus results. Any later change must be logged as a deviation and reported as sensitivity analysis.

## 1. Geography and legal universe

The geographic universe is the 50 U.S. states plus the District of Columbia. Municipal law is excluded.

The discovery universe is frozen in `config/discovery_universe.csv`. Discovery uses the Future of Privacy Forum enacted-law chart for 2023–2025, the FPF 2026 chatbot tracker, NCSL's state AI legislation resources, and primary state legislative records used to resolve amendments and controlling texts.

The confirmatory corpus includes an enacted state statute when, by the freeze date, it creates or materially amends an operative AI-specific:

- duty;
- prohibition;
- individual right;
- substantive government-use restriction;
- public enforcement power;
- private right of action;
- penalty; or
- exemption or safe harbor

that maps to the fixed domains in `config/policy_domains.json`.

The confirmatory corpus excludes municipal measures, nonbinding resolutions and study-only measures, definition-only amendments with no independent AI-specific obligation, and pure intellectual-property or ownership rules outside the fixed codebook. Superseded statutes remain in the historical registry but do not enter a later current-law snapshot after their `inactive_from_date`.

## 2. Unit of observation

The base unit is:

`state × law × obligation domain × regulated actor × sector × effective period`

A provision produces separate rows only when duties are independently enforceable, cover materially different actors or sectors, or have different operative periods.

## 3. Fixed domain roles

Headline protection coverage uses only domains assigned `substantive` in `config/domain_roles.json`. Enforcement and scope domains are reported separately and cannot mechanically raise substantive protection coverage.

The fixed substantive-strength scale is:

- 0: absent
- 1: disclosure, reporting, documentation, or procedural duty
- 2: assessment, risk management, mitigation, technical evaluation, or human-review duty
- 3: prohibition or individual right

Strength is legal form, not welfare or compliance cost.

## 4. Temporal rule

The primary current-law snapshot is **2026-08-25**. An obligation enters that snapshot only if:

`effective_date <= 2026-08-25 < inactive_from_date`

where the right inequality is omitted when no verified inactivity date exists.

Future-effective obligations are reported separately and are not counted as current protection. Mixed-effective-date laws require an obligation-level date and fail closed when the date is unresolved.

A secondary forward-looking snapshot of **2027-01-01** is reported because several enacted laws become operative then. It is secondary, not the headline current-law estimate.

## 5. Source and coding hierarchy

Primary enacted legal text controls. Trackers and legislative summaries are discovery tools, not operative evidence.

Every positive machine-assisted row must carry a source passage identifier and a contiguous quotation that deterministically occurs in the retrieved primary text. Exact quotation provenance is necessary but not sufficient for legal correctness.

The coding model is pinned to `claude-haiku-4-5-20251001`. Prompt protocol `0.3.0` is fixed before the full-corpus run. Model output is never publication-eligible without independent legal review.

The 72-row pilot adjudication in `data/validation/pilot_gold_review.csv` is an AI-assisted primary-text benchmark used for pipeline validation. It is explicitly **not** an independent human validation set and every row has `publication_eligible=False`.

## 6. Primary weighting

The primary incidence denominator is resident population using U.S. Census Bureau Vintage 2025 state population estimates in `config/state_universe.csv`.

Unweighted state coverage is always reported alongside population-weighted coverage.

Employment-weighted estimates are secondary and are reported only for labor-market domains if a consistent public BLS denominator is available for every state in the analysis. Missing or incompatible employment data may not be imputed from population.

## 7. Primary counterfactuals

### Current state system

Retain all verified obligations active on the snapshot date.

### Broad federal ceiling

Set state obligations in the selected preemption scope to zero. This is an upper-bound displacement benchmark, not a legal prediction and not a claim that federal law would leave no replacement protection.

### EO 14365 carve-out ceiling

Apply the same ceiling while preserving the modelled carve-out domains `child_safety`, `infrastructure`, and `government_use`.

### Federal floor

For every state-domain cell, apply `max(state_strength, federal_minimum_strength)` while preserving stronger state rules. Domain-specific floor vectors are preferred. Scalar floors 1–3 are sensitivity tests only.

## 8. Primary estimands

For domain `d`, scenario `r`, state `s`, and weight `w_s`:

`C_dr = sum_s w_s I(strength_sdr >= 1) / sum_s w_s`

Primary scenario effects are:

- protection coverage change;
- mean legal-strength change;
- weighted variance of legal strength; and
- binary heterogeneity `2*C*(1-C)`.

These are legal-incidence and regulatory-heterogeneity measures. They are not estimates of dollar compliance cost, innovation effects, safety effects, or welfare.

## 9. Validation and advancement rules

Before expanding from the eight-law pilot, protocol 0.3.0 must pass the repository test suite. The rerun is compared with the committed 72-row adjudication benchmark for quotation provenance and repeated classification errors.

For the full run:

- source retrieval and schema validation must pass before paid calls;
- API cost must be estimated before execution and hard-capped;
- raw model labels remain `unreviewed`;
- assistant adjudication, when used to produce provisional estimates, must be separately identified from independent human review;
- publication-grade confirmatory tables remain locked until independent review is complete.

## 10. Reporting order

The results section will report, in this order:

1. frozen-universe construction and exclusions;
2. source retrieval and unresolved-source missingness;
3. current substantive protection coverage;
4. broad-ceiling exposure;
5. carve-out retention;
6. federal-floor gains;
7. enforcement and scope structure;
8. future-effective 2027 snapshot; and
9. robustness and sensitivity analyses.

No headline result may be described as causal or as a welfare estimate.
