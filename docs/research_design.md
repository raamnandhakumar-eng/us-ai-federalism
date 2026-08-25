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

## Domain roles

The codebook separates three kinds of legal features before any scenario analysis:

1. **Substantive protections**: duties, prohibitions, safeguards, disclosures, review rights, and similar rules governing AI conduct.
2. **Enforcement structure**: public enforcement authority, private rights of action, and penalties.
3. **Scope structure**: exemptions and safe harbors.

Headline **protection coverage** estimates use only substantive domains. Enforcement and scope measures are reported separately rather than counted as additional substantive protections. This prevents, for example, a penalty provision or exemption from mechanically increasing a state's protection-coverage score.

The fixed mapping is committed in `config/domain_roles.json` before analysis.

## Primary variables

### Obligation presence

`covered = 1` only when the operative text creates a mandatory duty, prohibition, individual right, or public enforcement authority appropriate to the coded domain. Findings, legislative intent, voluntary guidance, study commissions, and authorized but unexercised rulemaking are not treated as substantive obligations.

An express statutory statement that no private right of action exists may be retained as a negative enforcement-structure observation. Silence is not coded as an express denial.

### Substantive strength

For substantive domains:

- 0: absent
- 1: disclosure, reporting, documentation, or procedural duty
- 2: assessment, risk-management, mitigation, technical evaluation, or human-review duty
- 3: prohibition or individual right

Strength describes legal form. It is not a welfare score or an enforcement score. Deadlines do not increase strength. Penalties, public enforcement authority, and private rights are coded separately so enforcement is not double-counted in substantive strength.

### Evidence provenance

Every retained machine-assisted row identifies one retrieved `P###` passage and one contiguous verbatim statutory excerpt. A deterministic check records whether that exact normalized quote occurs in both the cited passage and full downloaded primary text. Passing that check establishes quote provenance only; it does not establish that the legal classification is correct.

### Coverage weights

- Unweighted state coverage
- Resident-population coverage
- Employment coverage for labor-market rules
- Sector-specific denominators where a defensible public source exists

Every denominator has a year and source. The analysis reports unweighted estimates when a relevant denominator is unavailable.

## Counterfactuals

1. **Observed state system:** all verified obligations active on the analysis date.
2. **Broad federal ceiling:** all state obligations in the selected preemption scope are displaced.
3. **EO 14365 carve-out ceiling:** displacement excludes modeled state rules on child safety, AI compute/data-center infrastructure, and state government procurement/use.
4. **Federal floor:** a domain-specific federal minimum applies nationally while stronger state obligations remain.

The preferred federal-floor specification is a committed vector of minimum strengths by substantive domain, not one universal scalar. Scalar floors remain available only as sensitivity tests.

These are transparent policy simulations, not legal predictions. The project does not decide whether Congress possesses authority to preempt a particular rule or how a court would interpret a future preemption clause.

## Estimands

For substantive obligation domain \(d\), state \(s\), and scenario \(r\):

\[
C_{dr} = \frac{\sum_s w_s I(strength_{sdr} \geq 1)}{\sum_s w_s}
\]

Protection loss under a ceiling is:

\[
L_d = C_{d,current} - C_{d,ceiling}
\]

The primary ordinal heterogeneity measure is the weighted variance of substantive obligation strength across states. A secondary binary heterogeneity measure is:

\[
H_{dr}^{binary} = 2 C_{dr}(1-C_{dr})
\]

This equals zero when a protection is either absent everywhere or present everywhere and is highest when coverage is evenly split across the weighted state universe. Additional secondary measures can include the number of unique state-domain profiles and pairwise profile distance.

These are regulatory-complexity or legal-heterogeneity measures, not dollar compliance costs.

Enforcement and scope domains receive separate descriptive tables. They are not included in the headline protection-coverage average.

## Reliability protocol

1. A deterministic filter retrieves passages using domain-specific terms and globally removes substantially overlapping windows.
2. Claude codes the retrieved passages into a fixed schema.
3. Every returned row carries a passage ID and contiguous statutory quote; positive rows require both.
4. A deterministic provenance check verifies that the quote occurs in the cited passage and full source text after whitespace normalization.
5. A human reviewer checks every retained code against primary legal text.
6. A blinded second reviewer independently codes a stratified 20% sample.
7. Agreement is reported as raw agreement and Cohen's kappa by domain. Low-prevalence domains also report positive and negative agreement.
8. Disagreements are resolved before simulations, without showing reviewers the direction of scenario effects.

Model output is research assistance, not legal advice or ground truth.

## Source-text hierarchy

The enacted statutory text controls. Legislative summaries, bill digests, findings, press releases, and secondary descriptions may help discover provisions but are not treated as operative evidence when the enacted section is available.

For California bill-text pages, the retrieval pipeline excludes the Legislative Counsel's Digest and, when identifiable, an opening findings section before searching the enacted operative body.

## Sensitivity analysis

- Narrow versus broad definitions of AI-specific law
- Enactment date versus effective date
- Binary presence versus ordinal substantive strength
- Population-weighted versus unweighted results
- Exclusion of statutes lacking machine-readable primary text
- Alternative treatment of delegated rulemaking authority
- Full preemption versus EO 14365 carve-outs
- Alternative domain-specific federal-floor vectors
- Scalar federal-floor strengths from 1 through 3 as a diagnostic
- Alternative treatment of documentation-only obligations
- Leave-one-state-out estimates

## Reporting rules

- Do not publish a headline estimate until the source universe is frozen and human review is complete.
- Report counts of statutes, substantive obligation rows, enforcement/scope rows, states, missing documents, and unresolved amendments.
- Label all model-only outputs as unverified.
- Distinguish current law from future-effective obligations.
- Do not describe simulated heterogeneity as observed business cost.
- Keep introduced-bill results out of the confirmatory tables.
- Do not claim that a domain's ordinal strength measures its social value.
