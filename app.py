import re

import streamlit as st

from pipeline import run_research_pipeline

# ---------- Page setup ----------
st.set_page_config(page_title="Multi-Agent Research System", page_icon="🔎", layout="wide")

st.title("🔎 Multi-Agent Research System")
st.caption("Search agent → Reader agent → Writer → Critic")

# ---------- Sidebar ----------
with st.sidebar:
    st.header("How it works")
    st.markdown(
        """
1. **Search agent** finds recent information on the web
2. **Reader agent** scrapes the most relevant page
3. **Writer** drafts a structured report
4. **Critic** reviews and scores the report
"""
    )
    st.info("A full run can take 1 to 3 minutes.")

# ---------- Input ----------
topic = st.text_input(
    "Enter a research topic",
    placeholder="e.g. Impact of war on the stock market",
)

run = st.button("Run Research", type="primary")

# ---------- Run pipeline ----------
if run:
    if not topic.strip():
        st.warning("Please enter a topic first.")
    else:
        try:
            with st.spinner("Agents are working... please wait"):
                st.session_state["state"] = run_research_pipeline(topic.strip())
                st.session_state["topic"] = topic.strip()
        except Exception as e:
            st.error(f"Something went wrong: {e}")

# ---------- Show results ----------
state = st.session_state.get("state")

if state:
    st.success(f"Research complete for: {st.session_state['topic']}")

    # Pull the score (e.g. "Score: 8/10") out of the critic feedback
    feedback = state.get("feedback", "")
    match = re.search(r"Score:\s*(\d+(?:\.\d+)?)\s*/\s*10", feedback)
    if match:
        st.metric("Critic score", f"{match.group(1)}/10")

    tab_report, tab_feedback, tab_search, tab_scraped = st.tabs(
        ["📄 Final Report", "🧐 Critic Feedback", "🔍 Search Results", "🌐 Scraped Content"]
    )

    with tab_report:
        st.markdown(state.get("report", ""))
        st.download_button(
            "Download report (.md)",
            data=state.get("report", ""),
            file_name="research_report.md",
            mime="text/markdown",
        )

    with tab_feedback:
        st.markdown(feedback)

    with tab_search:
        st.text(state.get("search_results", ""))

    with tab_scraped:
        st.text(state.get("scraped_content", ""))