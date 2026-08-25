from __future__ import annotations

import hashlib
import json
import re
import ssl
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from lxml import html
from pypdf import PdfReader

from .retrieval import normalize_text

USER_AGENT = "us-ai-federalism/0.1 (+https://github.com/raamnandhakumar-eng/us-ai-federalism)"
MAX_DOWNLOAD_BYTES = 25 * 1024 * 1024
MIN_TEXT_CHARACTERS = 2_000
STRICT_TRANSPORT = "strict"
OFFICIAL_HOST_TLS_FALLBACK = "official_host_tls_fallback"
TLS_FALLBACK_HOSTS = {"cga.ct.gov"}


@dataclass(frozen=True)
class SourceReceipt:
    law_id: str
    requested_url: str
    resolved_url: str
    retrieved_at_utc: str
    content_type: str
    raw_bytes: int
    raw_sha256: str
    text_characters: int
    text_sha256: str
    output_path: str
    transport_policy: str
    tls_verified: bool
    expected_raw_sha256: str
    raw_hash_matched: bool | None
    expected_text_marker: str


def _read_response(
    request: Request,
    *,
    timeout: int,
    context: ssl.SSLContext | None = None,
) -> tuple[bytes, str, str]:
    kwargs: dict[str, object] = {"timeout": timeout}
    if context is not None:
        kwargs["context"] = context
    with urlopen(request, **kwargs) as response:  # type: ignore[arg-type]
        declared = int(response.headers.get("Content-Length", "0") or 0)
        if declared > MAX_DOWNLOAD_BYTES:
            raise ValueError(
                f"Source declares {declared:,} bytes; limit is {MAX_DOWNLOAD_BYTES:,}"
            )
        payload = response.read(MAX_DOWNLOAD_BYTES + 1)
        if len(payload) > MAX_DOWNLOAD_BYTES:
            raise ValueError(f"Source exceeds {MAX_DOWNLOAD_BYTES:,}-byte limit")
        return payload, response.headers.get_content_type(), response.geturl()


def _is_certificate_error(exc: Exception) -> bool:
    if isinstance(exc, ssl.SSLCertVerificationError):
        return True
    if isinstance(exc, URLError):
        reason = exc.reason
        if isinstance(reason, ssl.SSLCertVerificationError):
            return True
        return "CERTIFICATE_VERIFY_FAILED" in str(reason)
    return "CERTIFICATE_VERIFY_FAILED" in str(exc)


def _unverified_context_for(url: str, transport_policy: str) -> ssl.SSLContext:
    parsed = urlparse(url)
    if transport_policy != OFFICIAL_HOST_TLS_FALLBACK:
        raise ValueError(f"Unsupported transport policy: {transport_policy!r}")
    if parsed.scheme != "https" or parsed.hostname not in TLS_FALLBACK_HOSTS:
        raise ValueError(
            "Unverified TLS fallback is restricted to explicitly allow-listed official hosts"
        )
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    return context


def _download(
    url: str,
    timeout: int = 60,
    attempts: int = 3,
    transport_policy: str = STRICT_TRANSPORT,
) -> tuple[bytes, str, str, bool]:
    request = Request(
        url, headers={"User-Agent": USER_AGENT, "Accept": "text/html,application/pdf"}
    )
    last_error: Exception | None = None
    for attempt in range(attempts):
        try:
            payload, content_type, resolved_url = _read_response(request, timeout=timeout)
            return payload, content_type, resolved_url, True
        except (HTTPError, URLError, TimeoutError) as exc:
            last_error = exc
            if attempt + 1 < attempts:
                time.sleep(2**attempt)

    assert last_error is not None
    if transport_policy == STRICT_TRANSPORT or not _is_certificate_error(last_error):
        raise last_error

    context = _unverified_context_for(url, transport_policy)
    payload, content_type, resolved_url = _read_response(
        request, timeout=timeout, context=context
    )
    return payload, content_type, resolved_url, False


def _is_pdf_header(line: str) -> bool:
    compact = line.strip()
    return bool(
        re.fullmatch(r"[A-Z]\.?\s*\d+[A-Z-]*\s+\d+", compact)
        or re.fullmatch(r"PAGE\s+\d+[-–].+", compact, flags=re.IGNORECASE)
        or re.fullmatch(r".+Public Act No\.\s*\S+\s+\d+\s+of\s+\d+", compact)
    )


