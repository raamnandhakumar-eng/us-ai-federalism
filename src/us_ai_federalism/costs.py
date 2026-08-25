from __future__ import annotations

from dataclasses import dataclass

from .settings import MODEL_PRICING


@dataclass(frozen=True)
class CostEstimate:
    input_tokens: int
    output_tokens: int
    usd: float
    batch: bool


def approximate_tokens(text: str) -> int:
    # Conservative planning approximation. API usage fields replace this after a live call.
    return max(1, (len(text) + 3) // 4)


def estimate_cost(
    input_texts: list[str],
    model: str,
    output_tokens_each: int = 1800,
    batch: bool = False,
) -> CostEstimate:
    if model not in MODEL_PRICING:
        raise ValueError(f"No pinned pricing for {model}; update MODEL_PRICING before spending")
    input_tokens = sum(approximate_tokens(text) for text in input_texts)
    output_tokens = output_tokens_each * len(input_texts)
    rate = MODEL_PRICING[model]
    multiplier = 0.5 if batch else 1.0
    usd = multiplier * (
        input_tokens / 1_000_000 * rate["input"] + output_tokens / 1_000_000 * rate["output"]
    )
    return CostEstimate(input_tokens, output_tokens, round(usd, 6), batch)
