import pytest
from pydantic import ValidationError

from us_ai_federalism.schema import ObligationLabel


def test_positive_code_requires_quote() -> None:
    with pytest.raises(ValidationError):
        ObligationLabel(
            domain="consumer_notice",
            covered=True,
            strength=1,
            regulated_actor="deployer",
            sector="all",
            section_reference="Sec. 1",
            evidence_quote="",
            confidence=0.9,
        )


def test_negative_code_requires_zero_strength() -> None:
    with pytest.raises(ValidationError):
        ObligationLabel(
            domain="consumer_notice",
            covered=False,
            strength=2,
            regulated_actor="deployer",
            sector="all",
            section_reference="Sec. 1",
            evidence_quote="",
            confidence=0.9,
        )
