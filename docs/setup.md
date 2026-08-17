# Setup and Running Guide

## 1. Requirements

- Python 3.12 or compatible Python 3 version
- DeepSeek API key

## 2. Create a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate
```

## 3. Install Dependencies

```bash
python -m pip install -U pip
python -m pip install -r requirements.txt
```

## 4. Configure DeepSeek API

Create a `.env` file in the project root:

```text
DEEPSEEK_API_KEY=your_api_key
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-v4-flash
```

Do not commit `.env` to Git.

## 5. Build the RAG Index

```bash
python src/build_index.py
```

## 6. Ask the RAG System

Without LLM generation:

```bash
python src/rag_ask.py \
  --question "KiCad 的 PCB 设计流程是什么？" \
  --no-llm
```

With DeepSeek:

```bash
python src/rag_ask.py \
  --question "KiCad 的 PCB 设计流程是什么？"
```

## 7. Run the Agent

Knowledge-base search:

```bash
python src/agent_demo.py \
  --question "KiCad 的 PCB 设计流程是什么？"
```

List documents:

```bash
python src/agent_demo.py \
  --question "列出知识库中的文档"
```

Calculator:

```bash
python src/agent_demo.py \
  --question "帮我算一下 12 * 8"
```

## 8. Run Automated Tests

```bash
python -m pytest -v
```

The current final-project baseline contains 7 automated tests.
