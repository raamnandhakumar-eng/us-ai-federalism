from types import SimpleNamespace

import pytest

from us_ai_federalism.coding import _coerce_research_schema, _extract_parsed_output
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
    assert result.needs_human_review is True
