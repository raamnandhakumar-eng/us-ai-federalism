from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

from .costs import estimate_cost
from .retrieval import normalize_text, render_passages, retrieve_passages
from .schema import LawCodingResponse, LawRecord, ObligationLabel, RawLawCodingResponse
from .settings import (
    CODING_MAX_OUTPUT_TOKENS,
    MODEL_PRICING,
    PROJECT_ROOT,
    PROMPT_VERSION,
    load_domains,
)

SYSTEM_PROMPT = """You are assisting a transparent empirical study of U.S. AI statutes.
Code only what the supplied primary legal text expressly supports. Do not use outside knowledge.
A positive code requires operative legal language and an exact supporting quote from the supplied
text. Do not infer a private right of action, legal preemption, or coverage from silence. Treat
findings, intent, optional guidance, and study commissions as nonbinding. When text is incomplete,
flag human review. This is structured research coding, not legal advice."""


def build_prompt(law: LawRecord, passage_text: str) -> str:
    return f"""LAW METADATA
law_id: {law.law_id}
state: {law.state}
bill: {law.bill_number}
title: {law.title}
source: {law.primary_source_url}

TASK
Identify every distinct enforceable AI-specific obligation in the supplied passages. Use only the
fixed domains in the response schema. Return positive rows only unless a passage appears relevant
but proves that the domain is absent. Strength is 1 for disclosure/procedure, 2 for assessment,
mitigation or human review, and 3 for a prohibition, individual right, mandatory human decision,
or duty backed by a specified penalty. Keep the evidence quote verbatim and under 600 characters.
Use the statutory section when visible. Set needs_human_review true for incomplete, conflicting,
amended, ambiguous, or cross-referenced text.

PRIMARY-TEXT PASSAGES
{passage_text}
"""


def request_hash(model: str, law_id: str, prompt: str) -> str:
    payload = f"{PROMPT_VERSION}\0{model}\0{law_id}\0{SYSTEM_PROMPT}\0{prompt}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _atomic_json_write(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    temporary.replace(path)


def _extract_parsed_output(message: Any) -> RawLawCodingResponse:
    for block in message.content:
        parsed = getattr(block, "parsed_output", None)
        if parsed is not None:
            return RawLawCodingResponse.model_validate(parsed)
    raise ValueError("Claude response did not contain parsed structured output")


def _exact_excerpt(text: str, limit: int) -> tuple[str, bool]:
    clean = " ".join(text.split())
    if len(clean) <= limit:
        return clean, False
    excerpt = clean[:limit]
    if " " in excerpt:
        excerpt = excerpt.rsplit(" ", 1)[0]
    return excerpt, True


def _coerce_research_schema(raw: RawLawCodingResponse) -> LawCodingResponse:
    obligations: list[ObligationLabel] = []
    adjusted_document = False
    for item in raw.obligations:
        evidence, clipped = _exact_excerpt(item.evidence_quote, 600)
        covered = item.covered
        strength = max(0, min(3, int(item.strength)))
        adjusted = clipped or strength != item.strength
        if covered and strength == 0:
            strength = 1
            adjusted = True
        if covered and not evidence:
            covered = False
            strength = 0
            adjusted = True
        if not covered and strength != 0:
            strength = 0
            adjusted = True
        notes, notes_clipped = _exact_excerpt(item.notes, 330)
        adjusted = adjusted or notes_clipped
        if adjusted:
            suffix = "API output normalized; verify during human review."
            notes = f"{notes} {suffix}".strip()
        obligations.append(
            ObligationLabel(
                domain=item.domain,
                covered=covered,
                strength=strength,
                regulated_actor=_exact_excerpt(item.regulated_actor, 120)[0],
                sector=_exact_excerpt(item.sector, 120)[0],
                effective_date=_exact_excerpt(item.effective_date, 40)[0],
                section_reference=_exact_excerpt(item.section_reference, 120)[0],
                evidence_quote=evidence,
                confidence=max(0.0, min(1.0, float(item.confidence))),
                notes=notes,
            )
        )
        adjusted_document = adjusted_document or adjusted
    document_notes, document_clipped = _exact_excerpt(raw.document_notes, 600)
    return LawCodingResponse(
        law_id=raw.law_id,
        obligations=obligations,
        document_notes=document_notes,
        needs_human_review=(raw.needs_human_review or adjusted_document or document_clipped),
    )


