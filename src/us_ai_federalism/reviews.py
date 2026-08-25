from __future__ import annotations

import pandas as pd

VALID_STATUSES = {"verified", "revised", "rejected", "unresolved"}
REVISION_MAP = {
    "revised_domain": "domain",
    "revised_strength": "strength",
    "revised_actor": "regulated_actor",
    "revised_sector": "sector",
    "revised_effective_date": "effective_date",
    "revised_inactive_from_date": "inactive_from_date",
    "revised_section_reference": "section_reference",
    "revised_evidence_quote": "evidence_quote",
}


def apply_reviews(codings: pd.DataFrame, reviews: pd.DataFrame) -> pd.DataFrame:
    if "coding_id" not in codings or "coding_id" not in reviews:
        raise ValueError("Both files require coding_id")
    if reviews["coding_id"].duplicated().any():
        raise ValueError("Each coding_id may have only one adjudicated review")
    unknown = set(reviews["review_status"].dropna()) - VALID_STATUSES
    if unknown:
        raise ValueError(f"Unknown review statuses: {sorted(unknown)}")

    review_columns = ["coding_id", "review_status", "reviewer_id", "review_reason", *REVISION_MAP]
    available = [column for column in review_columns if column in reviews.columns]
    merged = codings.drop(columns=["review_status"], errors="ignore").merge(
        reviews[available], on="coding_id", how="left", validate="one_to_one"
    )
    merged["review_status"] = merged["review_status"].fillna("unreviewed")
    revised_mask = merged["review_status"].eq("revised")
    for revision, target in REVISION_MAP.items():
        if revision not in merged:
            continue
        replacement = merged[revision].notna() & merged[revision].astype(str).str.strip().ne("")
        merged.loc[revised_mask & replacement, target] = merged.loc[
            revised_mask & replacement, revision
        ]
    invalid_positive = (
        merged["review_status"].isin({"verified", "revised"})
        & merged["covered"].astype(str).str.lower().isin({"true", "1"})
        & merged["evidence_quote"].fillna("").str.strip().eq("")
    )
    if invalid_positive.any():
        ids = merged.loc[invalid_positive, "coding_id"].tolist()
        raise ValueError(f"Reviewed positive rows missing evidence: {ids}")
    return merged
