import json

from tools import TOOLS


def describe_tools():
    tool_descriptions = []
    for name, spec in TOOLS.items():
        tool_descriptions.append({
            "name": name,
            "description": spec["description"],
        })
    return tool_descriptions


def call_tool(tool_name: str, arguments: dict):
    if tool_name not in TOOLS:
        raise ValueError(f"Unknown tool: {tool_name}")
    return TOOLS[tool_name]["function"](**arguments)


def main():
    print("MCP-like tool discovery response:")
    print(json.dumps(describe_tools(), ensure_ascii=False, indent=2))

    print("\nMCP-like tool call request:")
    request = {
        "tool_name": "list_documents",
        "arguments": {},
    }
    print(json.dumps(request, ensure_ascii=False, indent=2))

    print("\nMCP-like tool call response:")
    result = call_tool(request["tool_name"], request["arguments"])
    print(result)


if __name__ == "__main__":
    main()

