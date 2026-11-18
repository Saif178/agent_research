import asyncio
import streamlit as st

from src.researcher.workflow import run_research

st.set_page_config(page_title="Researcher Agent v2", page_icon="🔬", layout="wide")
st.title("🔬 Multi-Agent Research Assistant")
st.caption("Chemical engineering · Sustainability · Environmental science · Industrial AI")

with st.sidebar:
    st.subheader("Research settings")
    depth = st.selectbox("Research depth", ["quick", "standard", "deep"], index=1)
    st.info("The agent coordinates literature, domain specialists, evidence auditing and report writing.")

topic = st.text_area(
    "Research question",
    placeholder="Example: Compare adsorption and membrane technologies for removing heavy metals from industrial wastewater, including LCA and scale-up constraints.",
    height=130,
)
if st.button("Start research", type="primary", disabled=not topic.strip()):
    with st.spinner("Research team is working. This may take several minutes..."):
        try:
            report = asyncio.run(run_research(topic.strip(), depth))
            st.session_state["research_report"] = report
        except Exception as exc:
            st.error(f"Research failed: {type(exc).__name__}: {exc}")

if st.session_state.get("research_report"):
    st.markdown("---")
    st.markdown(st.session_state["research_report"])
    st.download_button(
        "Download Markdown report",
        data=st.session_state["research_report"],
        file_name="research_report.md",
        mime="text/markdown",
    )
