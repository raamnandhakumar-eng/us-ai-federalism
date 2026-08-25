from us_ai_federalism.source_fetch import extract_source_text


def test_html_extraction_removes_deleted_language() -> None:
    payload = b"<html><body><p>A deployer shall provide notice.</p><s>shall not</s></body></html>"
    text = extract_source_text(payload, "text/html", "html")
    assert "shall provide notice" in text
    assert "shall not" not in text


def test_short_html_can_be_extracted_before_length_validation() -> None:
    text = extract_source_text(b"<p>Section 1.</p>", "text/html", "html")
    assert text == "Section 1."
