import argparse
import pickle

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from config import INDEX_PATH, RESULTS_DIR, ensure_dirs
from deepseek_client import generate_answer


def load_index():
    if not INDEX_PATH.exists():
        raise FileNotFoundError(
            f"Index not found: {INDEX_PATH}\n"
            "Please run: python src/build_index.py"
        )

    with INDEX_PATH.open("rb") as f:
        return pickle.load(f)


def retrieve(
    question: str,
    top_k: int = 3,
    score_threshold: float = 0.1,
):
    payload = load_index()
    vectorizer = payload["vectorizer"]
    matrix = payload["matrix"]
    chunks = payload["chunks"]

    query_vec = vectorizer.transform([question])
    scores = cosine_similarity(query_vec, matrix).flatten()
    top_indices = scores.argsort()[::-1][:top_k]
    if len(top_indices) == 0 or scores[top_indices[0]] < score_threshold:
        return []
    results = []

    rank = 1

    for idx in top_indices:
        score = float(scores[idx])

        if score < score_threshold:
            continue

        item = dict(chunks[idx])
        item["rank"] = rank
        item["score"] = score
        results.append(item)

        rank += 1

    return results


def format_sources(contexts):
    return "\n\n".join(
        (
            f"[{item['rank']}] "
            f"source={item['source']} "
            f"score={item['score']:.4f}\n"
            f"{item['text']}"
        )
        for item in contexts
    )


def build_answer(question: str, contexts, use_llm: bool = True):
    if not contexts:
        return f"""问题：{question}

知识库中没有找到相关内容，无法回答该问题。
"""

    if use_llm:
        context_text = "\n\n".join(
            item["text"]
            for item in contexts
        )

        generated_answer = generate_answer(
            question=question,
            context=context_text,
        )
    else:
        generated_answer = contexts[0]["text"]

    sources = format_sources(contexts)

    return f"""问题：{question}

基于知识库检索到的内容，参考答案如下：

{generated_answer}

参考来源：
{sources}
"""


def ask(
    question: str,
    top_k: int = 3,
    use_llm: bool = True,
):
    ensure_dirs()

    contexts = retrieve(
        question,
        top_k=top_k,
    )

    answer = build_answer(
        question,
        contexts,
        use_llm=use_llm,
    )

    result_path = RESULTS_DIR / "last_rag_answer.md"
    result_path.write_text(
        answer,
        encoding="utf-8",
    )

    rows = pd.DataFrame(contexts)
    rows.to_csv(
        RESULTS_DIR / "last_retrieval_results.csv",
        index=False,
        encoding="utf-8-sig",
    )

    return answer


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--question",
        required=True,
        help="Question to ask the RAG system",
    )

    parser.add_argument(
        "--top-k",
        type=int,
        default=3,
    )

    parser.add_argument(
        "--no-llm",
        action="store_true",
        help="Use template output instead of DeepSeek.",
    )

    args = parser.parse_args()

    answer = ask(
        question=args.question,
        top_k=args.top_k,
        use_llm=not args.no_llm,
    )

    print(answer)


if __name__ == "__main__":
    main()