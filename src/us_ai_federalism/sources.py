from __future__ import annotations

import hashlib
from pathlib import Path

import pandas as pd

from .schema import LawRecord
from .settings import PROJECT_ROOT

REQUIRED_MANIFEST_COLUMNS = set(LawRecord.model_fields)
OPTIONAL_MANIFEST_FIELDS = {
    "enactment_date",
    "effective_date",
    "amends_law_id",
    "inactive_from_date",
    "superseded_by_law_id",
}


def read_manifest(path: str | Path) -> pd.DataFrame:
    manifest_path = Path(path)
    frame = pd.read_csv(manifest_path, dtype=str, keep_default_na=False)
    missing = REQUIRED_MANIFEST_COLUMNS.difference(frame.columns)
    if missing:
        raise ValueError(f"Manifest missing columns: {sorted(missing)}")
    if frame["law_id"].duplicated().any():
        duplicates = frame.loc[frame["law_id"].duplicated(), "law_id"].tolist()
        raise ValueError(f"Duplicate law_id values: {duplicates}")
    for row in frame.to_dict(orient="records"):
        cleaned = {
            key: (None if key in OPTIONAL_MANIFEST_FIELDS and not value else value)
            for key, value in row.items()
        }
        LawRecord.model_validate(cleaned)
    return frame


def resolve_text_path(path: str, root: Path = PROJECT_ROOT) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else root / candidate


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def validate_sources(frame: pd.DataFrame, root: Path = PROJECT_ROOT) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for row in frame.to_dict(orient="records"):
        path = resolve_text_path(row["local_text_path"], root)
        exists = path.is_file()
        rows.append(
            {
                "law_id": row["law_id"],
                "state": row["state"],
                "text_exists": exists,
                "bytes": path.stat().st_size if exists else 0,
                "sha256": file_sha256(path) if exists else "",
                "path": str(path),
            }
        )
    return pd.DataFrame(rows)
