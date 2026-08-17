import ast
import operator
from pathlib import Path

from config import DOCS_DIR
from rag_ask import ask


def list_documents():
    files = sorted(
        path.relative_to(DOCS_DIR).as_posix()
        for path in DOCS_DIR.rglob("*")
        if path.is_file() and path.suffix.lower() in {".md", ".txt", ".pdf"}
    )
    return "\n".join(files)


def search_knowledge(question: str):
    return ask(question, top_k=3)


_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}


def _eval_expr(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPERATORS:
        return _ALLOWED_OPERATORS[type(node.op)](_eval_expr(node.left), _eval_expr(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_OPERATORS:
        return _ALLOWED_OPERATORS[type(node.op)](_eval_expr(node.operand))
    raise ValueError("Only simple numeric expressions are allowed.")


def calculate(expression: str):
    tree = ast.parse(expression, mode="eval")
    return str(_eval_expr(tree.body))


TOOLS = {
    "list_documents": {
        "description": "List all documents in the local knowledge base.",
        "function": list_documents,
    },
    "search_knowledge": {
        "description": "Search the local RAG knowledge base and return an answer.",
        "function": search_knowledge,
    },
    "calculate": {
        "description": "Evaluate a simple numeric expression.",
        "function": calculate,
    },
}

