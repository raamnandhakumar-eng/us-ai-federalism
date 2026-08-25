# Statutory coding codebook

## Evidence rule

A positive code requires operative language such as **shall**, **must**, **may not**, **is prohibited**, **is entitled**, or a clearly granted enforcement power. The row must include the shortest exact excerpt that proves the code and its section or page.

## Obligation domains

| Domain | Positive-code rule | Common exclusions |
|---|---|---|
| `impact_assessment` | Requires an impact, risk, or consequential-decision assessment | Optional internal review; general study commission |
| `model_evaluation` | Requires testing, evaluation, red teaming, or documented performance review | General duty of reasonable care without testing language |
| `human_oversight` | Requires meaningful human review, intervention, or a human decision | Human contact channel that cannot change the decision |
| `consumer_notice` | Requires disclosure that AI is used or that a person is interacting with AI | General privacy notice with no AI-specific content |
| `explanation_appeal` | Creates explanation, correction, contest, review, or appeal rights | Agency discretion to answer complaints |
| `antidiscrimination` | Prohibits AI-linked discrimination or requires bias-risk mitigation | Existing civil-rights law merely referenced in findings |
| `incident_reporting` | Requires reporting specified incidents to government or affected persons | Voluntary notification |
| `frontier_safety` | Requires safety protocols, risk frameworks, thresholds, or reports for frontier/foundation models | General consumer AI rules |
| `child_safety` | Creates AI-specific duties protecting minors | Generally applicable child law with no AI rule |
| `health_restriction` | Restricts AI use in care, insurance, clinical judgment, or mental health | Health-data privacy alone |
| `infrastructure` | Regulates AI compute, data centers, related energy systems, or permitting | Generally applicable land-use rules with no AI link |
| `government_use` | Regulates procurement or use by state/local agencies | Requirements applying only to private deployers |
| `enforcement_authority` | Expressly authorizes a public body to investigate or enforce | General agency jurisdiction not connected to the act |
| `private_right` | Expressly permits a private civil action or remedy | Administrative complaint only |
| `penalty` | Specifies civil, criminal, or administrative penalties | Injunction alone, recorded under enforcement |
| `exemption` | Excludes a class of actor, system, use, sector, or firm size | Scope definitions that do not remove otherwise covered conduct |

## Required row fields

| Field | Meaning |
|---|---|
| `coding_id` | Stable hash-based identifier |
| `law_id` | State, session/year, and bill identifier |
| `domain` | One value from the fixed domain list |
| `covered` | Whether an enforceable provision is present |
| `strength` | 0 to 3 using the research-design scale |
| `regulated_actor` | Developer, deployer, employer, insurer, agency, platform, or other |
| `sector` | Cross-sector or the named sector |
| `effective_date` | Date the obligation becomes operative, if known |
| `section_reference` | Statutory section or source page |
| `evidence_quote` | Exact supporting text, capped at 600 characters |
| `source_url` | Primary legal source |
| `confidence` | Model or coder confidence from 0 to 1 |
| `review_status` | Unreviewed, verified, revised, rejected, or unresolved |
| `coder` | Human identifier or model name |
| `prompt_version` | Fixed prompt version for machine-assisted labels |

## Ambiguity rules

- Code each duty at the narrowest supported actor and sector.
- Do not infer a private right of action from silence.
- Do not infer preemption from a general conflict clause.
- Preserve delayed effective dates.
- Record exemptions as separate rows linked to the affected obligation when possible.
- When a primary source and summary conflict, the primary enacted text controls.
- Mark unresolved amendments for legal review rather than forcing a label.
