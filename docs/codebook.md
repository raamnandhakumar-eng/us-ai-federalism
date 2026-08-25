# Statutory coding codebook

## Evidence rule

A positive code requires operative language such as **shall**, **must**, **may not**, **is prohibited**, **is entitled**, or a clearly granted enforcement power. Every returned row must identify one retrieved `P###` passage and include one contiguous verbatim excerpt from that passage. Do not use ellipses, paraphrases, bracket substitutions, or quotes assembled from separate locations.

Machine-assisted rows also contain `evidence_verified`. This field means only that the quoted text is mechanically present in the cited retrieved passage and the full source text. It does **not** mean the legal interpretation is correct. Human verification remains required.

An express statutory denial of a private right of action may be retained as `private_right`, `covered=false`, `strength=0`. This distinguishes an explicit no-private-action rule from silence.

## Unit of coding

Code one row per independently enforceable obligation. Do not split a single statutory duty merely because it contains several clauses. Split only when duties are independently enforceable or protect materially different actors or rights.

Use the most specific domain supported by the operative provision. Retrieval `DOMAIN_HINTS` are search aids only and are never evidence for a classification.

## Obligation domains

| Domain | Positive-code rule | Common exclusions |
|---|---|---|
| `impact_assessment` | Regulated actor must conduct a formal impact, algorithmic-impact, or risk assessment | General reasonable care; standing risk program; developer only supplies documents for another actor's assessment |
| `risk_management` | Regulated actor must implement a risk policy, program, framework, governance process, or mitigation process | One-off assessment; bare prohibition; duty only to describe risk controls |
| `model_evaluation` | Regulated actor must conduct technical testing, evaluation, red teaming, capability testing, or performance assessment | Documentation saying how prior testing was done, absent a separate testing mandate |
| `human_oversight` | Requires a human person to review, intervene, supervise, or make a decision | Instructions saying how a system should be monitored; internal governance; generic safety controls |
| `consumer_notice` | Requires direct AI-specific notice to a consumer, user, patient, worker, or affected person | Public website posting; business-to-business technical documentation |
| `developer_documentation` | Requires model cards, dataset cards, technical documentation, use instructions, evaluation documentation, or assessment-support information for a downstream developer/deployer/customer or regulator | Direct consumer notice; generally available public report |
| `public_transparency` | Requires a public website posting, public report, public framework, or similar generally available disclosure | Direct individualized notice; downstream technical documentation |
| `explanation_appeal` | Creates explanation, correction, contest, reconsideration, review, or appeal rights | Agency discretion to answer complaints |
| `antidiscrimination` | Prohibits AI-linked discrimination or imposes an enforceable discrimination-risk duty | Civil-rights law mentioned only in findings |
| `incident_reporting` | Requires a regulated entity to report a qualifying AI incident, harm, safety event, or discriminatory outcome | Consumer complaint mechanism; regulator merely creates a reporting channel; regulator reports on its own work |
| `frontier_safety` | Imposes substantive safety, mitigation, evaluation, or incident-management duties specific to frontier/foundation models or catastrophic risk | Generic transparency/reporting duty coded only because the law concerns frontier AI |
| `harmful_use_restriction` | Prohibits developing, deploying, or using AI to cause or facilitate physical harm, self-harm, criminal conduct, coercion, or similar harm | Minor-specific rule, which belongs in `child_safety`; human oversight unless expressly required |
| `child_safety` | Creates an AI-specific prohibition, safeguard, disclosure, design duty, or right specifically protecting minors | Generally applicable child law with no AI-specific rule |
| `health_restriction` | Restricts AI use or creates review/safeguard duties in health care, clinical judgment, insurance medical necessity, or therapy | Health-data privacy alone |
| `synthetic_content` | Requires labeling, watermarking, provenance, detection, or disclosure for AI-generated or manipulated content | General consumer notice unrelated to synthetic content |
| `whistleblower_protection` | Protects insiders who report AI safety risks or violations through anti-retaliation, confidentiality, or reporting rights | General employment protection with no AI nexus |
| `infrastructure` | Regulates AI compute, data centers, related energy systems, siting, or permitting | Generally applicable land-use rules with no AI link |
| `government_use` | Substantively constrains or requires government procurement, deployment, or use of AI | Agency study, administration, enforcement, or reporting duties that do not constrain government AI use |
| `enforcement_authority` | Expressly authorizes a public body to investigate, enforce, seek orders, or seek injunctions | General agency jurisdiction not connected to the act |
| `private_right` | Expressly permits a private civil action or right to sue | Administrative complaint or petition only; silence |
| `penalty` | Specifies a civil, criminal, or administrative penalty for violation | Injunction alone, recorded under enforcement authority |
| `exemption` | Expressly removes or reduces application for an actor, system, use, sector, firm size, or safe-harbor condition | Public-records confidentiality exemption or unrelated background-law exemption |

## Strength scale

| Strength | Meaning |
|---:|---|
| 0 | No positive obligation coded |
| 1 | Disclosure, reporting, documentation, or procedural duty |
| 2 | Assessment, risk-management, mitigation, technical evaluation, or human-review duty |
| 3 | Prohibition or individual right |

Strength describes the legal form of the substantive obligation. It is **not** a welfare score or an enforcement score. A deadline does not increase strength. Penalties, public enforcement authority, and private rights are coded separately.

## Required row fields

| Field | Meaning |
|---|---|
| `coding_id` | Stable hash-based identifier |
| `law_id` | State, session/year, and bill identifier |
| `domain` | One value from the fixed domain list |
| `covered` | Whether an enforceable provision is present |
| `strength` | 0 to 3 using the scale above |
| `regulated_actor` | Developer, deployer, employer, insurer, agency, platform, or other |
| `sector` | Cross-sector or the named sector |
| `effective_date` | Date the obligation becomes operative if visible in supplied text |
| `section_reference` | Statutory section or source page if visible |
| `evidence_passage` | Retrieved passage identifier, for example `P003` |
| `evidence_quote` | One contiguous exact supporting excerpt, capped at 600 characters |
| `evidence_verified` | Mechanical quote-location check; not a legal-validation flag |
| `source_url` | Primary legal source |
| `confidence` | Model or coder confidence from 0 to 1 |
| `review_status` | Unreviewed, verified, revised, rejected, or unresolved |
| `coder` | Human identifier or model name |
| `prompt_version` | Fixed prompt version for machine-assisted labels |

## Ambiguity rules

- Code each duty at the narrowest supported actor and sector.
- Classify the legal duty, not the topic mentioned in the provision.
- Do not infer a private right of action from silence.
- Do not infer preemption from a general conflict clause.
- Do not infer an effective date from bill metadata if the operative passage states something different.
- Preserve delayed operative dates and amendment uncertainty.
- Record scope exemptions separately when possible.
- A public-records confidentiality rule is not an exemption from the AI obligation itself.
- When a primary source and summary conflict, the primary enacted text controls.
- A mechanically verified quotation can still be substantively misclassified.
- Mark cross-references, unresolved amendments, incomplete passages, and ambiguous scope for legal review rather than forcing a label.
