import ssl
from urllib.error import URLError

import pytest

from us_ai_federalism.source_fetch import (
    OFFICIAL_HOST_TLS_FALLBACK,
    _clean_pdf_page,
    _is_certificate_error,
    _unverified_context_for,
    extract_source_text,
)


def test_html_extraction_removes_deleted_language() -> None:
    payload = b"<html><body><p>A deployer shall provide notice.</p><s>shall not</s></body></html>"
    text = extract_source_text(payload, "text/html", "html")
    assert "shall provide notice" in text
    assert "shall not" not in text


def test_short_html_can_be_extracted_before_length_validation() -> None:
    text = extract_source_text(b"<p>Section 1.</p>", "text/html", "html")
    assert text == "Section 1."


def test_line_numbered_legislative_pdf_page_is_cleaned() -> None:
    page = """S. 8828 4
1 A large frontier developer shall write, implement, comply with, and
2 clearly and conspicuously publish on its internet website a fron-
3 tier AI framework that applies to its frontier models.
4 The framework shall describe risk management procedures.
5 A frontier developer shall report a critical safety incident.
6 The report shall be transmitted to the office.
7 The office may adopt regulations.
8 These duties are cumulative with other law.
9 Nothing in this section creates a private right of action.
10 This section applies to frontier models."""
    cleaned = _clean_pdf_page(page)
    assert "S. 8828 4" not in cleaned
    assert "1 A large" not in cleaned
    assert "frontier AI framework" in cleaned
    assert "fron-tier" not in cleaned


def test_non_numbered_pdf_page_preserves_leading_numbers() -> None:
    page = "Section 1. Requirements\n2027 is the operative year.\nA deployer shall provide notice."
    cleaned = _clean_pdf_page(page)
    assert "2027 is the operative year." in cleaned


def test_certificate_verification_failure_is_detected() -> None:
    error = URLError(ssl.SSLCertVerificationError(1, "certificate verify failed"))
    assert _is_certificate_error(error)


def test_unverified_context_is_restricted_to_allowlisted_official_host() -> None:
    context = _unverified_context_for(
        "https://cga.ct.gov/2023/act/example.pdf", OFFICIAL_HOST_TLS_FALLBACK
    )
    assert context.verify_mode == ssl.CERT_NONE
    assert context.check_hostname is False

    with pytest.raises(ValueError, match="allow-listed official hosts"):
        _unverified_context_for(
            "https://example.com/example.pdf", OFFICIAL_HOST_TLS_FALLBACK
        )


def test_unverified_context_requires_explicit_policy() -> None:
    with pytest.raises(ValueError, match="Unsupported transport policy"):
        _unverified_context_for("https://cga.ct.gov/example.pdf", "strict")