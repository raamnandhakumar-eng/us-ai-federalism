from pathlib import Path

import pandas as pd

from us_ai_federalism.sources import read_manifest


def test_project_source_manifest_parses_with_transport_metadata() -> None:
    manifest = read_manifest(Path("config/source_manifest.csv"))
    assert len(manifest) == 9

    colorado = manifest.loc[manifest["law_id"] == "CO-2026-SB189"].iloc[0]
    assert colorado["amends_law_id"] == "CO-2024-SB205"
    assert colorado["mixed_effective_dates"] == "true"

    connecticut = manifest.loc[manifest["law_id"] == "CT-2023-SB1103"].iloc[0]
    assert connecticut["transport_policy"] == "official_host_tls_fallback"
    assert connecticut["expected_raw_sha256"] == (
        "2bfb035054c6399424eaba95bb7cf3abc3fdfefaa97dcb95eef9d4590a5c586a"
    )
    assert connecticut["expected_text_marker"] == "Public Act No. 23-16"
    assert connecticut["amends_law_id"] == ""
    assert connecticut["mixed_effective_dates"] == "true"

    historical_colorado = manifest.loc[manifest["law_id"] == "CO-2024-SB205"].iloc[0]
    assert historical_colorado["inactive_from_date"] == "2026-05-14"
    assert historical_colorado["superseded_by_law_id"] == "CO-2026-SB189"


def test_census_population_universe_is_complete_and_reconciles() -> None:
    states = pd.read_csv("config/state_universe.csv")
    assert len(states) == 51
    assert states["state"].nunique() == 51
    assert states["population"].notna().all()
    assert (states["population"] > 0).all()
    assert set(states["weight_source_year"]) == {2025}
    assert int(states["population"].sum()) == 341_784_857