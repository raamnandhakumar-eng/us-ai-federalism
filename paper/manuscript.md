# Federal Floor or Federal Ceiling?

## The Coverage and Fragmentation Effects of Preempting State AI Laws

**Sriramkrishnan (Raam) Nandhakumar**  
**Draft status:** provisional working paper; empirical results reported; independent human legal validation pending

## Abstract

Federal policymakers increasingly seek a uniform national artificial-intelligence framework while U.S. states continue to enact enforceable protections governing automated decisions, consumer notice, children, health care, government use, and frontier-model safety. The federalism debate often invokes a regulatory “patchwork,” but it rarely measures which protections would actually disappear, survive, or become nationally uniform under different preemption designs. This paper constructs an obligation-level dataset of enacted state AI statutes and simulates a broad federal ceiling, a narrow carve-out ceiling based on Executive Order 14365 categories, a broader police-power preservation bound, and a stylized federal floor.

The frozen discovery registry contains 52 candidate state measures. After source validation, model-assisted first-pass coding, primary-text adjudication, and manual recovery of provisions missed inside omnibus or codified statutes, the working dataset contains 247 positive obligation rows across 39 laws. Using Census Vintage 2025 population weights, 15 states have at least one active substantive coded AI protection on August 25, 2026, covering 41.7% of the U.S. state-plus-D.C. population. By January 1, 2027, 19 states are covered, representing 47.4% of the population. Mean population-weighted coverage across 18 substantive domains rises from 15.6% to 19.3%. Consumer notice is the broadest domain, while child-safety coverage expands most sharply over the near term.

The distribution is highly concentrated. Unweighted mean domain coverage is only 7.2% in August 2026 and 10.1% in January 2027. Removing California lowers the August population-weighted mean from 15.6% to 11.1%; removing Texas lowers it to 10.4%; removing California, Texas, and New York together lowers it to 4.1%. Preemption exposure is also highly sensitive to legal mapping. A narrow EO 14365 carve-out benchmark retains 11.7% of observed aggregate domain coverage in August 2026, whereas an expanded police-power preservation bound retains 52.1%.

The results show that state AI regulation is simultaneously fragmented and concentrated: geographically incomplete, uneven across policy domains, and disproportionately located in several populous states. The analysis is descriptive and counterfactual rather than causal. Current legal coding is AI-assisted primary-text adjudication and remains provisional until independent human validation is completed.

## 1. Introduction

The central question in U.S. AI federalism is not simply whether state laws differ. It is whether national uniformity would standardize overlapping obligations, eliminate substantive protections, or do both at once.

That distinction matters because “fragmentation” is not a single quantity. A firm may face different rules across jurisdictions, but residents in those jurisdictions may also receive different rights, disclosures, safety protections, or review procedures. A federal ceiling can reduce interstate legal variation by displacing state rules. A federal floor can reduce geographic gaps while preserving stricter state protections. These two forms of uniformity are not empirically equivalent.

This paper measures the difference.

The unit of analysis is the enforceable statutory obligation rather than the bill count. Each retained obligation is assigned to a fixed policy domain, legal strength level, regulated actor, sector, and effective period. The analysis then asks four questions.

First, how much of the U.S. population is currently covered by enforceable state AI protections? Second, how does that coverage vary across domains such as consumer notice, child safety, health restrictions, human oversight, antidiscrimination, and frontier-model safety? Third, how much observed protection coverage would be exposed under alternative federal-ceiling mappings? Fourth, how much geographic inequality would a national minimum eliminate if stronger state protections remained in place?

The empirical contribution is therefore not a new legislative tracker. Existing work has already established that AI federalism is an important political, legal, and institutional issue. The contribution is a statute-level, obligation-level counterfactual that converts the preemption debate into measurable quantities: population-weighted protection coverage, strength, and interstate heterogeneity.

Three findings stand out.

First, state AI protections reach a substantial share of the U.S. population despite being adopted by a minority of jurisdictions. On August 25, 2026, 15 of 51 jurisdictions have at least one active substantive coded protection, but those states contain 41.7% of the national state-plus-D.C. population. By January 1, 2027, the figures rise to 19 jurisdictions and 47.4% of the population.