def _clean_pdf_page(text: str) -> str:
    """Remove recurring legislative-PDF artifacts without rewriting legal words.

    Some official bill PDFs, especially New York Senate PDFs, extract with a printed line number
    before nearly every text line and page labels between clauses. Those artifacts caused otherwise
    verbatim model quotations to fail deterministic provenance checks. We remove line numbers only
    when the page is strongly detected as line-numbered, and dehyphenate only a word explicitly
    split at a line ending.
    """

    lines = [line.rstrip() for line in text.splitlines() if line.strip()]
    if not lines:
        return ""

    numbered = sum(bool(re.match(r"^\s*\d{1,2}\s+\S", line)) for line in lines)
    line_numbered_page = numbered >= 8 and numbered / len(lines) >= 0.45

    cleaned: list[str] = []
    for raw in lines:
        line = raw.strip()
        if _is_pdf_header(line):
            continue
        if line_numbered_page:
            line = re.sub(r"^\d{1,2}\s+", "", line).strip()
        if not line or _is_pdf_header(line):
            continue

        if cleaned and cleaned[-1].endswith("-") and re.match(r"^[a-z]", line):
            cleaned[-1] = cleaned[-1][:-1] + line
        else:
            cleaned.append(line)
    return "\n".join(cleaned)


def _pdf_text(payload: bytes) -> str:
    reader = PdfReader(BytesIO(payload))
    if reader.is_encrypted:
        raise ValueError("Encrypted PDF cannot be processed")
    return "\n\n".join(_clean_pdf_page(page.extract_text() or "") for page in reader.pages)


def _html_text(payload: bytes) -> str:
    document = html.fromstring(payload)
    for unwanted in document.xpath("//script|//style|//noscript|//svg|//nav|//footer|//s|//del"):
        unwanted.drop_tree()
    return document.text_content()


def extract_source_text(payload: bytes, content_type: str, source_format: str) -> str:
    format_hint = source_format.strip().lower()
    if content_type == "application/pdf" or format_hint == "pdf" or payload.startswith(b"%PDF"):
        text = _pdf_text(payload)
    elif content_type in {"text/html", "application/xhtml+xml"} or format_hint == "html":
        text = _html_text(payload)
    else:
        raise ValueError(f"Unsupported source format: {source_format!r} ({content_type})")
    return normalize_text(text).strip()


def fetch_source(
    *,
    law_id: str,
    url: str,
    source_format: str,
    output_path: Path,
    receipt_path: Path,
    minimum_characters: int = MIN_TEXT_CHARACTERS,
    transport_policy: str = STRICT_TRANSPORT,
    expected_raw_sha256: str = "",
    expected_text_marker: str = "",
) -> SourceReceipt:
    payload, content_type, resolved_url, tls_verified = _download(
        url, transport_policy=transport_policy
    )
    raw_sha256 = hashlib.sha256(payload).hexdigest()
    raw_hash_matched: bool | None = None
    if expected_raw_sha256:
        raw_hash_matched = raw_sha256 == expected_raw_sha256
        if not raw_hash_matched:
            raise ValueError(
                f"{law_id} raw SHA-256 changed: expected {expected_raw_sha256}, "
                f"got {raw_sha256}"
            )

    text = extract_source_text(payload, content_type, source_format)
    if len(text) < minimum_characters:
        raise ValueError(
            f"{law_id} produced only {len(text):,} text characters; "
            f"minimum is {minimum_characters:,}"
        )
    if expected_text_marker and expected_text_marker not in text:
        raise ValueError(
            f"{law_id} does not contain expected legal marker {expected_text_marker!r}"
        )
    if not tls_verified and not (expected_raw_sha256 or expected_text_marker):
        raise ValueError(
            f"{law_id} used unverified TLS without a pinned hash or expected legal marker"
        )

    receipt = SourceReceipt(
        law_id=law_id,
        requested_url=url,
        resolved_url=resolved_url,
        retrieved_at_utc=datetime.now(timezone.utc).isoformat(),
        content_type=content_type,
        raw_bytes=len(payload),
        raw_sha256=raw_sha256,
        text_characters=len(text),
        text_sha256=hashlib.sha256(text.encode("utf-8")).hexdigest(),
        output_path=str(output_path),
        transport_policy=transport_policy,
        tls_verified=tls_verified,
        expected_raw_sha256=expected_raw_sha256,
        raw_hash_matched=raw_hash_matched,
        expected_text_marker=expected_text_marker,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text + "\n", encoding="utf-8")
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(json.dumps(asdict(receipt), indent=2) + "\n", encoding="utf-8")
    return receipt