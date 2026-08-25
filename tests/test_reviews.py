import pandas as pd
import pytest

from us_ai_federalism.reviews import apply_reviews


def test_revision_changes_coded_value_and_preserves_status() -> None:
    codings = pd.DataFrame(
        [
            {
                "coding_id": "x",
                "covered": True,
                "domain": "consumer_notice",
                "strength": 1,
                "evidence_quote": "shall notify",
                "review_status": "unreviewed",
            }
        ]
    )
    reviews = pd.DataFrame(
        [
            {
                "coding_id": "x",
                "reviewer_id": "r1",
                "review_status": "revised",
                "revised_domain": "human_oversight",
                "revised_strength": 2,
                "review_reason": "Human review is mandatory.",
            }
        ]
    )
    result = apply_reviews(codings, reviews)
    assert result.loc[0, "domain"] == "human_oversight"
    assert result.loc[0, "strength"] == 2
    assert result.loc[0, "review_status"] == "revised"


def test_duplicate_reviews_fail() -> None:
    codings = pd.DataFrame([{"coding_id": "x", "covered": True, "evidence_quote": "text"}])
    reviews = pd.DataFrame(
        [
            {"coding_id": "x", "review_status": "verified"},
            {"coding_id": "x", "review_status": "rejected"},
        ]
    )
    with pytest.raises(ValueError):
        apply_reviews(codings, reviews)