def _verify_quotes(result: LawCodingResponse, source_text: str) -> LawCodingResponse:
    normalized_source = normalize_text(source_text).lower()
    for obligation in result.obligations:
        if (
            obligation.covered
            and normalize_text(obligation.evidence_quote).lower() not in normalized_source
        ):
            obligation.confidence = min(obligation.confidence, 0.25)
            suffix = "Evidence quote did not match the supplied source text exactly."
            obligation.notes = f"{obligation.notes} {suffix}".strip()
            result.needs_human_review = True
    return result


class ClaudeLawCoder:
    def __init__(
        self,
        model: str,
        max_spend_usd: float,
        cache_dir: Path | None = None,
        api_key: str | None = None,
    ) -> None:
        if model not in MODEL_PRICING:
            raise ValueError(f"Pricing is not pinned for model {model}")
        self.model = model
        self.max_spend_usd = max_spend_usd
        self.cache_dir = cache_dir or PROJECT_ROOT / "data" / "cache" / "claude"
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.spent_usd = 0.0

    def _client(self) -> Any:
        if not self.api_key:
            raise RuntimeError("Set ANTHROPIC_API_KEY in your shell. Never paste it into the repo.")
        from anthropic import Anthropic

        return Anthropic(api_key=self.api_key)

    def code(self, law: LawRecord, source_text: str) -> tuple[LawCodingResponse, dict[str, Any]]:
        domains = load_domains()
        passages = retrieve_passages(source_text, domains)
        if not passages:
            result = LawCodingResponse(
                law_id=law.law_id,
                obligations=[],
                document_notes="No domain-keyword passages retrieved; human completeness review required.",
                needs_human_review=True,
            )
            return result, {"cache_hit": False, "api_called": False, "cost_usd": 0.0}

        prompt = build_prompt(law, render_passages(passages))
        key = request_hash(self.model, law.law_id, prompt)
        cache_path = self.cache_dir / f"{key}.json"
        if cache_path.exists():
            cached = json.loads(cache_path.read_text(encoding="utf-8"))
            result = LawCodingResponse.model_validate(cached["result"])
            return result, {**cached["usage"], "cache_hit": True, "api_called": False}

        preflight = estimate_cost(
            [SYSTEM_PROMPT + prompt],
            self.model,
            output_tokens_each=CODING_MAX_OUTPUT_TOKENS,
        )
        if self.spent_usd + preflight.usd > self.max_spend_usd:
            raise RuntimeError(
                f"Projected spend ${self.spent_usd + preflight.usd:.4f} exceeds "
                f"the ${self.max_spend_usd:.2f} ceiling"
            )

        client = self._client()
        message = client.messages.parse(
            model=self.model,
            max_tokens=CODING_MAX_OUTPUT_TOKENS,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
            output_format=RawLawCodingResponse,
        )
        result = _verify_quotes(
            _coerce_research_schema(_extract_parsed_output(message)), source_text
        )
        pricing = MODEL_PRICING[self.model]
        input_tokens = int(message.usage.input_tokens)
        output_tokens = int(message.usage.output_tokens)
        cost_usd = (
            input_tokens / 1_000_000 * pricing["input"]
            + output_tokens / 1_000_000 * pricing["output"]
        )
        self.spent_usd += cost_usd
        usage = {
            "model": self.model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cost_usd": round(cost_usd, 6),
            "cache_hit": False,
            "api_called": True,
            "prompt_version": PROMPT_VERSION,
            "request_hash": key,
        }
        _atomic_json_write(cache_path, {"result": result.model_dump(mode="json"), "usage": usage})
        return result, usage


def flatten_result(law: LawRecord, result: LawCodingResponse, model: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for sequence, obligation in enumerate(result.obligations, start=1):
        seed = f"{law.law_id}|{obligation.domain.value}|{sequence}|{obligation.evidence_quote}"
        coding_id = hashlib.sha256(seed.encode("utf-8")).hexdigest()[:20]
        rows.append(
            {
                "coding_id": coding_id,
                "law_id": law.law_id,
                "state": law.state,
                **obligation.model_dump(mode="json"),
                "source_url": law.primary_source_url,
                "review_status": "unreviewed",
                "coder": model,
                "prompt_version": PROMPT_VERSION,
                "document_needs_human_review": result.needs_human_review,
            }
        )
    return rows
