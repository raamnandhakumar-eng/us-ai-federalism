from __future__ import annotations

import hashlib
import json
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from lxml import html
from pypdf import PdfReader

from .retrieval import normalize_text

USER_AGENT = "us-ai-federalism/0.1 (+https://github.com/raamnandhakumar-eng/us-ai-federalism)"
MAX_DOWNLOAD_BYTES = 25 * 1024 * 1024
MIN_TEXT_CHARACTERS = 2_000


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


def _download(url: str, timeout: int = 60, attempts: int = 3) -> tuple[bytes, str, str]:
    request = Request(
        url, headers={"User-Agent": USER_AGENT, "Accept": "text/html,application/pdf"}
    )
    last_error: Exception | None = None
    for attempt in range(attempts):
        try:
            with urlopen(request, timeout=timeout) as response:
                declared = int(response.headers.get("Content-Length", "0") or 0)
                if declared > MAX_DOWNLOAD_BYTES:
                    raise ValueError(
                        f"Source declares {declared:,} bytes; limit is {MAX_DOWNLOAD_BYTES:,}"
                    )
                payload = response.read(MAX_DOWNLOAD_BYTES + 1)
                if len(payload) > MAX_DOWNLOAD_BYTES:
                    raise ValueError(f"Source exceeds {MAX_DOWNLOAD_BYTES:,}-byte limit")
                return payload, response.headers.get_content_type(), response.geturl()
        except (HTTPError, URLError, TimeoutError) as exc:
            last_error = exc
            if attempt + 1 < attempts:
                time.sleep(2**attempt)
    assert last_error is not None
    raise last_error


def _pdf_text(payload: bytes) -> str:
    reader = PdfReader(BytesIO(payload))
    if reader.is_encrypted:
        raise ValueError("Encrypted PDF cannot be processed")
    return "\n\n".join(page.extract_text() or "" for page in reader.pages)


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
) -> SourceReceipt:
    payload, content_type, resolved_url = _download(url)
    text = extract_source_text(payload, content_type, source_format)
    if len(text) < minimum_characters:
        raise ValueError(
            f"{law_id} produced only {len(text):,} text characters; "
            f"minimum is {minimum_characters:,}"
        )
    receipt = SourceReceipt(
        law_id=law_id,
        requested_url=url,
        resolved_url=resolved_url,
        retrieved_at_utc=datetime.now(timezone.utc).isoformat(),
        content_type=content_type,
        raw_bytes=len(payload),
        raw_sha256=hashlib.sha256(payload).hexdigest(),
        text_characters=len(text),
        text_sha256=hashlib.sha256(text.encode("utf-8")).hexdigest(),
        output_path=str(output_path),
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text + "\n", encoding="utf-8")
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(json.dumps(asdict(receipt), indent=2) + "\n", encoding="utf-8")
    return receipt
