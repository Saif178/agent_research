from __future__ import annotations

from datetime import datetime
from pathlib import Path

from agents import Runner

from .agents import research_manager


DEPTH_GUIDANCE = {
    "quick": "Rapid scoping review: prioritize the most relevant sources and concise findings.",
    "standard": "Balanced technical review: cover core literature, methods, trade-offs and gaps.",
    "deep": "Deep research review: broaden source coverage, compare methods and conflicting evidence, "
            "examine limitations and research gaps in detail. Do not misrepresent this as systematic review.",
}


async def run_research(topic: str, depth: str = "standard", output: str | None = None) -> str:
    if depth not in DEPTH_GUIDANCE:
        raise ValueError(f"Unsupported depth: {depth}")

    prompt = f"""
Research question:
{topic}

Review depth:
{depth} — {DEPTH_GUIDANCE[depth]}

Workflow requirements:
1. Identify the relevant specialist domains and explain the scope.
2. Retrieve scholarly records and current authoritative web sources.
3. Have relevant specialists analyze the topic; include literature review and citation audit.
4. Synthesize agreements, disagreements, trade-offs and evidence gaps.
5. Produce a technical report with numbered references and usable source URLs/DOIs.
6. Clearly mark unverified claims and metadata-only sources.
7. Include a short reproducibility/search-method note describing source types and limitations.

Today's date: {datetime.now().date().isoformat()}
"""
    result = await Runner.run(research_manager, prompt)
    report = str(result.final_output)

    if output:
        path = Path(output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(report, encoding="utf-8")
    return report
