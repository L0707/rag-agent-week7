from agent_demo import run_agent


def test_agent_handles_division_by_zero():
    result = run_agent("计算 1 / 0")

    assert isinstance(result, str)
    assert "失败" in result or "错误" in result
    assert "Traceback" not in result
