# RAG-Agent Knowledge Assistant

## 1. 项目简介

本项目是一个基于 RAG（Retrieval-Augmented Generation，检索增强生成）和 Agent 工具调用的本地知识库智能助手。

项目最初来源于 Week 4 的 RAG + Agent 实践，在 Week 7 中进一步进行了功能修复、测试补充和工程化整理，使其从一个课程 Demo 改进为可以独立运行、测试和展示的最终项目。

系统目前支持：

- 加载本地 Markdown 知识库文档；
- 使用 TF-IDF 建立文本检索索引；
- 根据用户问题进行相似度检索；
- 使用相似度阈值过滤无关检索结果；
- 对知识库之外的问题进行拒答；
- 将检索结果作为上下文交给 DeepSeek 生成回答；
- 使用 Agent 根据用户问题选择不同工具；
- 支持知识检索、文档列表和数学计算工具；
- 支持常见中文自然语言计算表达；
- 对工具执行异常进行统一处理；
- 使用自动化测试验证核心功能。

---

## 2. 系统架构

系统的主要工作流程如下：

```text
                        User Query
                            |
                            v
                     +-------------+
                     | Agent Router|
                     +------+------+
                            |
              +-------------+-------------+
              |             |             |
              v             v             v
      list_documents    calculate    search_knowledge
                                          |
                                          v
                                     RAG Retriever
                                          |
                                   TF-IDF + Cosine
                                          |
                                          v
                                  Local Knowledge Base
                                          |
                                          v
                                      DeepSeek
                                          |
                                          v
                                       Answer
```

其中：

- `Agent Router` 根据用户输入选择工具；
- `list_documents` 用于查看本地知识库文件；
- `calculate` 用于执行简单数学表达式；
- `search_knowledge` 进入 RAG 问答流程；
- RAG 模块使用 TF-IDF 和余弦相似度进行知识检索；
- DeepSeek 根据检索到的本地知识生成最终回答。

---

## 3. 项目结构

```text
rag-agent/
├── data/
│   └── docs/
│       ├── kicad_basics.md
│       ├── pcb_design_flow.md
│       └── rag_agent_notes.md
│
├── docs/
│   ├── feature_checklist.md
│   └── setup.md
│
├── results/
│   ├── last_rag_answer.md
│   └── last_retrieval_results.csv
│
├── src/
│   ├── __init__.py
│   ├── agent_demo.py
│   ├── build_index.py
│   ├── config.py
│   ├── deepseek_client.py
│   ├── document_loader.py
│   ├── mcp_like_demo.py
│   ├── rag_ask.py
│   └── tools.py
│
├── tests/
│   ├── test_agent_errors.py
│   ├── test_agent_routing.py
│   └── test_rag_retrieval.py
│
├── vector_store/
│   ├── chunks.csv
│   └── rag_index.pkl
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

## 4. 环境要求

本项目当前验证环境：

- Python 3.12.4
- macOS
- DeepSeek API
- OpenAI-compatible Python SDK

创建虚拟环境：

```bash
python -m venv .venv
source .venv/bin/activate
```

安装依赖：

```bash
python -m pip install -U pip
python -m pip install -r requirements.txt
```

详细安装说明见：

```text
docs/setup.md
```

---

## 5. DeepSeek API 配置

在项目根目录创建 `.env`：

```text
DEEPSEEK_API_KEY=your_api_key
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-v4-flash
```

`.env` 已加入 `.gitignore`，不要将真实 API Key 提交到 Git 仓库。

---

## 6. 构建知识库索引

执行：

```bash
python src/build_index.py
```

当前示例知识库包含 3 个文档。

成功运行后会生成：

```text
vector_store/rag_index.pkl
vector_store/chunks.csv
```

---

## 7. RAG 问答

### 7.1 不调用大模型

可以只测试检索部分：

```bash
python src/rag_ask.py \
  --question "KiCad 的 PCB 设计流程是什么？" \
  --no-llm
```

### 7.2 使用 DeepSeek 生成回答

```bash
python src/rag_ask.py \
  --question "KiCad 的 PCB 设计流程是什么？"