Second, that reach is highly concentrated. Mean population-weighted domain coverage is 15.6% in August 2026, but mean unweighted state coverage is only 7.2%. California and Texas are especially influential. Removing either state lowers the population-weighted mean domain coverage by roughly four to five percentage points. Removing California, Texas, and New York together lowers it to 4.1%.

Third, estimates of “protection lost to preemption” depend heavily on what the federal ceiling actually preserves. A narrow EO 14365 carve-out mapping retains only 11.7% of observed aggregate domain coverage in August 2026. An expanded mapping that also preserves several consumer-protection and police-power domains retains 52.1%. The empirical implication is not that one of these mappings is legally correct. It is that preemption exposure should be reported as a transparent range rather than as a single pseudo-precise legal forecast.

These findings support a narrower but more defensible conclusion than the usual “patchwork versus innovation” framing. State AI governance is both fragmented and concentrated. A ceiling can reduce legal heterogeneity partly by eliminating protections concentrated in several large states. A floor can close geographic gaps without necessarily erasing higher-strength state rules. Which tradeoff Congress chooses is a policy question; this paper measures the distributional structure of that choice.

## 2. Institutional Background

### 2.1 State AI legislation

State AI governance has developed through multiple sectoral and cross-sector approaches rather than through one common model. The coded corpus includes rules governing consumer-facing chatbots, health-care uses, employment decisions, government deployment, model transparency, catastrophic-risk management, synthetic content, and protection of minors.

This heterogeneity makes simple enactment counts difficult to interpret. Two statutes can both be described as “AI laws” while imposing very different legal burdens and creating very different protections. A disclosure requirement, an individual right to review, a ban on a class of conduct, and an agency reporting duty are not interchangeable.

The analysis therefore codes legal obligations rather than statutes as indivisible units.

### 2.2 Federal preemption

The federal policy debate has moved toward explicit consideration of national uniformity and limits on state AI regulation. The White House's March 20, 2026 national AI legislative framework calls for a uniform federal approach while preserving selected areas of state authority. Executive Order 14365, issued December 11, 2025, similarly identifies categories such as child safety, AI infrastructure, and state government procurement or use as areas that may receive different treatment from other state AI restrictions.

This paper does not treat either document as a self-executing statutory preemption rule. Instead, they motivate transparent counterfactual scenarios.

A broad ceiling removes selected state obligations. A narrow carve-out ceiling preserves the three express EO-style categories coded in the repository. A broader preservation bound additionally protects several domains plausibly associated with traditional police powers or consumer protection. Finally, a stylized federal floor imposes a national minimum while preserving stronger state strength scores.

These are simulations, not predictions of congressional drafting or judicial doctrine.

## 3. Related Literature and Contribution

The paper sits at the intersection of AI federalism, empirical studies of state AI legislation, and broader research on regulatory fragmentation.

Rubenstein's *Federalism & Algorithms* maps the doctrinal and institutional terrain of AI federalism and establishes that AI governance raises familiar but unusually dynamic federalism questions. Mallinson, Robles, Best, and Azevedo examine federal preemption and state policy experimentation directly. Agrawal and coauthors empirically describe patterns in state AI legislation. Dawson and coauthors study conditions associated with passage of state AI bills. Fu and Phillips-Robins place AI preemption in the historical context of federal technology regulation. Kalmenovitz, Lowry, and Volkova demonstrate in a different institutional setting that regulatory fragmentation can have measurable firm-level consequences.

This paper differs in estimand. It does not ask which states legislate, which bills pass, or whether federalism is normatively desirable. It estimates how alternative preemption rules change the population-weighted coverage and interstate dispersion of enforceable state AI protections.

The qualified novelty claim is therefore narrow:

> To our knowledge as of August 25, 2026, this is the first statute-level empirical study to estimate how alternative federal AI preemption rules would change population-weighted coverage of enforceable state protections and the cross-state dispersion of those protections.

The literature and search protocol are documented in `docs/literature_review.md`.

