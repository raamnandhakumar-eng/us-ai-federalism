from types import SimpleNamespace

import pytest

from us_ai_federalism.coding import _extract_parsed_output
from us_ai_federalism.schema import LawCodingResponse


def test_extract_parsed_output_accepts_sdk_parsed_model() -> None:
    expected = LawCodingResponse(
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
