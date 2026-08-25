# Statutory coding codebook

## Evidence rule

A positive code requires operative language such as **shall**, **must**, **may not**, **is prohibited**, **is entitled**, or a clearly granted enforcement power. Every positive row must identify one retrieved `P###` passage and include one contiguous verbatim excerpt from that passage. Do not use ellipses, paraphrases, bracket substitutions, or quotes assembled from separate locations.

Machine-assisted rows also contain `evidence_verified`. This field means only that the quoted text is mechanically present in the cited retrieved passage and the full source text. It does **not** mean the legal interpretation is correct. Human verification remains required.

## Unit of coding

Code one row per independently enforceable obligation. Do not split a single statutory duty merely because it contains several clauses. Split only when duties are independently enforceable or protect materially different actors or rights.

Use the most specific domain supported by the operative provision. Retrieval `DOMAIN_HINTS` are search aids only and are never evidence for a classification.

## Obligation domains

| Domain | Positive-code rule | Common exclusions |
|---|---|---|
| `impact_assessment` | Requires a formal impact, algorithmic-impact, or risk assessment of an AI system or deployment | General reasonable-care duty; standing risk-management program; ordinary testing |
| `risk_management` | Requires a risk policy, program, framework, governance process, or mitigation process | One-off impact assessment; bare prohibition |
| `model_evaluation` | Requires technical testing, evaluation, red teaming, capability testing, or performance assessment | Producing records to an investigator; general policy review |
| `human_oversight` | Requires a human person to review, intervene, supervise, or make a decision | Internal governance; generic safety controls; harmful-use prohibition with no human reviewer |
| `consumer_notice` | Requires direct AI-specific notice to a consumer, user, patient, worker, or affected person | Public website posting or general public report |
| `public_transparency` | Requires a public website posting, public report, public framework, or similar generally available disclosure | Direct individualized notice |
| `explanation_appeal` | Creates explanation, correction, contest, reconsideration, review, or appeal rights | Agency discretion to answer complaints |
| `antidiscrimination` | Prohibits AI-linked discrimination or imposes an enforceable discrimination-risk duty | Civil-rights law mentioned only in findings |
| `incident_reporting` | Requires a regulated entity to report a qualifying AI incident, harm, safety event, or discriminatory outcome | Consumer complaint mechanism; regulator report about its own enforcement activity |
| `frontier_safety` | Imposes a substantive safety, mitigation, evaluation, or incident-management duty specific to frontier/foundation models or catastrophic risk | Transparency duty coded only because the law concerns frontier AI |
| `harmful_use_restriction` | Prohibits developing, deploying, or using AI to cause or facilitate physical harm, self-harm, criminal conduct, coercion, or similar harm | Minor-specific rule, which belongs in `child_safety`; human oversight unless expressly required |
| `child_safety` | Creates an AI-specific prohibition, safeguard, disclosure, design duty, or right specifically protecting minors | Generally applicable child law with no AI-specific rule |
| `health_restriction` | Restricts AI use or creates review/safeguard duties in health care, clinical judgment, insurance medical necessity, or therapy | Health-data privacy alone |
| `synthetic_content` | Requires labeling, watermarking, provenance, detection, or disclosure for AI-generated or manipulated content | General consumer notice unrelated to synthetic content |
| `whistleblower_protection` | Protects insiders who report AI safety risks or violations through anti-retaliation, confidentiality, or reporting rights | General employment protection with no AI nexus |
| `infrastructure` | Regulates AI compute, data centers, related energy systems, siting, or permitting | Generally applicable land-use rules with no AI link |
| `government_use` | Substantively constrains or requires government procurement, deployment, or use of AI | Agency study, administration, enforcement, or reporting duties that do not constrain government AI use |
| `enforcement_authority` | Expressly authorizes a public body to investigate, enforce, seek orders, or seek injunctions | General agency jurisdiction not connected to the act |
| `private_right` | Expressly permits a private civil action or right to sue | Administrative complaint or petition only |
| `penalty` | Specifies a civil, criminal, or administrative penalty for violation | Injunction alone, recorded under enforcement authority |
| `exemption` | Expressly removes or reduces application for an actor, system, use, sector, firm size, or safe-harbor condition | Scope definition that does not remove otherwise covered conduct |

## Strength scale

| Strength | Meaning |
|---:|---|
| 0 | No positive obligation coded |
| 1 | Disclosure or procedural duty |
| 2 | Assessment, risk-management, mitigation, evaluation, or human-review duty |
| 3 | Prohibition, individual right, mandatory human decision, or mandate backed by a specified penalty |

Strength is an ordinal description of legal form. It is **not** a welfare score and should not be interpreted as the social value of a protection.

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
- Do not infer a private right of action from silence.
- Do not infer preemption from a general conflict clause.
- Do not infer an effective date from bill metadata if the operative passage states something different.
- Preserve delayed operative dates and amendment uncertainty.
- Record exemptions as separate rows linked to the affected obligation when possible.
- When a primary source and summary conflict, the primary enacted text controls.
- A mechanically verified quotation can still be substantively misclassified.
- Mark cross-references, unresolved amendments, incomplete passages, and ambiguous scope for legal review rather than forcing a label.
