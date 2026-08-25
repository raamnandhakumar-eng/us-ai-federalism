# Data

## What is committed

- `config/source_manifest.csv`: seed records and primary-source links
- `config/reference_sources.csv`: federal and NCSL research sources
- `config/policy_domains.json`: frozen coding taxonomy and retrieval terms
- `data/synthetic/`: invented records used only for tests

## What is not committed

Full statutory text, source exports, API caches, and unreviewed model output stay outside version control. This avoids redistributing third-party material and prevents preliminary labels from appearing as findings.

## Building the primary dataset

1. Export enacted records from the NCSL AI Legislation Database using a documented query and freeze date.
2. Supplement 2023–2024 records using NCSL archives and official state legislative sites.
3. Resolve each record to the final enacted or codified text.
4. Save a plain-text copy at the manifest's `local_text_path`.
5. Record a SHA-256 hash, retrieval date, source URL, and amendment relationship.
6. Run deterministic passage retrieval and model-assisted coding.
7. Human-review all retained obligation rows.

NCSL is a discovery and cross-check source. Primary statutory text controls the final coding.

## Generated schemas

`codings_reviewed.csv` contains one row per obligation with these required fields:

`coding_id, law_id, state, domain, covered, strength, regulated_actor, sector, effective_date, section_reference, evidence_quote, source_url, confidence, review_status, coder, prompt_version`

No model-only row is eligible for a headline estimate.

