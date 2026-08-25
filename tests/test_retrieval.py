from us_ai_federalism.retrieval import normalize_text, retrieve_passages


def test_retrieval_returns_domain_window_with_passage_id() -> None:
    text = "Section 1. A deployer shall provide notice before using artificial intelligence."
    passages = retrieve_passages(text, {"consumer_notice": ["provide notice"]}, window=20)
    assert len(passages) == 1
    assert passages[0].passage_id == "P001"
    assert passages[0].domain == "consumer_notice"
    assert "provide notice" in passages[0].text


def test_nearby_hits_are_merged() -> None:
    text = "notice x notice x notice"
    passages = retrieve_passages(text, {"consumer_notice": ["notice"]}, window=10)
    assert len(passages) == 1


def test_cross_domain_overlaps_are_not_sent_twice() -> None:
    text = (
        "Section 1. A deployer shall provide notice and conduct an impact assessment "
        "before a consequential decision."
    )
    passages = retrieve_passages(
        text,
        {
            "consumer_notice": ["provide notice"],
            "impact_assessment": ["impact assessment"],
        },
        window=80,
    )
    assert len(passages) == 1
    assert passages[0].domain == "consumer_notice|impact_assessment"


def test_normalization_collapses_line_breaks_for_quote_matching() -> None:
    source = "A deployer shall\nprovide   notice\tto the consumer."
    assert normalize_text(source) == "A deployer shall provide notice to the consumer."
