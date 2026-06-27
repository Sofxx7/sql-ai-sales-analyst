from __future__ import annotations

import json

import streamlit as st

from database import get_schema, run_readonly_query
from guard import UnsafeQueryError, validate_and_limit
from llm import generate_sql


st.set_page_config(page_title="Local AI Sales Analyst", page_icon="📊")
st.title("📊 Local AI Sales Analyst")
st.caption("Ask a business question. The app generates, validates, and runs read-only SQL.")

question = st.text_input(
    "Business question",
    placeholder="Which three product categories generated the most revenue?",
)

if st.button("Analyze", type="primary", disabled=not question):
    try:
        raw_answer = generate_sql(question, get_schema())
        answer = json.loads(raw_answer)
        safe_sql = validate_and_limit(answer["sql"])

        st.subheader("Generated SQL")
        st.code(safe_sql, language="sql")
        st.write(answer["explanation"])

        result = run_readonly_query(safe_sql)
        st.subheader(f"Result ({len(result)} rows)")
        st.dataframe(result, use_container_width=True)
    except (ValueError, KeyError, json.JSONDecodeError, UnsafeQueryError) as exc:
        st.error(f"The generated answer could not be used safely: {exc}")
    except Exception as exc:
        st.error(f"Unable to complete the analysis: {exc}")

with st.expander("Try these questions"):
    st.markdown(
        """
- Which three product categories generated the most revenue?
- Who are the five customers with the highest lifetime spend?
- Show monthly revenue and number of orders.
- Which products have never been ordered?
"""
    )
