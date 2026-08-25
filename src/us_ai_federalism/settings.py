from __future__ import annotations

import json
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MODEL = "claude-haiku-4-5-20251001"
DEFAULT_MAX_SPEND = 8.0
CODING_MAX_OUTPUT_TOKENS = 5_000
PROMPT_VERSION = "0.2.1"

# USD per million tokens. Verified against Anthropic's published pricing on 2026-08-25.
MODEL_PRICING = {
    "claude-haiku-4-5-20251001": {"input": 1.0, "output": 5.0},
}


def model_name() -> str:
    return os.getenv("CLAUDE_MODEL", DEFAULT_MODEL)


def max_spend() -> float:
    return float(os.getenv("MAX_API_SPEND_USD", str(DEFAULT_MAX_SPEND)))


def _domain_config(path: Path | None = None) -> dict[str, object]:
    config_path = path or PROJECT_ROOT / "config" / "policy_domains.json"
    return json.loads(config_path.read_text(encoding="utf-8"))


def load_domains(path: Path | None = None) -> dict[str, list[str]]:
    payload = _domain_config(path)
    return payload["domains"]  # type: ignore[return-value]


def load_domain_definitions(path: Path | None = None) -> dict[str, str]:
    payload = _domain_config(path)
    return payload.get("definitions", {})  # type: ignore[return-value]
