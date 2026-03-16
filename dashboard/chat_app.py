import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
from ai.sql_agent import generate_sql, run_query


st.set_page_config(page_title="AI Job Market Intelligence", layout="wide")

st.title("AI Job Market Intelligence Assistant")

st.markdown("Explore AI and tech job trends across the world.")

# -------------------------------
# Sidebar Filters
# -------------------------------

st.sidebar.header("Filters")

region = st.sidebar.selectbox(
    "Region",
    ["Global", "North America", "Europe", "Asia"]
)

# Top skills from database
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

question = st.sidebar.text_input(
    "Ask AI",
    placeholder="ex: top skills for ML engineers"
)

# -------------------------------
# Main Logic
# -------------------------------

sql = None

# Skill based search
if selected_skill != "None":

    sql = f"""
    SELECT
        j.job_title,
        j.company_name,
        j.company_location,
        j.country,
        j.region,
        j.job_url
    FROM jobs j
    JOIN job_skills js ON j.job_id = js.job_id
    JOIN skills s ON js.skill_id = s.skill_id
    WHERE LOWER(s.skill_name) = LOWER('{selected_skill}')
    """

    if region != "Global":
        sql += f" AND j.region = '{region}'"

    sql += " LIMIT 200"


# AI question search
elif question:

    full_question = f"""
    {question}

    IMPORTANT:
    Filter region = '{region}'
    """

    sql = generate_sql(full_question)


# -------------------------------
# Show Results
# -------------------------------

if sql:

    rows = run_query(sql)

    if not rows:
        st.warning("No results found.")
    else:

        df = pd.DataFrame(rows)

        df = df.rename(columns={
            "job_title": "Job Title",
            "company_name": "Company",
            "company_location": "Location",
            "job_url": "Apply"
        })

        drop_cols = [
            "job_id",
            "job_description",
            "experience_level",
            "employment_type",
            "remote_ratio",
            "company_size",
            "date_posted",
            "source"
        ]

        df = df.drop(columns=[c for c in drop_cols if c in df.columns], errors="ignore")
        df = df.dropna(axis=1, how="all")

        # clickable links
        if "Apply" in df.columns:
            df["Apply"] = df["Apply"].apply(
                lambda x: f'<a href="{x}" target="_blank">Apply</a>' if pd.notnull(x) else ""
            )

        st.subheader("Job Listings")

        st.write(
            df.to_html(escape=False, index=False),
            unsafe_allow_html=True
        )