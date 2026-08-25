# Live pilot validation

## Pilot run

The first paid model-assisted validation run used three enacted-law source records:

- Colorado SB24-205
- Texas HB149
- California SB53

GitHub Actions run `32888343065` completed successfully on 2026-08-25 using the pinned `claude-haiku-4-5-20251001` model.

The preflight cost estimate was **$0.104093**. Actual API spend was **$0.069334** across all three requests:

| Law | Actual API cost |
|---|---:|
| CO-2024-SB205 | $0.021040 |
| TX-2025-HB149 | $0.022656 |
| CA-2025-SB53 | $0.025638 |

The model returned 44 candidate obligation rows. The deterministic quotation-provenance check verified 41 of 44 rows. The three failed rows were automatically capped at `confidence=0.25` and flagged for human review. These figures describe pipeline behavior only. They are not substantive research results.

## What the pilot caught

The pilot exposed a source-version problem before the project scaled. Colorado SB24-205 cannot be treated as the controlling 2026 source by itself. Colorado later delayed its requirements and then enacted SB26-189, which repealed and reenacted the relevant provisions with new requirements and mixed operative dates.

The pilot output is therefore retained only as a model/retrieval validation artifact. Its Colorado labels must not enter a current-law estimate.

## Protocol changes before the next paid run

1. Preserve amendment and supersession relationships in the source manifest.
2. Record an `inactive_from_date` for a source that ceases to control.
3. Mark statutes with mixed section-level operative dates.
4. Require an explicit analysis snapshot date.
5. For mixed-date laws, require an obligation-level effective date before a positive row can enter a dated analysis.
6. Permit human reviewers to revise both operative and inactivity dates.
7. Add regression tests for future-effective and superseded obligations.

## Advancement rule

Do not run the larger pilot or main batch until the temporal-validity tests pass on CI. After they pass, rerun a diverse pilot using the current controlling sources and review the resulting labels before expanding the statutory universe.
