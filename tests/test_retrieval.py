from us_ai_federalism.retrieval import retrieve_passages


def test_retrieval_returns_domain_window() -> None:
    text = "Section 1. A deployer shall provide notice before using artificial intelligence."
    passages = retrieve_passages(text, {"consumer_notice": ["provide notice"]}, window=20)
    assert len(passages) == 1
    assert passages[0].domain == "consumer_notice"
    assert "provide notice" in passages[0].text


def test_nearby_hits_are_merged() -> None:
    text = "notice x notice x notice"
    passages = retrieve_passages(text, {"consumer_notice": ["notice"]}, window=10)
    assert len(passages) == 1
