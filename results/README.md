# Provisional empirical results

**Freeze date:** 2026-08-25  
**Primary snapshot:** 2026-08-25  
**Sensitivity snapshot:** 2027-01-01  
**Status:** AI-assisted primary-text adjudication. Not publication-grade until independent legal review.

## Corpus

The frozen discovery registry contains 52 candidate state measures. The source-clean confirmatory and snapshot-supplement manifests produced 238 first-pass model rows. Primary-text adjudication plus manual recovery of missed omnibus or codified provisions yields 247 positive provisional obligation rows across 39 laws and 20 states with an operative or future-effective coded obligation.

All retained model quotations in the working adjudication dataset were rechecked against normalized primary legal text. Rows whose original quotation did not match exactly were repaired only when an 8+ word exact anchor could be located in the official source. Manual-recovery rows use direct primary-text quotations.

The row-level working adjudication dataset is not released here as publication-grade legal data. The tables below are the provisional analytical outputs derived from it and should be interpreted subject to independent human review.

## Headline descriptive results

At the 2026-08-25 snapshot, **15 states** have at least one active substantive coded AI protection. Those states contain **41.7%** of the 2025 U.S. state + D.C. population. Mean population-weighted coverage across the 18 substantive codebook domains is **15.6%**.

By 2027-01-01, **19 states** have at least one active substantive coded protection, covering **47.4%** of the population. Mean domain coverage rises to **19.3%**.

The largest population-weighted domains are:

| Domain | 2026-08-25 | 2027-01-01 |
|---|---:|---:|
| Consumer notice | 34.3% | 41.0% |
| Child safety | 22.6% | 34.9% |
| Health restrictions | 27.3% | 29.1% |
| Harmful-use restrictions | 22.6% | 27.0% |
| Risk management | 20.7% | 22.0% |

## Federalism counterfactuals

The simulations are transparent policy benchmarks, not predictions of enacted federal law or judicial preemption.

- **Broad ceiling:** all selected state substantive obligations are displaced. Coverage therefore falls to zero by construction.
- **EO 14365 carve-out benchmark:** child safety, AI infrastructure, and government-use obligations survive. This preserves **11.7%** of aggregate observed domain coverage at the primary snapshot and **13.0%** at the 2027 snapshot.
- **Stylized federal floor:** a strength-1 federal minimum is imposed in every substantive codebook domain and stronger state rules remain. Geographic coverage becomes 100% by construction, while state strength above the floor is preserved.

## Files

- `domain_coverage_2026-08-25.csv`: primary snapshot.
- `domain_coverage_2027-01-01.csv`: 2027 sensitivity snapshot.
- `scenarios_by_domain_2026-08-25.csv`: primary snapshot domain-by-scenario estimates.
- `scenarios_by_domain_2027-01-01.csv`: 2027 domain-by-scenario estimates.
- `scenario_summary.csv`: aggregate scenario summaries.
- `state_summary.csv`: state protection breadth.
- `../figures/*.svg`: vector figures from the provisional results.

## Important limitation

These are **provisional AI-assisted primary-text adjudicated estimates**. They are suitable for repository analysis and a working-paper draft, but not for a claim that legal coding has been independently validated. A second human reviewer should independently code a stratified sample before publication.
