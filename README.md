# local-graphrag-starter

**PDF → knowledge graph → precise answers. 100% local, $0 per query.**

Minimal production-oriented GraphRAG stack: PyMuPDF + LangChain + Neo4j + Ollama.
No cloud APIs, no data leaving your machine.

> 📢 Companion repo of the Telegram channel [@llmops_engineering](https://t.me/llmops_engineering) —
> hardcore LLMOps breakdowns, benchmarks and production war stories.

## Why GraphRAG

Classic RAG hallucinates on tables and numbers: naive chunking destroys table
structure, and cosine similarity doesn't understand rows and columns.
GraphRAG queries an **entity graph** instead of embeddings — exact numbers, zero guesses.

## Architecture
