from agent_demo import choose_tool


def test_choose_tool_for_explicit_calculate():
    tool_name, kwargs = choose_tool("计算 12 * 8 + 5")

    assert tool_name == "calculate"
    assert kwargs["expression"] == "12 * 8 + 5"


def test_choose_tool_for_natural_chinese_calculation():
    tool_name, kwargs = choose_tool("帮我算一下 12 * 8")

    assert tool_name == "calculate"
    assert kwargs["expression"] == "12 * 8"


def test_choose_tool_for_document_listing():
    tool_name, kwargs = choose_tool("列出知识库中的文档")

    assert tool_name == "list_documents"
    assert kwargs == {}


def test_choose_tool_defaults_to_knowledge_search():
    tool_name, kwargs = choose_tool("KiCad 的 PCB 设计流程是什么？")

    assert tool_name == "search_knowledge"
    assert kwargs["question"] == "KiCad 的 PCB 设计流程是什么？"
