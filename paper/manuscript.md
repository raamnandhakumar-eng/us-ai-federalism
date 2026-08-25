# Federal Floor or Federal Ceiling?

## The Coverage and Fragmentation Effects of Preempting State AI Laws

**Sriramkrishnan (Raam) Nandhakumar**  
**Draft status:** pre-analysis manuscript; no confirmatory estimates reported

## Abstract

Federal proposals increasingly seek a uniform national artificial-intelligence policy, while U.S.
states continue to enact protections governing automated decisions, consumer notice, children,
health, government use, and frontier-model safety. The policy debate often invokes either a costly
“patchwork” or a regulatory vacuum, but it rarely measures which enforceable protections different
preemption designs would remove or preserve. This study constructs an obligation-level dataset of
enacted state AI statutes and simulates a broad federal ceiling, a ceiling with stated carve-outs,
and federal floors of varying strength. Primary outcomes are population-weighted protection
coverage and cross-state dispersion in obligation strength. Claude supplies quotation-backed
first-pass labels under a fixed codebook; all retained labels require human verification against
primary legal text. The design is descriptive and counterfactual, not a causal estimate of
regulation's effects on innovation, safety, or welfare. Results will be inserted only after the
statutory universe is frozen and review is complete.

## 1. Introduction

The central federalism question is not simply whether state AI laws differ. It is whether a chosen
form of national uniformity would standardize overlapping requirements, eliminate substantive
protections, or both. The empirical object is therefore the legally enforceable obligation—not the
bill count.

This paper estimates four quantities: current protection coverage, protection loss under a broad
ceiling, protection retained by policy carve-outs, and coverage gained under a federal floor. The
analysis reports both resident-population weights and unweighted state estimates. Employment or
sector denominators are used only where the regulated population can be defined defensibly.

The paper's intended contribution is an auditable bridge between the legal preemption debate and
measurable policy incidence. The dated novelty audit and closest related work are maintained in
`docs/literature_review.md`.

## 2. Institutional background

### 2.1 State AI legislation

*[Insert frozen-universe counts, enactment timeline, and scope after source collection.]*

### 2.2 Federal preemption proposals

*[Describe the March 2026 White House framework, Executive Order 14365, and any enacted or formally
introduced congressional language as of the freeze date. Separate legal authority from the policy
simulations.]*

## 3. Data

### 3.1 Statutory universe

The confirmatory sample contains enacted statutes with an AI-specific obligation, prohibition,
right, enforcement power, or exemption between January 1, 2023 and the recorded freeze date.
Nonbinding resolutions, study-only measures, executive guidance, and superseded versions are
excluded. Discovery records come from public trackers; final coding uses controlling state legal
text.

### 3.2 Obligation coding

The row is a state-law-domain-actor-sector-effective-period obligation. Positive codes require
operative language, a section or page reference, and a matching quotation. Model outputs remain
unreviewed until a human coder checks the controlling text. A blinded second reviewer independently
codes a stratified 20 percent sample.

### 3.3 Coverage denominators

*[Document Census population year, BLS employment sources, joins, missingness, and denominator
choices.]*

## 4. Methods

For domain \(d\), scenario \(r\), state \(s\), and weight \(w_s\), coverage is

\[
C_{dr}=\frac{\sum_s w_s\mathbb{1}(strength_{sdr}\geq 1)}{\sum_s w_s}.
\]

Protection loss under a federal ceiling is

\[
L_d=C_{d,current}-C_{d,ceiling}.
\]

The paper also reports weighted dispersion in obligation strength, unique state-domain profiles,
and leave-one-state-out sensitivity. These measures describe regulatory heterogeneity; they are not
dollar compliance costs.

## 5. Results

**Locked until source freeze and human review.**

1. Sample construction and missingness
2. Current protection coverage by domain
3. Broad-ceiling protection loss
4. Coverage retained under carve-outs
5. Federal-floor gains and residual heterogeneity
6. Sensitivity analyses

## 6. Limitations

The scenarios are transparent policy counterfactuals, not predictions about congressional text or
judicial interpretation. Strength scores are ordinal and do not measure welfare. Population
coverage does not establish that every resident uses a regulated system or receives equal benefit.
The statutory landscape changes quickly, and effective dates, amendments, exemptions, and agency
rules require continuing verification.

## 7. Policy implications

*[Interpret results in terms of which domains gain uniformity, which protections are displaced,
and where a federal floor could preserve experimentation. Avoid causal or welfare claims.]*

## Reproducibility statement

The repository pins the coding schema, prompt version, model snapshot, source URLs, source hashes,
cost ceiling, simulation rules, and review status. Raw model labels are never treated as final legal
data. Public-law text is retrieved at runtime and is not redistributed as a repository asset.
