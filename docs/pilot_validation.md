# Live pilot validation

## Purpose

Paid model calls are used only after free source and test gates pass. Pilot outputs validate the research pipeline; they are not substantive estimates and cannot enter headline analysis until independent human review is complete.

## Pilot 1: three-law pipeline validation

The first paid model-assisted validation run used:

- Colorado SB24-205
- Texas HB149
- California SB53

GitHub Actions run `32888343065` completed successfully on 2026-08-25 using the pinned `claude-haiku-4-5-20251001` model.

The preflight cost estimate was **$0.104093**. Actual API spend was **$0.069334**. The model returned 44 candidate obligation rows. The deterministic quotation-provenance check verified 41 of 44 rows (**93.2%**).

The run also caught a temporal-design problem: Colorado SB24-205 could not be treated as controlling 2026 law after later delay and repeal/re-enactment legislation. The repository therefore added amendment chains, inactivity dates, mixed-effective-date handling, explicit snapshot dates, and fail-closed temporal validation.

## Pilot 2: eight-law diverse temporal validation

GitHub Actions run `32893623723` tested eight controlling sources after the temporal protocol changes. All free source and test gates passed before paid calls.

The conservative preflight estimate was **$0.2656**. Actual API spend was **$0.140119**.

| Law | Candidate rows | Exact quote provenance |
|---|---:|---:|
| CO-2026-SB189 | 10 | 3/10 |
| TX-2025-HB149 | 18 | 18/18 |
| CA-2025-SB53 | 13 | 9/13 |
| IL-2024-HB3773 | 2 | 2/2 |
| CA-2024-AB3030 | 3 | 1/3 |
| CT-2023-SB1103 | 11 | 6/11 |
| WA-2026-HB2225 | 8 | 4/8 |
| NY-2026-S8828 | 7 | 0/7 |
| **Total** | **72** | **43/72 (59.7%)** |

The result showed that exact-quote fidelity was highly source-dependent and that passing quote provenance was not equivalent to correct legal classification.

## Primary-text adjudication benchmark

All 72 Pilot 2 rows were subsequently reviewed against the retrieved primary legal text and recorded in `data/validation/pilot_gold_review.csv`.

The adjudication produced:

- **36 verified as classified**;
- **30 revised**; and
- **6 rejected**.

The benchmark identified recurring ontology errors, including adverse-outcome notice being confused with anti-discrimination, an agency-created reporting portal being confused with a regulated-entity incident-reporting duty, public-records confidentiality being confused with a substantive exemption, and recipient-specific AI disclaimers being confused with synthetic-content regulation.

This benchmark is an **AI-assisted primary-text adjudication**, not independent human validation. Every benchmark row is marked `publication_eligible=False`. It is used to improve and test the coding pipeline, not to support publication-grade legal-accuracy claims.

## Protocol 0.3.0 changes

Before a third paid run, the repository:

1. cleaned recurring legislative-PDF line numbers and page headers;
2. dehyphenated words explicitly split across PDF lines;
3. added regression tests for line-numbered legislative PDFs;
4. hardened domain definitions using the adjudication errors;
5. clarified that administrative agency duties are not automatically regulated-entity obligations;
6. clarified the boundaries among consumer notice, anti-discrimination, health restrictions, synthetic content, enforcement authority, penalties, and exemptions; and
7. incremented the fixed prompt protocol to `0.3.0`.

The full test suite passed before the next paid call.

## Pilot 3: protocol 0.3.0 benchmark rerun

GitHub Actions run `32897252597` reran the same eight-law validation sample under protocol `0.3.0`.

The conservative preflight estimate was **$0.2712**. Actual API spend was **$0.141433**. The model returned 79 candidate rows.

| Law | Candidate rows | Exact quote provenance |
|---|---:|---:|
| CO-2026-SB189 | 8 | 5/8 |
| TX-2025-HB149 | 13 | 13/13 |
| CA-2025-SB53 | 19 | 15/19 |
| IL-2024-HB3773 | 2 | 2/2 |
| CA-2024-AB3030 | 3 | 1/3 |
| CT-2023-SB1103 | 11 | 5/11 |
| WA-2026-HB2225 | 7 | 3/7 |
| NY-2026-S8828 | 16 | 16/16 |
| **Total** | **79** | **60/79 (75.9%)** |

The most important source-level improvement was New York: exact quote provenance increased from **0/7 to 16/16** after legislative-PDF normalization. Overall provenance increased from **59.7% to 75.9%**.

The rerun nevertheless showed that classification guardrails do not eliminate all semantic errors. For example, the model could still classify an agency duty to establish a reporting mechanism as `incident_reporting`. Therefore protocol 0.3.0 is suitable for **first-pass corpus coding and provisional analysis only**, not automatic legal ground truth.

## API spend through Pilot 3

Known Claude API spend through the three successful paid pilots is:

- Pilot 1: **$0.069334**
- Pilot 2: **$0.140119**
- Pilot 3: **$0.141433**
- **Cumulative: $0.350886**

The two failed Connecticut-source attempts stopped before model calls and spent **$0**.

## Connecticut source-retrieval exception

The Connecticut General Assembly PDF host cannot pass certificate-chain verification on GitHub's Python runner. The repository does not disable TLS verification globally. Instead, Connecticut uses a source-level exception restricted to `cga.ct.gov`, attempted only after ordinary certificate verification fails, recorded in the source receipt, and protected by the pinned raw PDF SHA-256:

`2bfb035054c6399424eaba95bb7cf3abc3fdfefaa97dcb95eef9d4590a5c586a`

## Advancement decision

Protocol 0.3.0 may now be used for a bounded full-corpus **first-pass** run because:

- source and temporal gates are functioning;
- the legal universe and confirmatory design are frozen before full results;
- the quotation pipeline materially improved;
- known failure modes are documented; and
- raw outputs remain publication-ineligible.

The full-corpus run must still satisfy all of the following:

1. source retrieval and schema validation before paid calls;
2. a hard API cost ceiling;
3. exact-quote provenance checks on every positive row;
4. explicit unresolved-source missingness;
5. provisional labeling for assistant-adjudicated estimates; and
6. independent human review before publication-grade confirmatory claims.