## 4. Data

### 4.1 Statutory universe

The empirical freeze is August 25, 2026. Geography is the 50 states plus the District of Columbia. The discovery registry contains 52 candidate measures identified through public legislative trackers and primary-source cross-checking.

The confirmatory sample includes enacted statutes containing an AI-specific obligation, prohibition, individual right, enforcement power, or scope rule. Nonbinding resolutions, study-only measures, guidance, and superseded enactment text are excluded from the primary protection estimates.

The source pipeline validates official legal text before any model-assisted coding occurs. Official state legislative text, public acts, enrolled bills, session laws, or codified statutes are used as controlling sources. Tracker data are used for discovery, not final legal interpretation.

### 4.2 Unit of observation

The coding unit is:

`state × law × obligation domain × regulated actor × sector × effective period`

The working analysis contains 247 positive obligation rows across 39 laws. Twenty states have at least one coded obligation that is active on one of the two analysis dates or becomes effective later within the coded horizon.

The fixed substantive domain universe contains 18 categories:

- impact assessment
- risk management
- model evaluation
- human oversight
- consumer notice
- developer documentation
- public transparency
- explanation or appeal
- antidiscrimination
- incident reporting
- frontier-model safety
- harmful-use restrictions
- child safety
- health restrictions
- synthetic content
- whistleblower protection
- infrastructure
- government use

Enforcement and scope domains are retained separately in the underlying coding but are excluded from the headline substantive-coverage mean.

### 4.3 Strength scale

Each positive obligation receives an ordinal strength score:

- **1**: disclosure, reporting, documentation, or procedural requirement;
- **2**: assessment, risk management, mitigation, evaluation, or required human review;
- **3**: prohibition or individual right.

The score measures legal form, not social value or expected effectiveness.

### 4.4 Model assistance and adjudication

Claude Haiku 4.5 (`claude-haiku-4-5-20251001`) supplies structured first-pass labels under prompt protocol 0.3.0.

Three validation pilots were run before the full corpus. The third pilot improved exact quotation provenance to 75.9%, but the benchmark also demonstrated that quotation fidelity does not guarantee correct semantic classification. The full main corpus generated 204 candidate rows; the supplemental run generated 34.

The current working dataset then underwent AI-assisted primary-text adjudication. Misclassified rows were revised or rejected, exact quotation anchors were checked against normalized official text, and provisions missed by retrieval inside omnibus or codified laws were manually recovered from the primary text.

This is not independent human legal validation. The dataset and all estimates remain provisional until a second human reviewer independently checks a stratified sample.

Known Claude API spend across pilots and full runs is $0.858473.

### 4.5 Effective dates and snapshots

The primary snapshot is August 25, 2026. January 1, 2027 is a prespecified near-term sensitivity date.

A positive obligation enters a snapshot only when its obligation-level effective date is on or before the analysis date. Mixed-date statutes are not assigned a single guessed effective date. Where an omnibus act contains different operative dates, the obligation-level date controls.

### 4.6 Population denominator

The primary weight is Census Vintage 2025 resident population for the 50 states plus D.C., totaling 341,784,857.

Population weighting measures the share of residents located in jurisdictions with a coded protection. It does not imply that every resident uses the regulated technology or receives equal practical benefit.

## 5. Methods

### 5.1 State-domain strength

For state \(s\), domain \(d\), and analysis date \(t\), define the state-domain strength as the maximum active legal strength among coded obligations in that cell:

\[
S_{sdt} = \max_j strength_{jsdt}.
\]

A state-domain cell is covered when \(S_{sdt} \geq 1\).

### 5.2 Population-weighted coverage

For state population weight \(w_s\), domain coverage is:

\[
C_{dt} =
\frac{\sum_s w_s \mathbb{1}(S_{sdt}\geq1)}
{\sum_s w_s}.
\]

The paper also reports mean strength and weighted variance in strength across jurisdictions.

### 5.3 Regulatory heterogeneity

Binary coverage heterogeneity is summarized as:

\[
H_{dt}=2C_{dt}(1-C_{dt}).
\]

