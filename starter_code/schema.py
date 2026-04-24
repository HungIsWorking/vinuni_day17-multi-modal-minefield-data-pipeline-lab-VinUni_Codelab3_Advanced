"""Unified Data Contract for the Multi-Modal Minefield pipeline.

Role 1 — Lead Data Architect.

This is SCHEMA v1. A breaking migration to v2 is expected at T+60 minutes.
Keep all field names referenced through ``UnifiedDocument`` so renames stay
contained to this module.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

SCHEMA_VERSION: str = "v1"


class SourceType(str, Enum):
    """Canonical set of upstream sources supported by the pipeline."""

    PDF = "PDF"
    VIDEO = "Video"
    HTML = "HTML"
    CSV = "CSV"
    CODE = "Code"


class UnifiedDocument(BaseModel):
    """Single record stored in the Knowledge Base.

    Every processor in ``process_*.py`` must return instances of this class
    (or a list of them). Downstream quality gates and the forensic agent rely
    on the exact field names and the ``source_type`` enum values below.
    """

    model_config = ConfigDict(
        str_strip_whitespace=True,
        use_enum_values=True,
        extra="ignore",
        validate_assignment=True,
    )

    document_id: str = Field(
        ...,
        min_length=1,
        description="Globally unique id, conventionally prefixed by source (e.g. 'csv-1042').",
    )
    content: str = Field(
        ...,
        min_length=1,
        description="Cleaned, human-readable text ready for indexing.",
    )
    source_type: SourceType = Field(
        ...,
        description="Origin channel: PDF / Video / HTML / CSV / Code.",
    )
    author: Optional[str] = Field(
        default="Unknown",
        description="Author or speaker when known; 'Unknown' otherwise.",
    )
    timestamp: Optional[datetime] = Field(
        default=None,
        description="Source timestamp in ISO 8601 (UTC preferred).",
    )
    source_metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Source-specific structured fields (e.g. detected_price_vnd, table rows).",
    )

    @field_validator("document_id")
    @classmethod
    def _id_must_be_non_blank(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("document_id must be a non-empty string")
        return v.strip()

    @field_validator("content")
    @classmethod
    def _content_must_be_non_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("content must be non-empty after stripping")
        return v

    @field_validator("author")
    @classmethod
    def _default_author(cls, v: Optional[str]) -> str:
        if v is None or not str(v).strip():
            return "Unknown"
        return str(v).strip()
