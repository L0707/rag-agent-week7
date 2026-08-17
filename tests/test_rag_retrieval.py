from rag_ask import retrieve


def test_retrieve_filters_results_below_threshold():
    results = retrieve(
        "KiCad 的 PCB 设计流程是什么？",
        top_k=3,
        score_threshold=0.1,
    )

    assert results
    assert all(item["score"] >= 0.1 for item in results)
    assert len(results) == 2


def test_retrieve_returns_empty_for_unrelated_question():
    results = retrieve(
        "法国的首都是哪里？",
        top_k=3,
        score_threshold=0.1,
    )

    assert results == []