The analysis also reports weighted variance in the 0–3 strength score. These are measures of interstate legal heterogeneity, not compliance-cost estimates.

### 5.4 Counterfactual scenarios

Four core regimes are simulated.

**Current state system.** Active state-domain strengths are retained.

**Broad federal ceiling.** Selected state obligations are set to zero. In the headline benchmark, all 18 substantive domains are displaced.

**EO 14365 carve-out ceiling.** The broad ceiling applies except to child safety, infrastructure, and government use.

**Federal floor.** Each state-domain strength is replaced by:

\[
S^{floor}_{sd}=\max(S_{sd},1).
\]

This closes binary geographic coverage gaps by construction while retaining strength above the federal minimum.

A robustness analysis adds an expanded preservation bound covering the narrow carve-outs plus consumer notice, health restrictions, harmful-use restrictions, antidiscrimination, and explanation or appeal.

## 6. Results

### 6.1 Geographic reach

On August 25, 2026, 15 states have at least one active substantive coded AI protection. Those states contain 41.7% of the 2025 U.S. state-plus-D.C. population.

By January 1, 2027, 19 states have at least one active substantive protection, covering 47.4% of the population. Colorado, Oregon, Rhode Island, and Washington enter the active set by the later snapshot, alongside additional obligations becoming operative within states already covered.

The result illustrates the difference between jurisdiction counts and population incidence. Fewer than one-third of jurisdictions are active in the primary snapshot, yet more than two-fifths of the population lives in one of them.

### 6.2 Coverage by domain

Mean population-weighted coverage across the 18 substantive domains is 15.6% in August 2026 and 19.3% in January 2027.

| Domain | Aug. 25, 2026 | Jan. 1, 2027 | States 2026 | States 2027 |
|---|---:|---:|---:|---:|
| Consumer notice | 34.3% | 41.0% | 9 | 14 |
| Health restrictions | 27.3% | 29.1% | 5 | 6 |
| Child safety | 22.6% | 34.9% | 5 | 10 |
| Harmful-use restrictions | 22.6% | 27.0% | 5 | 8 |
| Incident reporting | 20.8% | 26.6% | 2 | 3 |
| Risk management | 20.7% | 22.0% | 8 | 9 |
| Antidiscrimination | 17.3% | 17.3% | 6 | 6 |
| Public transparency | 13.5% | 22.9% | 3 | 6 |

Consumer notice is the broadest domain at both dates. Child-safety coverage expands most rapidly, increasing by 12.3 percentage points. Public transparency and developer documentation also expand materially as 2027-effective statutes enter the snapshot.

Infrastructure has no active substantive coded coverage at either headline date under the fixed codebook.

![Population-weighted coverage by substantive domain](../figures/domain_coverage_current.svg)

### 6.3 State protection breadth

The state-level pattern is heterogeneous. Texas has 12 active substantive domains in the primary snapshot, California 9, Utah 7, and Connecticut, Maryland, and Montana 5 each. By January 2027, Connecticut rises to 9 active domains, New York to 8, and Colorado to 7.

The pattern is therefore not merely that some states regulate and others do not. Active states also differ substantially in the breadth and legal strength of their protection portfolios.

![State protection breadth](../figures/state_protection_breadth.svg)

### 6.4 Federal ceiling and floor scenarios

Under the broad-ceiling benchmark, substantive state protection coverage falls to zero by construction. This should be interpreted as an upper-bound displacement scenario rather than as a prediction of likely federal law.

Under the narrow EO 14365 carve-out mapping, mean domain coverage falls from 15.6% to 1.8% in August 2026 and from 19.3% to 2.5% in January 2027. Expressed relative to observed aggregate domain coverage, the narrow carve-outs retain 11.7% in the primary snapshot and 13.0% in the 2027 snapshot.

The stylized federal floor moves binary geographic coverage to 100% in every substantive domain by construction. Mean strength rises from 0.333 to 1.178 in August 2026 and from 0.404 to 1.211 in January 2027. Binary coverage heterogeneity falls to zero, although strength variance remains positive because states above the minimum retain stronger rules.

