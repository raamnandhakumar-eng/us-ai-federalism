from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Passage:
    domain: str
    start: int
    end: int
    text: str


def normalize_text(text: str) -> str:
    return re.sub(r"[ \t]+", " ", text.replace("\r\n", "\n").replace("\r", "\n"))


def retrieve_passages(
    text: str,
    domains: dict[str, list[str]],
    window: int = 1800,
    max_passages_per_domain: int = 8,
) -> list[Passage]:
    """Retrieve overlapping keyword windows and merge nearby hits within each domain."""
    clean = normalize_text(text)
    lower = clean.lower()
    passages: list[Passage] = []
    for domain, terms in domains.items():
        spans: list[tuple[int, int]] = []
        for term in terms:
            for match in re.finditer(re.escape(term.lower()), lower):
                spans.append(
                    (max(0, match.start() - window), min(len(clean), match.end() + window))
                )
        merged: list[list[int]] = []
        for start, end in sorted(spans):
            if merged and start <= merged[-1][1]:
                merged[-1][1] = max(merged[-1][1], end)
            else:
                merged.append([start, end])
        for start, end in merged[:max_passages_per_domain]:
            passages.append(Passage(domain, start, end, clean[start:end]))
    return passages


def render_passages(passages: list[Passage]) -> str:
    blocks = []
    for index, passage in enumerate(passages, start=1):
        blocks.append(
            f"[PASSAGE {index} | DOMAIN_HINT={passage.domain} | CHARS={passage.start}:{passage.end}]\n"
            f"{passage.text}"
        )
    return "\n\n".join(blocks)
