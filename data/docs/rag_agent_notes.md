# RAG and Agent Notes

RAG 是 Retrieval-Augmented Generation 的缩写，意思是检索增强生成。

一个基础 RAG 系统通常包含：

1. 文档加载：读取 Markdown、TXT、PDF 等资料。
2. 文本切分：把长文档切成较小 chunk。
3. 向量化或索引：把 chunk 转成可检索表示。
4. 检索：根据用户问题找出最相关的 chunk。
5. 生成回答：把检索结果作为上下文，生成答案。

Agent 是能根据任务选择工具并执行动作的程序。一个简单 Agent 可以包含：

- 工具列表。
- 工具描述。
- 决策逻辑。
- 工具调用。
- 最终回答。

MCP 是 Model Context Protocol 的缩写，它强调用标准协议把模型和外部工具连接起来。MCP 的核心思想不是某一个具体工具，而是让模型能够以统一方式发现工具、理解工具参数、调用工具并获得结果。

