import argparse

from build_index import build_index
from config import INDEX_PATH
from tools import TOOLS


def choose_tool(question: str):
    lowered = question.lower()

    if "列出" in question or "list" in lowered or "documents" in lowered:
        return "list_documents", {}

    calculate_markers = [
        "计算",
        "算一下",
        "算出",
        "calculate",
    ]

    for marker in calculate_markers:
        if marker in lowered:
            expression = lowered.replace(marker, "").strip()

            if marker in {"算一下", "算出"}:
                expression = expression.replace("帮我", "").strip()

            return "calculate", {
                "expression": expression or "1 + 1"
            }

    return "search_knowledge", {"question": question}


def run_agent(question: str):
    if not INDEX_PATH.exists():
        print("Index not found. Building index first...")
        build_index()

    tool_name, kwargs = choose_tool(question)
    tool = TOOLS[tool_name]

    print(f"User question: {question}")
    print(f"Chosen tool: {tool_name}")
    print(f"Tool description: {tool['description']}")
    print("-" * 60)

    try:
        result = tool["function"](**kwargs)
    except Exception as exc:
        return f"工具执行失败：{exc}"

    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--question", required=True)
    args = parser.parse_args()

    result = run_agent(args.question)
    print(result)


if __name__ == "__main__":
    main()

