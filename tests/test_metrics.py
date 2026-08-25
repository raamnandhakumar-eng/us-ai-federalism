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


def test_fixed_domain_universe_keeps_zero_adoption_domain() -> None:
    codings, states = sample_data()
    domains = ["consumer_notice", "child_safety", "model_evaluation"]
    grid = prepare_state_domain(codings, states, domains=domains)
    missing_domain = grid.query("domain == 'model_evaluation'")
    assert len(missing_domain) == 2
    assert missing_domain["strength"].sum() == 0


def test_domain_specific_floor_only_changes_selected_domains() -> None:
    codings, states = sample_data()
    domains = ["consumer_notice", "child_safety", "model_evaluation"]
    grid = prepare_state_domain(codings, states, domains=domains)
    floor = apply_scenario(
        grid,
        "federal_floor",
        floor_strengths={"consumer_notice": 2, "model_evaluation": 1},
    )
    assert (floor.query("domain == 'consumer_notice'")["strength"] >= 2).all()
    assert (floor.query("domain == 'model_evaluation'")["strength"] == 1).all()
    assert floor.query("state == 'BB' and domain == 'child_safety'")["strength"].item() == 0


def test_binary_heterogeneity_is_zero_at_full_coverage() -> None:
    codings, states = sample_data()
    estimates = simulate_all(prepare_state_domain(codings, states), floor_strength=1)
    floor = estimates.query("scenario == 'federal_floor'")
    assert (floor["binary_heterogeneity"] == 0).all()


def test_snapshot_excludes_future_and_inactive_obligations() -> None:
    codings = pd.DataFrame(
        [
            {
                "law_id": "AA-future",
                "state": "AA",
                "domain": "consumer_notice",
                "covered": True,
                "strength": 1,
                "review_status": "verified",
                "effective_date": "2027-01-01",
                "law_effective_date": "2026-05-14",
                "inactive_from_date": "",
                "law_inactive_from_date": "",
                "mixed_effective_dates": True,
            },
            {
                "law_id": "AA-expired",
                "state": "AA",
                "domain": "child_safety",
                "covered": True,
                "strength": 3,
                "review_status": "verified",
                "effective_date": "2026-01-01",
                "law_effective_date": "2026-01-01",
                "inactive_from_date": "",
                "law_inactive_from_date": "2026-07-01",
                "mixed_effective_dates": False,
            },
            {
                "law_id": "AA-active",
                "state": "AA",
                "domain": "model_evaluation",
                "covered": True,
                "strength": 2,
                "review_status": "verified",
                "effective_date": "2026-01-01",
                "law_effective_date": "2026-01-01",
                "inactive_from_date": "",
                "law_inactive_from_date": "",
                "mixed_effective_dates": False,
            },
        ]
    )
    states = pd.DataFrame([{"state": "AA", "weight": 1}])
    domains = ["consumer_notice", "child_safety", "model_evaluation"]
    grid = prepare_state_domain(
        codings,
        states,
        domains=domains,
        analysis_date="2026-08-25",
    )
    assert grid.query("domain == 'consumer_notice'")["strength"].item() == 0
    assert grid.query("domain == 'child_safety'")["strength"].item() == 0
    assert grid.query("domain == 'model_evaluation'")["strength"].item() == 2


def test_mixed_effective_date_law_requires_row_date() -> None:
    codings = pd.DataFrame(
        [
            {
                "law_id": "AA-mixed",
                "state": "AA",
                "domain": "consumer_notice",
                "covered": True,
                "strength": 1,
                "review_status": "verified",
                "effective_date": "",
                "law_effective_date": "2026-05-14",
                "law_inactive_from_date": "",
                "mixed_effective_dates": True,
            }
        ]
    )
    states = pd.DataFrame([{"state": "AA", "weight": 1}])
    with pytest.raises(ValueError, match="obligation-level effective_date"):
        prepare_state_domain(codings, states, analysis_date="2026-08-25")


def test_single_effective_date_law_uses_manifest_fallback() -> None:
    codings = pd.DataFrame(
        [
            {
                "law_id": "AA-simple",
                "state": "AA",
                "domain": "consumer_notice",
                "covered": True,
                "strength": 1,
                "review_status": "verified",
                "effective_date": "",
                "law_effective_date": "2026-01-01",
                "law_inactive_from_date": "",
                "mixed_effective_dates": False,
            }
        ]
    )
    states = pd.DataFrame([{"state": "AA", "weight": 1}])
    grid = prepare_state_domain(codings, states, analysis_date="2026-08-25")
    assert grid.query("domain == 'consumer_notice'")["strength"].item() == 1