![Aggregate coverage across policy scenarios](../figures/scenario_coverage.svg)

## 7. Robustness

### 7.1 Unweighted state estimates

Population weighting materially raises measured incidence because several large states are active early regulators.

On August 25, 2026, 15 of 51 jurisdictions have at least one substantive protection, or 29.4% on an unweighted basis. Mean unweighted coverage across the 18 domains is 7.2%, compared with 15.6% when weighted by population.

By January 1, 2027, 19 of 51 jurisdictions are covered, or 37.3%, and mean unweighted domain coverage rises to 10.1%, compared with 19.3% population-weighted.

The conclusion that regulation is geographically incomplete survives. The level of population incidence, however, depends strongly on the fact that several populous states are early movers.

### 7.2 Leave-California, Texas, and New York out

The second robustness check removes three populous and policy-relevant states and renormalizes the population denominator.

| Specification | Aug. 2026 mean domain coverage | Jan. 2027 |
|---|---:|---:|
| Baseline | 15.6% | 19.3% |
| Exclude California | 11.1% | 15.3% |
| Exclude Texas | 10.4% | 14.5% |
| Exclude New York | 15.9% | 17.7% |
| Exclude CA, TX, NY | 4.1% | 6.5% |

California and Texas individually account for substantial population-weighted protection coverage. New York has little effect on the August mean but becomes more consequential by January 2027 as additional provisions become active.

Excluding all three states sharply lowers the level, but it does not eliminate the broader phenomenon. Twelve of the remaining 48 jurisdictions still have at least one active substantive domain in August 2026, increasing to 16 by January 2027.

This concentration is itself a federalism result: national preemption can alter protection coverage for a large share of the population by changing the law in a relatively small number of large states.

### 7.3 Alternative preemption-mapping bounds

Legal mapping is the most important scenario uncertainty.

The narrow EO benchmark preserves only child safety, infrastructure, and government use. The expanded police-power preservation bound additionally retains consumer notice, health restrictions, harmful-use restrictions, antidiscrimination, and explanation or appeal.

| Mapping | Retained observed coverage, Aug. 2026 | Jan. 2027 |
|---|---:|---:|
| Broad ceiling | 0.0% | 0.0% |
| Narrow EO mapping | 11.7% | 13.0% |
| Expanded preservation bound | 52.1% | 49.9% |
| No-preemption reference | 100.0% | 100.0% |

Under the expanded mapping, post-preemption mean domain coverage is 8.1% in August 2026 and 9.6% in January 2027.

The large gap between the narrow and expanded mappings shows why the paper does not describe one carve-out simulation as a legal forecast. The robust conclusion is conditional: a broad ceiling can substantially reduce observed state protection coverage, but the magnitude depends on which categories Congress or courts preserve.

Detailed robustness outputs are in `docs/robustness_checks.md` and the `results/robustness_*.csv` files.

## 8. Discussion

The results complicate both sides of the usual federalism narrative.

A “patchwork” framing is directionally correct in the sense that obligation presence and legal strength vary substantially across states. But the pattern is not a uniform fifty-state maze. Most jurisdictions have no active coded protection in many domains, while a smaller set of states—especially several populous states—account for a large share of population-weighted incidence.

A “regulatory vacuum” framing is also incomplete. By August 2026, state protections are already relevant to more than two-fifths of the national population on an any-protection basis. Several domains reach materially large population shares even though only a handful of jurisdictions regulate them.

This matters for federal design.

A ceiling achieves uniformity partly through subtraction. Where protections are concentrated in large states, displacement can affect a large population share even if the number of preempted jurisdictions is modest.

A floor achieves a different kind of uniformity. It closes geographic gaps but can preserve state experimentation above the minimum. In the stylized strength-1 simulation, every jurisdiction receives baseline coverage while higher state strength survives.

The paper does not establish that a floor is socially optimal. Federal uniformity may reduce transaction costs, legal uncertainty, or duplicative compliance. State variation may create experimentation benefits or impose real burdens. The present analysis measures protection coverage and heterogeneity, not innovation, firm entry, compliance expenditure, or welfare.

