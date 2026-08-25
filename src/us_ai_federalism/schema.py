from __future__ import annotations

from datetime import date
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class ReviewStatus(str, Enum):
    unreviewed = "unreviewed"
    verified = "verified"
    revised = "revised"
    rejected = "rejected"
    unresolved = "unresolved"


class ObligationDomain(str, Enum):
    impact_assessment = "impact_assessment"
    risk_management = "risk_management"
    model_evaluation = "model_evaluation"
    human_oversight = "human_oversight"
    consumer_notice = "consumer_notice"
    public_transparency = "public_transparency"
    explanation_appeal = "explanation_appeal"
    antidiscrimination = "antidiscrimination"
    incident_reporting = "incident_reporting"
    frontier_safety = "frontier_safety"
    harmful_use_restriction = "harmful_use_restriction"
    child_safety = "child_safety"
    health_restriction = "health_restriction"
    synthetic_content = "synthetic_content"
    whistleblower_protection = "whistleblower_protection"
    infrastructure = "infrastructure"
    government_use = "government_use"
    enforcement_authority = "enforcement_authority"
    private_right = "private_right"
    penalty = "penalty"
    exemption = "exemption"


class LawRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    law_id: str = Field(min_length=3, max_length=80)
    state: str = Field(pattern=r"^[A-Z]{2}$")
    bill_number: str
    title: str
    enactment_date: date | None = None
    effective_date: date | None = None
    status: str
    primary_source_url: str
    local_text_path: str
    source_format: str
    amends_law_id: str | None = None
    collection_status: str
    notes: str = ""


class ObligationLabel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    domain: ObligationDomain
    covered: bool
    strength: int = Field(ge=0, le=3)
    regulated_actor: str = Field(max_length=120)
    sector: str = Field(max_length=120)
    effective_date: str = Field(default="", max_length=40)
    section_reference: str = Field(max_length=120)
    evidence_passage: str = Field(default="", max_length=16)
    evidence_quote: str = Field(max_length=600)
    evidence_verified: bool = False
    confidence: float = Field(ge=0, le=1)
    notes: str = Field(default="", max_length=400)

    @model_validator(mode="after")
    def enforce_positive_evidence(self) -> ObligationLabel:
        if self.covered and (
            self.strength == 0
            or not self.evidence_quote.strip()
            or not self.evidence_passage.strip()
        ):
            raise ValueError(
                "Positive codes require strength > 0, an evidence passage, and an evidence quote"
            )
        if not self.covered and self.strength != 0:
            raise ValueError("Negative codes must have strength 0")
        return self

    @field_validator("evidence_quote")
    @classmethod
    def normalize_quote(cls, value: str) -> str:
        return " ".join(value.split())


class LawCodingResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    law_id: str
    obligations: list[ObligationLabel]
    document_notes: str = Field(default="", max_length=600)
    needs_human_review: bool


class RawObligationLabel(BaseModel):
    """Permissive API shape; converted to the strict research schema after receipt."""

    model_config = ConfigDict(extra="forbid")

    domain: ObligationDomain
    covered: bool
    strength: int
    regulated_actor: str
    sector: str
    effective_date: str = ""
    section_reference: str
    evidence_passage: str = ""
    evidence_quote: str
    confidence: float
    notes: str = ""


class RawLawCodingResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    law_id: str
    obligations: list[RawObligationLabel]
    document_notes: str = ""
    needs_human_review: bool