```

系统首先从本地知识库检索相关内容，然后将检索结果作为上下文发送给 DeepSeek。

如果没有找到达到相似度阈值的知识，系统会拒绝回答，而不是直接使用模型自身知识生成答案。

---

## 8. Agent 工具调用

Agent 当前包含三个工具：

### 8.1 知识库搜索

```bash
python src/agent_demo.py \
  --question "KiCad 的 PCB 设计流程是什么？"
```

Agent 会选择：

```text
search_knowledge
```

### 8.2 查看知识库文档

```bash
python src/agent_demo.py \
  --question "列出知识库中的文档"
```

Agent 会选择：

```text
list_documents
```

### 8.3 数学计算

```bash
python src/agent_demo.py \
  --question "帮我算一下 12 * 8"
```

Agent 会选择：

```text
calculate
```

并返回：

```text
96
```

---

## 9. Week 7 主要改进

### 9.1 RAG 检索结果逐条阈值过滤

原始实现只判断最高相似度结果是否超过阈值。

当最高结果满足要求后，即使后续文档相似度为 `0.0000`，仍然会被加入 RAG 上下文。

例如原始 KiCad 查询曾返回：

```text
kicad_basics.md       0.6863
pcb_design_flow.md    0.3623
rag_agent_notes.md    0.0000
```

Week 7 中增加逐条阈值检查后，低于阈值的文档不再进入上下文。

修改后只保留：

```text
kicad_basics.md       0.6863
pcb_design_flow.md    0.3623
```

这样可以减少无关上下文对生成结果的干扰。

### 9.2 改进 Agent 中文自然语言路由

原始 Agent 主要识别：

```text
计算
calculate
```

因此：

```text
帮我算一下 12 * 8
```

会被错误路由到知识检索工具。

Week 7 中扩展了轻量级中文计算表达规则，使“算一下”“算出”等常见表达能够正确进入计算工具。

### 9.3 增加工具异常处理

原始版本执行：

```text
计算 1 / 0
```

会直接输出 Python traceback，并抛出：

```text
ZeroDivisionError
```

现在 Agent 会捕获工具执行异常，并返回可读的错误信息，而不会直接暴露内部 traceback。

### 9.4 改善环境可复现性

项目从原有 Python 环境迁移到新的独立虚拟环境后，发现 SOCKS 代理相关依赖缺失，导致 DeepSeek 客户端无法初始化。

错误表现为：

```text
ImportError: Using SOCKS proxy, but the 'socksio' package is not installed.
```

因此在 `requirements.txt` 中补充：

```text
httpx[socks]
```

使项目在新的虚拟环境中也能够正常安装和运行。

---

## 10. 自动化测试

当前项目包含 3 组测试：

```text
tests/test_rag_retrieval.py
tests/test_agent_routing.py
tests/test_agent_errors.py
```

分别验证：

- RAG 相似度阈值过滤；
- 无关问题拒答；
- Agent 工具路由；
- 中文自然计算表达；
- 默认知识检索路由；
- 文档列表路由；
- 工具异常处理。

运行：

```bash
python -m pytest -v
```

当前最终版本测试结果：

```text
7 passed
```

---

## 11. 当前限制

当前项目仍然是一个轻量级教学与演示系统，主要限制包括：

1. 知识库规模较小，目前只有 3 个示例文档；
2. 使用 TF-IDF 而不是语义向量 Embedding；
3. Agent 路由仍然主要采用规则判断；
4. 当前没有 Web 图形界面；
5. 尚未实现复杂的多轮 Agent 推理；
6. MCP-like 部分主要用于展示工具协议思想，并非完整 MCP Server。

---

## 12. 后续优化方向

后续可以进一步：

- 使用 Embedding 模型替代 TF-IDF；
- 增加更大规模的 PDF、Markdown 和 TXT 知识库；
- 增加文档分块策略和召回质量评测；
- 使用 LLM 或分类模型进行 Agent 工具路由；
- 增加更多安全工具和参数验证；
- 增加 Web 或桌面交互界面；
- 接入标准 MCP Server；
- 建立更完整的 RAG 评测数据集与自动化指标。

---

## 13. 项目定位

本项目的重点不是重新实现一个大型 RAG 框架，而是在已有课程 Demo 的基础上，通过真实问题定位、自动化测试、最小功能修复和工程化整理，使项目达到：

- 可以运行；
- 可以测试；
- 可以解释；
- 可以演示；
- 可以继续迭代。

的最终交付状态。
