# Final analysis protocol

## Frozen design

The empirical freeze is August 25, 2026. The primary geography is the 50 states plus the District of
Columbia. The primary snapshot is August 25, 2026; January 1, 2027 is a prespecified near-term
effective-date sensitivity.

The unit of coding is:

`state × law × obligation domain × regulated actor × sector × effective period`

Only enacted, enforceable obligations, prohibitions, rights, enforcement powers, or scope rules that map to
the fixed codebook are retained. Superseded versions are not treated as simultaneously controlling.

## Primary-text adjudication

Claude Haiku 4.5 (`claude-haiku-4-5-20251001`) supplies first-pass structured labels. The full main run
generated 204 rows; the snapshot supplement generated 34. The full main run cost $0.423328 and the
supplement cost $0.084259. Together with three validation pilots ($0.350886), known cumulative API spend is
**$0.858473**.

For the provisional reviewed dataset:

1. every retained row is checked against the downloaded official legal text;
2. original exact quotations are preserved where valid;
3. failed quotations are repaired only where the source contains an exact 8+ word anchor from the model
   quote, after which a contiguous source passage is stored;
4. semantic misclassifications are revised using the frozen domain definitions;
5. rows that infer an obligation from regulator authority, background law, or an unrelated provision are
   rejected;
6. operative dates are resolved at the row level for mixed-effective-date statutes; and
7. provisions missed by passage retrieval in omnibus or codified laws are manually recovered from primary text.

This is AI-assisted legal adjudication, not independent human validation.

## Weighting

Population weights use Census Population Estimates Program Vintage 2025 state estimates. The 50 states plus
D.C. sum to 341,784,857 residents. Population coverage is:

`sum(population_s × 1[strength_sd >= 1]) / sum(population_s)`

No employment-weighted headline estimate is reported because a single defensible employment denominator
does not exist across all policy domains.

## Strength

- 0: absent
- 1: disclosure, reporting, documentation, or procedure
- 2: assessment, risk management, mitigation, evaluation, or human review
- 3: prohibition or individual right

Strength is an ordinal legal-form measure, not a welfare or enforcement-effectiveness score.

## Scenarios

1. **Current:** retain active reviewed state obligations.
2. **Broad ceiling:** set selected state substantive obligations to zero.
3. **EO 14365 carve-outs:** broad ceiling except child safety, AI infrastructure, and government use.
4. **Federal floor:** impose a stylized strength-1 minimum across substantive domains and retain stronger
   state rules.

The broad ceiling and federal floor are bounding counterfactuals. They are not forecasts of federal statutory
text.

## Publication gate

Before publication-grade confirmatory claims:

- independently human-review a stratified 20% sample;
- report raw agreement and Cohen's kappa by domain where prevalence permits;
- resolve disagreements without access to scenario results;
- rerun all tables from the locked review file; and
- update the freeze if the paper claims a later legal date.
