import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd

from ai.sql_agent import run_query
from ai.web_agent import ask_web_agent


st.set_page_config(page_title="AI Job Intelligence", layout="wide")

st.title("AI Job Intelligence")
st.markdown("Discover AI job opportunities and explore careers in artificial intelligence.")

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.header("Filters")

region = st.sidebar.selectbox(
    "Region",
    ["Global", "North America", "Europe", "Asia"]
)

# ==============================
# SKILL DROPDOWN
# ==============================

skill_sql = """
SELECT skill_name
FROM skills
ORDER BY skill_name
LIMIT 50
"""

skills = run_query(skill_sql)

skill_list = ["None"] + [s[0] for s in skills]

selected_skill = st.sidebar.selectbox(
    "Search by Skill",
    skill_list
)

st.sidebar.markdown("---")

# ==============================
# AI TECH ASSISTANT
# ==============================

st.sidebar.header("AI Tech Assistant")

tech_question = st.sidebar.text_input(
    "Ask anything about tech",
    placeholder="ex: how to become an AI engineer"
)

ask_button = st.sidebar.button("Ask")

# =====================================================
# FEATURED JOBS + LOCATIONS
# =====================================================

col1, col2 = st.columns([2,1])

# =====================================================
# FEATURED AI JOBS
# =====================================================

with col1:

    st.subheader("🔥 Featured AI Job Opportunities")

    sql = """
    SELECT j.job_title, j.company_name, j.company_location, j.job_url
    FROM jobs j
    """

    if selected_skill != "None":
        sql += """
        JOIN job_skills js ON j.job_id = js.job_id
        JOIN skills s ON js.skill_id = s.skill_id
        """

    sql += """
    WHERE j.job_title ~* '(machine learning|ai|data|ml|scientist|architect|engineer)'
    """

    if selected_skill != "None":
        sql += f" AND LOWER(s.skill_name) = LOWER('{selected_skill}')"

    if region != "Global":
        sql += f" AND j.region = '{region}'"

    sql += " LIMIT 8"

    rows = run_query(sql)

    if rows:

        df = pd.DataFrame(rows)

        df.columns = ["Job Title", "Company", "Location", "Apply"]

        df["Apply"] = df["Apply"].apply(
            lambda x: f'<a href="{x}" target="_blank">Apply</a>' if pd.notnull(x) else ""
        )

        st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)

# =====================================================
# TOP HIRING LOCATIONS
# =====================================================

with col2:

    st.subheader("🌍 Top AI Hiring Locations")

    loc_sql = """
    SELECT country, COUNT(*) as jobs
    FROM jobs
    WHERE job_title ~* '(machine learning|ai|data|ml|scientist|architect|engineer)'
    AND country IS NOT NULL
    GROUP BY country
    ORDER BY jobs DESC
    LIMIT 4
    """

    rows = run_query(loc_sql)

    if rows:

        df = pd.DataFrame(rows, columns=["Country", "Jobs"])

        st.bar_chart(df.set_index("Country"))

st.markdown("---")

# =====================================================
# AI CAREER ASSISTANT
# =====================================================

st.subheader("💬 AI Career Assistant")

career_question = st.text_input(
    "Want to explore a career in AI? Ask anything here.",
    placeholder="ex: what skills are required for a machine learning engineer"
)

if career_question:

    with st.spinner("Thinking..."):

        answer, sources = ask_web_agent(career_question, [])

    st.markdown(answer)

    st.markdown("### Sources")

    for s in sources[:5]:
        st.markdown(f"- {s}")

# =====================================================
# SIDEBAR AI ASSISTANT OUTPUT
# =====================================================

if ask_button and tech_question:

    st.markdown("---")
    st.subheader("🤖 AI Tech Assistant")

    with st.spinner("Searching the web..."):

        answer, sources = ask_web_agent(tech_question, [])

    st.markdown(answer)

    st.markdown("### Sources")

    for s in sources[:5]:
        st.markdown(f"- {s}")