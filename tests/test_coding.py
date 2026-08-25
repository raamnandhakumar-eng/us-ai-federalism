from types import SimpleNamespace

import pytest

from us_ai_federalism.coding import (
    _coerce_research_schema,
    _extract_parsed_output,
    _verify_quotes,
)
from us_ai_federalism.retrieval import Passage
from us_ai_federalism.schema import RawLawCodingResponse


def test_extract_parsed_output_accepts_sdk_parsed_model() -> None:
    expected = RawLawCodingResponse(
        law_id="CO-2024-SB205",
        obligations=[],
        document_notes="Pilot",
        needs_human_review=True,
    )
    message = SimpleNamespace(content=[SimpleNamespace(type="text", parsed_output=expected)])
    assert _extract_parsed_output(message) == expected


def test_extract_parsed_output_rejects_plain_text() -> None:
    message = SimpleNamespace(content=[SimpleNamespace(type="text", text="{}")])
    with pytest.raises(ValueError, match="parsed structured output"):
        _extract_parsed_output(message)


def test_coercion_clips_to_strict_exact_excerpt() -> None:
    quote = "A deployer shall provide notice " * 40
    raw = RawLawCodingResponse.model_validate(
        {
            "law_id": "CO-2024-SB205",
            "obligations": [
                {
                    "domain": "consumer_notice",
                    "covered": True,
                    "strength": 1,
                    "regulated_actor": "deployer",
                    "sector": "all",
                    "effective_date": "2026-02-01",
                    "section_reference": "6-1-1703",
                    "evidence_passage": "P001",
                    "evidence_quote": quote,
                    "confidence": 0.9,
                    "notes": "",
                }
            ],
            "document_notes": "",
            "needs_human_review": False,
        }
    )
    result = _coerce_research_schema(raw)
    assert len(result.obligations[0].evidence_quote) <= 600
    assert quote.startswith(result.obligations[0].evidence_quote)
    assert result.obligations[0].evidence_passage == "P001"
    assert result.needs_human_review is True


def test_verifier_accepts_quote_across_extracted_line_breaks() -> None:
    source = "Section 1. A deployer shall\nprovide notice to the consumer before deployment."
    passage = Passage(
        passage_id="P001",
        domain="consumer_notice",
        start=0,
        end=len(source),
        text=source,
    )
    raw = RawLawCodingResponse.model_validate(
        {
            "law_id": "CO-2024-SB205",
            "obligations": [
                {
                    "domain": "consumer_notice",
                    "covered": True,
                    "strength": 1,
                    "regulated_actor": "deployer",
                    "sector": "all",
                    "section_reference": "Section 1",
                    "evidence_passage": "P001",
                    "evidence_quote": (
                        "A deployer shall provide notice to the consumer before deployment."
                    ),
                    "confidence": 0.9,
                    "notes": "",
                }
            ],
            "document_notes": "",
            "needs_human_review": False,
        }
    )
    result = _verify_quotes(_coerce_research_schema(raw), source, [passage])
    assert result.obligations[0].evidence_verified is True
    assert result.obligations[0].confidence == 0.9


def test_verifier_rejects_noncontiguous_quote() -> None:
    source = "Section 1. A deployer shall provide notice promptly to the consumer."
    passage = Passage("P001", "consumer_notice", 0, len(source), source)
    raw = RawLawCodingResponse.model_validate(
        {
            "law_id": "CO-2024-SB205",
            "obligations": [
                {
                    "domain": "consumer_notice",
                    "covered": True,
                    "strength": 1,
                    "regulated_actor": "deployer",
                    "sector": "all",
                    "section_reference": "Section 1",
                    "evidence_passage": "P001",
                    "evidence_quote": "A deployer shall provide notice to the consumer.",
                    "confidence": 0.95,
                    "notes": "",
                }
            ],
            "document_notes": "",
            "needs_human_review": False,
        }
    )
    result = _verify_quotes(_coerce_research_schema(raw), source, [passage])
    assert result.obligations[0].evidence_verified is False
    assert result.obligations[0].confidence == 0.25
    assert result.needs_human_review is True
