import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
)


MODEL = os.getenv(
    "DEEPSEEK_MODEL",
    "deepseek-v4-flash"
)


def generate_answer(question: str, context: str) -> str:
    """
    Generate answer using DeepSeek
    with retrieved RAG context.
    """

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "你是一个知识助手。"
                    "请严格根据提供的知识库内容回答问题，"
                    "不要编造不存在的信息。"
                ),
            },
            {
                "role": "user",
                "content": (
                    f"问题：{question}\n\n"
                    f"知识库内容：\n{context}"
                ),
            },
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content