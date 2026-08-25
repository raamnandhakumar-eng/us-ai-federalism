import ssl
from urllib.error import URLError

import pytest

from us_ai_federalism.source_fetch import (
    OFFICIAL_HOST_TLS_FALLBACK,
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