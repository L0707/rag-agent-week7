# Feature Checklist

## Core RAG Features

- [x] Load local Markdown knowledge-base documents
- [x] Build and save a searchable RAG index
- [x] Retrieve relevant documents from a user question
- [x] Filter retrieval results using a similarity threshold
- [x] Reject questions with no sufficiently relevant knowledge
- [x] Generate answers using DeepSeek and retrieved context
- [x] Save the latest RAG answer and retrieval results

## Agent Features

- [x] Route document-list requests to `list_documents`
- [x] Route calculation requests to `calculate`
- [x] Route general knowledge questions to `search_knowledge`
- [x] Support natural Chinese calculation expressions such as “帮我算一下”
- [x] Handle tool execution errors without exposing Python traceback

## Engineering and Verification

- [x] Run in an isolated Python virtual environment
- [x] Record all required Python dependencies
- [x] Support SOCKS proxy environments through `httpx[socks]`
- [x] Protect `.env` and API credentials with `.gitignore`
- [x] Provide automated tests
- [x] All current automated tests pass
