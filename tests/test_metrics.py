import pandas as pd
import pytest

from us_ai_federalism.metrics import apply_scenario, prepare_state_domain, simulate_all


def sample_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    codings = pd.DataFrame(
        [
            {
                "state": "AA",
                "domain": "consumer_notice",
                "covered": True,
                "strength": 1,
                "review_status": "verified",
            },
            {
                "state": "AA",
                "domain": "child_safety",
                "covered": True,
                "strength": 3,
                "review_status": "verified",
            },
            {
                "state": "BB",
                "domain": "consumer_notice",
                "covered": True,
                "strength": 2,
                "review_status": "verified",
            },
            {
                "state": "BB",
                "domain": "child_safety",
                "covered": True,
                "strength": 1,
                "review_status": "unreviewed",
            },
        ]
    )
    states = pd.DataFrame([{"state": "AA", "weight": 1}, {"state": "BB", "weight": 3}])
    return codings, states


def test_unreviewed_rows_are_excluded() -> None:
    codings, states = sample_data()
    grid = prepare_state_domain(codings, states)
    value = grid.query("state == 'BB' and domain == 'child_safety'")["strength"].item()
    assert value == 0


def test_weighted_coverage() -> None:
    codings, states = sample_data()
    estimates = simulate_all(prepare_state_domain(codings, states))
    current_child = estimates.query("scenario == 'current' and domain == 'child_safety'").iloc[0]
    assert current_child["coverage"] == pytest.approx(0.25)


def test_eo_carveout_preserves_child_safety_only() -> None:
    codings, states = sample_data()
    grid = prepare_state_domain(codings, states)
    result = apply_scenario(grid, "eo14365_carveouts")
    assert result.query("domain == 'child_safety'")["strength"].sum() == 3
    assert result.query("domain == 'consumer_notice'")["strength"].sum() == 0


def test_floor_closes_binary_coverage_gap() -> None:
    codings, states = sample_data()
    estimates = simulate_all(prepare_state_domain(codings, states), floor_strength=1)
    floor = estimates.query("scenario == 'federal_floor'")
    assert (floor["coverage"] == 1).all()
