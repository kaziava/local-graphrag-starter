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

```
PDF → [PyMuPDF parse] → pages
    → [LLMGraphTransformer · Ollama] → entities & relations
    → [Neo4j] → knowledge graph
    → [GraphCypherQAChain] → NL question → Cypher → exact answer
```

## Quickstart

Prerequisites: Docker, Python 3.10+, [Ollama](https://ollama.com) with a pulled model
(`ollama pull llama3.1:8b`).

```bash
# 1. Start Neo4j
docker compose up -d

# 2. Install dependencies
pip install -r requirements.txt
cp .env.example .env

# 3. Build the graph from your PDF
python main.py ingest data/report.pdf

# 4. Ask
python main.py ask "What was Apple's revenue in Q3 2024?"
```

Explore the graph in Neo4j Browser: http://localhost:7474 (`neo4j` / `password`)

## Benchmarks (MacBook Pro M2, 16 GB RAM)

| Step | Time |
|---|---|
| Parse 50-page PDF | ~45 s |
| Load graph into Neo4j | ~10 s |
| Answer a question | 3–5 s |
| **Cost per query** | **$0** |

Same volume through GPT-4 API: **$15–20**.

## Limitations

- Local 8B models are weaker than frontier LLMs on complex reasoning
- 16+ GB RAM recommended
- Complex tables may require parser tuning

## Go deeper

📢 Why naive chunking fails on financial tables, the Microsoft GraphRAG research
digest, hybrid search + reranker setups and production tweaks — all broken down
in my Telegram channel: **[@llmops_engineering](https://t.me/llmops_engineering)** ·
[engineers' chat](https://t.me/llmops_engineering1)

## Roadmap

- [ ] Table-aware parsing (Markdown/JSON wrapping via LlamaParse)
- [ ] Hybrid retrieval: Cypher + BM25 + reranker
- [ ] FalkorDB / Memgraph backends

## License

MIT
