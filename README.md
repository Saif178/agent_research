# Researcher Agent v2 — Multi-Agent Research Assistant

A multi-agent technical research assistant built with the **OpenAI Agents SDK**. It routes research
questions to domain specialists, searches scholarly metadata and the web, retrieves passages from
a local PDF library, audits evidence, and writes a structured technical report.

## Specialist team

- **Research Manager** — orchestrates specialist handoffs and synthesis.
- **Literature Research Specialist** — OpenAlex discovery, Crossref DOI metadata, local PDF retrieval.
- **Chemical Engineering Specialist** — reaction engineering, separations, adsorption, membranes,
  catalysis, process systems, scale-up and process safety.
- **Sustainability and LCA Specialist** — ISO-aligned LCA concepts, carbon accounting, circularity,
  EPD and industrial decarbonization.
- **Environmental Science Specialist** — water, wastewater, air, soil, remediation, waste and monitoring.
- **Industrial AI Specialist** — predictive maintenance, process analytics, optimization, digital twins,
  model validation and deployment.
- **Evidence and Citation Auditor** — claim/source alignment, metadata checks and overclaim detection.
- **Research Report Writer** — final structured report.

## Tools and data sources

- OpenAI `WebSearchTool` for current web research.
- OpenAlex Works API for scholarly work discovery.
- Crossref REST API for DOI metadata validation.
- ChromaDB local vector collection for retrieved passages from user-supplied PDFs.
- Streamlit interface and command-line interface.

## Setup (Windows PowerShell)

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` and provide your OpenAI API key. Set `OPENAI_MODEL` to a model available to your API project.

## Run the CLI

From the project root:

```powershell
python -m src.researcher.cli --depth standard --output reports/wastewater_review.md "Compare adsorption and membrane technologies for heavy-metal removal from industrial wastewater"
```

More examples:

```powershell
python -m src.researcher.cli --depth deep "Life-cycle assessment of green hydrogen production pathways in India"
python -m src.researcher.cli --depth standard "Predictive maintenance for rotating equipment using multivariate time-series data"
python -m src.researcher.cli --depth quick "Recent advances in MOF-based CO2 capture"
```

## Run the Streamlit UI

```powershell
streamlit run app.py
```

## Index your own PDF papers

Place PDFs in a folder, then:

```powershell
python -m src.researcher.ingest ./papers
```

Or index one PDF:

```powershell
python -m src.researcher.ingest ./papers/example_paper.pdf
```

The extracted text is chunked and stored in `./data/chroma`. Scanned/image-only PDFs may need OCR
before ingestion. Local retrieval is supplementary; the agent should still cite and verify the
original paper. Keep copyrighted PDFs in accordance with your institutional/library license.

## Example workflow

1. Ask a focused technical question.
2. Research Manager selects the relevant specialists.
3. Literature specialist searches OpenAlex and local indexed PDFs.
4. Domain specialists assess the topic from their disciplines.
5. Evidence auditor reviews citation quality and unsupported claims.
6. Report writer produces a Markdown report.

## Output structure

- Executive Summary
- Research Question and Scope
- Method and Search Strategy
- Specialist Findings
- Evidence Synthesis
- Technical and Sustainability Trade-offs
- Evidence Gaps and Limitations
- Conclusions
- Recommendations / Future Work
- References

## Important limitations

- This is an AI-assisted rapid research workflow, not a systematic review or PRISMA-compliant
  evidence synthesis.
- OpenAlex and Crossref provide bibliographic metadata; metadata is not proof of a paper's findings.
- Web search may not access paywalled full text.
- PDF text extraction does not perform OCR on scanned documents.
- Citation auditing is an aid, not a guarantee. Verify source pages, DOI, methods, units and claims
  before academic, regulatory, engineering or investment use.
- Do not use generated outputs as a substitute for process-safety review, regulatory advice or
  qualified engineering sign-off.

## Project layout

```text
researcher_agent_v2/
├── app.py
├── requirements.txt
├── .env.example
├── README.md
├── src/
│   └── researcher/
│       ├── agents.py
│       ├── config.py
│       ├── tools.py
│       ├── workflow.py
│       ├── ingest.py
│       └── cli.py
├── data/
└── reports/
```
