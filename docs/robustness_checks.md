# Robustness checks

**Analysis snapshots:** 2026-08-25 and 2027-01-01  
**Status:** provisional, AI-assisted primary-text adjudication; independent human legal review remains pending.

These checks test whether the paper's descriptive conclusions depend on (1) population weighting, (2) the three largest early-moving states in the coded corpus, or (3) a single carve-out mapping for federal preemption.

## 1. Unweighted state results

The main analysis weights states by Census Vintage 2025 population. As a robustness check, every state and D.C. receives equal weight.

| Outcome | 2026-08-25 | 2027-01-01 |
|---|---:|---:|
| Jurisdictions with ≥1 active substantive domain | 15/51 (29.4%) | 19/51 (37.3%) |
| Mean unweighted domain coverage | 7.2% | 10.1% |
| Main population-weighted mean domain coverage | 15.6% | 19.3% |

The gap between population-weighted and unweighted estimates shows that early AI regulation is concentrated in populous states. The substantive conclusion is unchanged: protections are geographically incomplete and domain-specific, but the population-weighted incidence is materially larger than the simple state count suggests.

The full domain table is in `results/robustness_unweighted_domain_coverage.csv`.

## 2. Leave-large-state-out sensitivity

The analysis recomputes population-weighted coverage after excluding California, Texas, New York, and all three simultaneously. Population weights are renormalized over the remaining jurisdictions.

| Specification | 2026 mean domain coverage | 2027 mean domain coverage |
|---|---:|---:|
| Baseline | 15.6% | 19.3% |
| Exclude California | 11.1% | 15.3% |
| Exclude Texas | 10.4% | 14.5% |
| Exclude New York | 15.9% | 17.7% |
| Exclude CA, TX, NY | 4.1% | 6.5% |

California and Texas materially raise the population-weighted level of protection coverage. New York has little effect on the August 2026 snapshot but becomes more important by January 2027 as additional provisions become operative. Excluding all three reduces the level sharply but does not eliminate state-level protection: 12 of the remaining 48 jurisdictions still have at least one active substantive domain in August 2026, rising to 16 in January 2027.

This is not a failure of the main result. It identifies a second empirical feature of U.S. AI federalism: protection coverage is both fragmented across domains and concentrated in a small number of large states.

The aggregate sensitivity results are in `results/robustness_leave_large_states_out_summary.csv`.

## 3. Alternative preemption-mapping bounds

The EO 14365 scenario in the main analysis is intentionally narrow: only `child_safety`, `infrastructure`, and `government_use` survive the ceiling. Because mapping statutory obligations into federal carve-outs is legally contestable, the robustness analysis adds a broader preservation bound.

The expanded bound preserves the narrow domains plus `consumer_notice`, `health_restriction`, `harmful_use_restriction`, `antidiscrimination`, and `explanation_appeal`. This is a stylized upper preservation mapping for protections plausibly associated with traditional police powers and consumer protection. It is **not** a prediction that any particular statute would survive preemption.

| Mapping | Retained share of observed coverage, 2026 | Retained share, 2027 |
|---|---:|---:|
| Broad ceiling | 0.0% | 0.0% |
| Narrow EO 14365 mapping | 11.7% | 13.0% |
| Expanded police-power preservation bound | 52.1% | 49.9% |
| No-preemption reference | 100.0% | 100.0% |

Under the expanded mapping, mean domain coverage after preemption would be 8.1% in August 2026 and 9.6% in January 2027, compared with 15.6% and 19.3% under current state law.

The policy conclusion therefore depends strongly on the legal scope of a federal ceiling. The paper reports preemption exposure as a range across transparent mappings rather than presenting the narrow EO mapping as a definitive legal forecast.

The mapping table is in `results/robustness_preemption_mapping_bounds.csv`.

## Interpretation

The robustness checks sharpen rather than overturn the main result:

1. Population weighting raises estimated incidence because large states are prominent early regulators.
2. California and Texas account for a substantial share of population-weighted coverage, but meaningful regulation remains outside them.
3. The amount of protection displaced by federal preemption is highly sensitive to the carve-out definition.

Accordingly, the paper's strongest claim is not that any one federal proposal would remove a fixed percentage of protections. It is that the choice between a ceiling, carve-outs, and a floor has quantitatively different implications for both protection coverage and interstate heterogeneity, and those implications can be measured transparently.
