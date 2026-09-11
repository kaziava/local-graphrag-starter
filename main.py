"""CLI entrypoint.

Usage:
    python -m app.main ingest data/report.pdf
    python -m app.main ask "What was Apple's revenue in Q3 2024?"
"""
import argparse

from .pipeline import ask, get_graph, ingest


def main() -> None:
    parser = argparse.ArgumentParser(description="Local GraphRAG starter")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_ingest = sub.add_parser("ingest", help="Parse PDF and build the knowledge graph")
    p_ingest.add_argument("pdf", help="Path to a PDF file")

    p_ask = sub.add_parser("ask", help="Ask a question over the graph")
    p_ask.add_argument("question")

    args = parser.parse_args()

    if args.cmd == "ingest":
        ingest(args.pdf)
        print("✅ Graph built. Explore it at http://localhost:7474 (neo4j/password)")
    else:
        print(ask(get_graph(), args.question))


if __name__ == "__main__":
    main()
