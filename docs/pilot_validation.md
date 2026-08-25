# Live pilot validation

## Purpose

Paid model calls are used only after free source and test gates pass. Pilot outputs validate the research pipeline; they are not substantive estimates and cannot enter headline analysis until human review is complete.

## Pilot 1: three-law pipeline validation

The first paid model-assisted validation run used:

- Colorado SB24-205
- Texas HB149
- California SB53

GitHub Actions run `32888343065` completed successfully on 2026-08-25 using the pinned `claude-haiku-4-5-20251001` model.

The preflight cost estimate was **$0.104093**. Actual API spend was **$0.069334**:

| Law | Actual API cost |
|---|---:|
| CO-2024-SB205 | $0.021040 |
| TX-2025-HB149 | $0.022656 |
| CA-2025-SB53 | $0.025638 |

The model returned 44 candidate obligation rows. The deterministic quotation-provenance check verified 41 of 44 rows (**93.2%**). The three failed rows were automatically capped at `confidence=0.25` and flagged for human review.

### What Pilot 1 caught

Colorado SB24-205 could not be treated as the controlling 2026 source by itself. Colorado later delayed its requirements and enacted SB26-189, which repealed and reenacted the relevant provisions with new requirements and mixed operative dates.

The Colorado output from Pilot 1 is therefore retained as a pipeline-validation artifact only. It must not enter a later current-law snapshot as if SB24-205 still controlled.

## Temporal protocol changes after Pilot 1

The repository was changed to:

1. preserve amendment and supersession relationships;
2. record an `inactive_from_date` when an enacted source ceases to control;
3. mark laws with mixed section-level operative dates;
4. require an explicit analysis snapshot date;
5. require obligation-level dates for positive rows in mixed-date laws;
6. allow human review to revise operative and inactivity dates; and
7. fail closed when temporal information is incomplete.

## Pilot 2: eight-law diverse temporal validation

After the temporal tests passed, a broader validation sample was run across eight controlling enacted sources:

- Colorado SB26-189
- Texas HB149
- California SB53
- Illinois HB3773 / Public Act 103-0804
- California AB3030
- Connecticut SB1103 / Public Act 23-16
- Washington ESHB2225
- New York S8828

GitHub Actions run `32893623723` completed successfully on 2026-08-25. The workflow first ran lint and tests, fetched and validated all nine source-manifest texts including the historical Colorado source, enforced a **$1.00 hard pilot ceiling**, and only then made the eight model calls.

The conservative preflight estimate was **$0.2656**. Actual API spend was **$0.140119**:

| Law | Candidate rows | Exact quote provenance | Actual API cost |
|---|---:|---:|---:|
| CO-2026-SB189 | 10 | 3/10 | $0.024502 |
| TX-2025-HB149 | 18 | 18/18 | $0.026511 |
| CA-2025-SB53 | 13 | 9/13 | $0.021078 |
| IL-2024-HB3773 | 2 | 2/2 | $0.010316 |
| CA-2024-AB3030 | 3 | 1/3 | $0.006489 |
| CT-2023-SB1103 | 11 | 6/11 | $0.018845 |
| WA-2026-HB2225 | 8 | 4/8 | $0.014163 |
| NY-2026-S8828 | 7 | 0/7 | $0.018215 |
| **Total** | **72** | **43/72 (59.7%)** | **$0.140119** |

All 72 rows remain `unreviewed`. All eight document responses requested human review. The 29 rows that failed exact quote provenance were automatically reduced to `confidence=0.25`; no failed quote is silently treated as validated evidence.

The known cumulative Claude spend across Pilots 1 and 2 is **$0.209453**.

## Source-retrieval incident and resolution

Two attempted Pilot 2 runs stopped during free source retrieval before any model request because the Connecticut General Assembly PDF host could not pass certificate-chain verification on GitHub's Python runner. Those failed attempts spent **$0** on the Claude API.

The repository does not disable TLS verification globally. Instead, Connecticut uses a source-level exception that:

1. is restricted to the allow-listed official host `cga.ct.gov`;
2. is attempted only after ordinary verified TLS fails with a certificate-verification error;
3. requires the expected legal marker `Public Act No. 23-16`;
4. records `tls_verified=false` in the retrieval receipt; and
5. now pins the successfully retrieved raw PDF SHA-256:
   `2bfb035054c6399424eaba95bb7cf3abc3fdfefaa97dcb95eef9d4590a5c586a`.

Future retrievals through that exception must match the pinned bytes.

## What Pilot 2 says about model reliability

The larger pilot exposed a material deterioration in quotation fidelity. Pilot 1 verified 93.2% of candidate evidence quotes automatically; Pilot 2 verified 59.7%. Performance was highly source-dependent: Texas verified 18/18 while New York verified 0/7.

This does **not** establish a legal-coding accuracy rate. Exact quote provenance tests whether the model copied supporting text faithfully from its cited passage. A row can pass provenance and still be legally misclassified. Conversely, a failed quote may point to a real obligation but cannot be accepted without review.

The result is a reason to improve and review the coding stage before scaling, not a reason to discard the empirical design.

## Advancement rule after Pilot 2

Do **not** run the full statutory corpus yet.

Before the next paid expansion:

1. human-review all 72 Pilot 2 candidate rows against primary text;
2. record accept/revise/reject decisions and obligation-level effective dates;
3. diagnose the New York, Colorado, Connecticut, Washington, and California quote failures;
4. tighten the evidence-extraction protocol without weakening exact-match validation;
5. rerun only a small targeted reliability sample if the protocol changes materially;
6. require a materially improved provenance rate before scaling; and
7. freeze the enacted-law universe and denominator sources before the main run.

No pilot-only row should appear in a headline table or figure before these gates are satisfied.