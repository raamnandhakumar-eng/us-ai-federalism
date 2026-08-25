from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Passage:
    passage_id: str
    domain: str
    start: int
    end: int
    text: str


def normalize_text(text: str) -> str:
    """Normalize all whitespace so statutory quotes remain comparable across PDF/HTML extraction."""
    return re.sub(r"\s+", " ", text.replace("\r\n", "\n").replace("\r", "\n")).strip()


def _overlap_ratio(left: tuple[int, int], right: tuple[int, int]) -> float:
    start = max(left[0], right[0])
    end = min(left[1], right[1])
    overlap = max(0, end - start)
    denominator = max(1, min(left[1] - left[0], right[1] - right[0]))
    return overlap / denominator


def retrieve_passages(
    text: str,
    domains: dict[str, list[str]],
    window: int = 1500,
    max_passages: int = 14,
    max_passage_chars: int = 5000,
    max_total_chars: int = 32000,
) -> list[Passage]:
    """Retrieve keyword windows once, globally deduplicating overlaps across domains.

    The old implementation built a separate passage set for every policy domain. The same statutory
    section could therefore be sent to the model many times under different domain hints. This
    version merges substantially overlapping windows across all domains, preserves the combined
    hints, and caps total retrieved text for predictable cost.
    """
    clean = normalize_text(text)
    lower = clean.lower()
    candidates: list[tuple[int, int, str]] = []

    for domain, terms in domains.items():
        for term in terms:
            needle = term.lower()
            for match in re.finditer(re.escape(needle), lower):
                candidates.append(
                    (
                        max(0, match.start() - window),
                        min(len(clean), match.end() + window),
                        domain,
                    )
                )

    if not candidates:
        return []

    merged: list[dict[str, object]] = []
    for start, end, domain in sorted(candidates, key=lambda item: (item[0], item[1], item[2])):
        if merged:
            previous = merged[-1]
            previous_span = (int(previous["start"]), int(previous["end"]))
            candidate_span = (start, end)
            merged_end = max(previous_span[1], end)
            merged_start = min(previous_span[0], start)
            if (
                _overlap_ratio(previous_span, candidate_span) >= 0.50
                and merged_end - merged_start <= max_passage_chars
            ):
                previous["start"] = merged_start
                previous["end"] = merged_end
                hints = set(previous["domains"])
                hints.add(domain)
                previous["domains"] = hints
                continue
        merged.append({"start": start, "end": end, "domains": {domain}})

    selected: list[Passage] = []
    total_chars = 0
    for item in merged:
        if len(selected) >= max_passages:
            break
        start = int(item["start"])
        end = int(item["end"])
        length = end - start
        if selected and total_chars + length > max_total_chars:
            break
        hints = "|".join(sorted(str(value) for value in item["domains"]))
        selected.append(
            Passage(
                passage_id=f"P{len(selected) + 1:03d}",
                domain=hints,
                start=start,
                end=end,
                text=clean[start:end],
            )
        )
        total_chars += length

    return selected


def render_passages(passages: list[Passage]) -> str:
    blocks = []
    for passage in passages:
        blocks.append(
            f"[{passage.passage_id} | DOMAIN_HINTS={passage.domain} | "
            f"CHARS={passage.start}:{passage.end}]\n{passage.text}"
        )
    return "\n\n".join(blocks)
