import argparse
import asyncio

from .workflow import run_research


def main():
    parser = argparse.ArgumentParser(description="Multi-agent Research Assistant")
    parser.add_argument("topic", nargs="*", help="Research question")
    parser.add_argument("--depth", choices=["quick", "standard", "deep"], default="standard")
    parser.add_argument("--output", default="reports/research_report.md")
    args = parser.parse_args()
    topic = " ".join(args.topic).strip() or input("Research question: ").strip()
    if not topic:
        raise SystemExit("Research question is required.")
    report = asyncio.run(run_research(topic, args.depth, args.output))
    print(report)
    print(f"\nSaved: {args.output}")


if __name__ == "__main__":
    main()
