# Research design

## Working title

**Federal Floor or Federal Ceiling? The Coverage and Fragmentation Effects of Preempting State AI Laws**

## Confirmatory question

How would alternative federal preemption rules change the population and employment coverage of enforceable protections in enacted state AI statutes?

## Scope and freeze rule

- Geography: 50 states and the District of Columbia.
- Primary period: January 1, 2023 through the publicly recorded collection-freeze date.
- Primary sample: enacted statutes containing an AI-specific obligation, prohibition, right, enforcement power, or exemption.
- Secondary sample: introduced but unenacted bills. These describe legislative activity only.
- Exclusions: resolutions without enforceable duties, executive guidance without legal force, municipal rules, generally applicable laws that do not expressly regulate AI, and superseded bill versions.
- Amendment rule: code the law in force at the freeze date and preserve links to amending acts.

The freeze date, database query settings, and unresolved source records must be committed before the full model-assisted coding run.

## Unit of observation

The base row is one legally distinct obligation:

`state × law × obligation domain × regulated actor × sector × effective period`

A single section may generate multiple rows when it applies different duties to different actors or sectors. Identical wording repeated in the same law is coded once unless its effective date or regulated population differs.

## Primary variables

### Obligation presence

`covered = 1` only when the operative text creates a mandatory duty, prohibition, individual right, or public enforcement authority. Findings, legislative intent, voluntary guidance, study commissions, and authorized but unexercised rulemaking are coded separately.

### Strength

- 0: absent
- 1: disclosure, documentation, or procedural duty
- 2: assessment, mitigation, review, or enforceable conduct requirement
- 3: prohibition, individual right, mandatory human decision, or duty backed by specified penalties

Strength is domain-specific and is not interpreted as welfare value.

### Coverage weights

- Unweighted state coverage
- Resident-population coverage
- Employment coverage for labor-market rules
- Sector-specific denominators where a defensible public source exists

Every denominator has a year and source. The analysis reports unweighted estimates when a relevant denominator is unavailable.

## Counterfactuals

1. **Observed state system:** all coded obligations active on the analysis date.
2. **Broad federal ceiling:** all AI-specific state obligations in the selected policy domain are displaced.
3. **EO 14365 carve-out ceiling:** displacement excludes lawful state rules on child safety, AI compute and data-center infrastructure, and state government procurement/use.
4. **Federal floor:** every state receives the specified minimum strength; stronger state obligations remain.

These are transparent policy simulations, not legal predictions. The project does not decide whether Congress possesses authority to preempt a particular rule or how a court would interpret a clause.

## Estimands

For obligation domain \(d\), state \(s\), and scenario \(r\):

\[
C_{dr} = \frac{\sum_s w_s I(strength_{sdr} \geq 1)}{\sum_s w_s}
\]

Protection loss under a ceiling is:

\[
L_d = C_{d,current} - C_{d,ceiling}
\]

The primary heterogeneity measure is the weighted variance of obligation strength across states. Secondary measures include the number of unique state-domain profiles and mean pairwise distance. These are regulatory-complexity measures, not dollar compliance costs.

## Reliability protocol

1. A deterministic filter retrieves passages using domain-specific terms.
2. Claude codes the retrieved passage into the fixed schema.
3. Every positive code requires an exact supporting excerpt and section reference.
4. A human reviewer checks every retained code against primary legal text.
5. A blinded second reviewer independently codes a stratified 20% sample.
6. Agreement is reported as raw agreement and Cohen's kappa by domain. Low-prevalence domains also report positive and negative agreement.
7. Disagreements are resolved before simulations, without showing reviewers the direction of scenario effects.

Model output is research assistance, not legal advice or ground truth.

## Sensitivity analysis

- Narrow versus broad definitions of AI-specific law
- Enactment date versus effective date
- Binary presence versus ordinal strength
- Population-weighted versus unweighted results
- Exclusion of statutes lacking machine-readable primary text
- Alternative treatment of rulemaking authority
- Full preemption versus EO 14365 carve-outs
- Federal-floor strength values from 1 through 3
- Leave-one-state-out estimates

## Reporting rules

- Do not publish a headline estimate until the source universe is frozen and human review is complete.
- Report counts of statutes, obligation rows, states, missing documents, and unresolved amendments.
- Label all model-only outputs as unverified.
- Distinguish current law from future effective obligations.
- Do not describe simulated heterogeneity as observed business cost.
- Keep introduced-bill results out of the confirmatory tables.

