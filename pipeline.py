"""Local GraphRAG pipeline: PDF -> Neo4j knowledge graph -> Cypher QA."""
import os

import fitz
from dotenv import load_dotenv
from langchain.chains import GraphCypherQAChain
from langchain_community.graphs import Neo4jGraph
from langchain_core.documents import Document
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_ollama import OllamaLLM

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")


def get_llm(temperature: float = 0.0) -> OllamaLLM:
    return OllamaLLM(model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL, temperature=temperature)


def get_graph() -> Neo4jGraph:
    return Neo4jGraph(url=NEO4J_URI, username=NEO4J_USER, password=NEO4J_PASSWORD)


def load_pdf(path: str) -> list[Document]:
    """Parse PDF into page-level documents. Fully local, no cloud parsers."""
    docs = []
    with fitz.open(path) as pdf:
        for i, page in enumerate(pdf):
            text = page.get_text("text").strip()
            if text:
                docs.append(Document(page_content=text, metadata={"page": i + 1}))
    return docs


def ingest(pdf_path: str) -> Neo4jGraph:
    """PDF -> entities & relations -> Neo4j knowledge graph."""
    graph = get_graph()
    docs = load_pdf(pdf_path)
    transformer = LLMGraphTransformer(llm=get_llm())
    graph_docs = transformer.convert_to_graph_documents(docs)
    graph.add_graph_documents(graph_docs, baseEntityLabel=True, include_source=True)
    return graph


def ask(graph: Neo4jGraph, question: str) -> str:
    """NL question -> Cypher -> exact answer from the graph. Zero hallucinated numbers."""
    chain = GraphCypherQAChain.from_llm(
        get_llm(), graph=graph, verbose=True, allow_dangerous_requests=True
    )
    return chain.invoke({"query": question})["result"]