Its value is therefore diagnostic. It identifies what is being standardized and what is being displaced.

## 9. Limitations

The most important limitation is legal validation. Current codings are based on model-assisted extraction followed by AI-assisted primary-text adjudication. They have not yet been independently validated by a second human legal reviewer. All results should therefore be treated as provisional working-paper estimates.

Second, population coverage is an incidence proxy. A resident living in a covered state is not necessarily exposed to the regulated AI system, and sector-specific protections may apply only to subsets of the population.

Third, the 0–3 strength scale is ordinal. A score of 3 is not “three times stronger” than a score of 1, and strength does not measure enforcement intensity, compliance, or social welfare.

Fourth, the federal preemption scenarios are stylized. They do not predict final congressional text or judicial interpretation. The alternative-mapping robustness analysis partially addresses this by reporting a wide preservation range.

Fifth, the statutory landscape changes quickly. The freeze date provides reproducibility but means later enactments, amendments, rules, and litigation are outside the study period.

Finally, the current analysis focuses on statutory legal form. It does not yet estimate domain-specific employment denominators, regulated-firm exposure, or downstream behavioral effects.

## 10. Conclusion

The empirical structure of U.S. AI federalism is neither nationwide uniformity nor a simple fifty-state patchwork.

As of August 25, 2026, a minority of jurisdictions have active substantive AI protections, but those states contain 41.7% of the U.S. state-plus-D.C. population. By January 1, 2027, coverage rises to 47.4%. Protection types vary sharply by domain, and population-weighted incidence is concentrated in several large states.

That concentration changes the meaning of federal preemption. A ceiling can reduce interstate heterogeneity while simultaneously removing protections affecting large population shares. The magnitude of that effect is highly sensitive to the scope of federal carve-outs: the narrow EO-style mapping retains only 11.7% of observed aggregate coverage in the primary snapshot, while a broader police-power preservation bound retains 52.1%.

A federal floor presents a different counterfactual. It can eliminate geographic coverage gaps while preserving higher state strength above the minimum.

The central policy tradeoff is therefore not merely fragmentation versus uniformity. It is **which form of uniformity** federal law creates—and which existing protections that choice leaves intact.

## Reproducibility statement

The repository freezes the source universe, analysis dates, codebook, prompt version, model snapshot, source URLs, source hashes, population weights, scenario definitions, and robustness specifications. Paid model calls were preceded by source and test gates. Known Claude API spend is $0.858473.

Core outputs are stored in `results/`, figures in `figures/`, and the final analysis and robustness protocols in `docs/`.

Independent human legal review remains the final publication gate.

## References

- Agrawal, L., Mulgund, P., DaSouza, R. O., Bhaya, K., and Singh, R. (2026). “AI Regulation in U.S. States: Lessons Learned and Key Takeaways.” *Communications of the ACM*, 69(6), 68–77. https://doi.org/10.1145/3778178
- Dawson, G. S., Desouza, K. C., Denford, J. S., and Picavet, M. E. B. (2026). “Analyzing the Passage of State-Level AI Bills.” Brookings Institution.
- Fu, Y., and Phillips-Robins, A. (2025). “When Should Congress Preempt State AI Law? The Lessons of Past Technologies.” Carnegie Endowment for International Peace.
- Kalmenovitz, J., Lowry, M., and Volkova, E. (2025). “Regulatory Fragmentation.” *Journal of Finance*. https://doi.org/10.1111/jofi.13423
- Mallinson, D. J., Robles, P., Best, E., and Azevedo, L. (2026). “Artificial Intelligence’s Future Is in the States, if the Federal Government Allows.” *Publius: The Journal of Federalism*, 56(3), 733–761. https://doi.org/10.1093/publius/pjag017
- Rubenstein, D. S. (2025; revised 2026). “Federalism & Algorithms.” *Arizona Law Review*, Vol. 67, Issue 4. SSRN 5290048.
- National Conference of State Legislatures. “Artificial Intelligence Legislation Database.”
- International Association of Privacy Professionals. “U.S. State AI Governance Legislation Tracker.”
