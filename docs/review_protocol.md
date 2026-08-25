# Human review protocol

## Reviewer task

For each model-generated row, open the primary source and assign one status:

- `verified`: the domain, actor, sector, strength, date, section, and quotation are correct.
- `revised`: the row is substantively valid after recorded corrections.
- `rejected`: the text does not establish the coded obligation.
- `unresolved`: amendments, cross-references, or legal ambiguity require further review.

Reviewers must not see scenario estimates while coding.

## Required checks

1. Confirm the document is the final enacted or codified version.
2. Confirm later amendments and operative dates.
3. Locate the quotation in the primary text.
4. Confirm that the language is mandatory or creates a right or enforcement authority.
5. Confirm the narrowest supported actor and sector.
6. Confirm strength using the domain-specific codebook.
7. Record a short reason for every revision, rejection, or unresolved decision.

## Reliability sample

Independently double-code at least 20% of statutes. Stratify the draw by state, year, policy domain, statute length, and model confidence. Preserve both original reviews before adjudication.

Report:

- Raw agreement
- Cohen's kappa by domain
- Positive and negative agreement for rare codes
- Share of model positives verified without revision
- Error categories: wrong domain, nonbinding text, actor/sector mismatch, bad quotation, wrong strength, superseded text

## Release rule

Only `verified` and `revised` rows enter the primary analysis. Release unreviewed model labels separately, if at all, with a prominent warning.

