import time
import streamlit as st
from .home import _get_google_logo_html
from .theme import render_theme_toggle
from .utils import inject_autocomplete_js


def render_results_header(reset_search_callback):
    # Theme toggle will be floated to top-right via JS injected in render_theme_toggle
    render_theme_toggle(key="res_theme")

    col1, col2, col3 = st.columns([3, 6.5, 1.5])

    with col1:
        st.markdown(_get_google_logo_html("logo-compact"), unsafe_allow_html=True)

    with col2:
        val = st.text_input(
            "",
            value=st.session_state.search_query,
            label_visibility="collapsed",
            key="res_search",
        )
        if val != st.session_state.search_query:
            with st.spinner("Searching..."):
                time.sleep(0.3)
                st.session_state.search_query = val
            st.rerun()
        inject_autocomplete_js()

    with col3:
        st.button("Back Home", on_click=reset_search_callback, use_container_width=True)


def render_search_stats(elapsed_time: float):
    st.markdown(
        f"<div class='search-stats'>Found 4 related results ({elapsed_time} seconds)</div>",
        unsafe_allow_html=True,
    )


def _stream_typed_text(text: str, placeholder):
    words = text.split(" ")
    displayed = ""
    for i, word in enumerate(words):
        displayed += word + " "
        if i % 3 == 0 or i == len(words) - 1:
            placeholder.markdown(displayed.strip())
            time.sleep(0.015)


def render_featured_snippet(ans_content: str, animate: bool = True):
    if animate:
        ph = st.empty()
        _stream_typed_text(ans_content, ph)
    else:
        st.markdown(ans_content)


def render_organic_results():
    results = [
        {
            "site": "LinkedIn",
            "title": "Niranjan Hebli — Generative AI Developer",
            "url": "https://www.linkedin.com/in/niranjan-hebli-333211211/",
            "snippet": "Software engineer specialising in Generative AI, LLM orchestration, and RAG pipelines.",
        },
        {
            "site": "GitHub",
            "title": "NiranjanHebli (Niranjan Hebli) · GitHub",
            "url": "https://github.com/NiranjanHebli",
            "snippet": "Explore open-source projects, agentic workflows, and machine learning repositories.",
        },
        {
            "site": "LeetCode",
            "title": "NiranjanHebli - LeetCode Profile",
            "url": "https://leetcode.com/u/NiranjanHebli/",
            "snippet": "View coding challenge progress, algorithm practice, and problem-solving statistics.",
        },
        {
            "site": "CodeChef",
            "title": "niranjan_hebli | CodeChef User Profile",
            "url": "https://www.codechef.com/users/niranjan_hebli",
            "snippet": "Competitive programming profile showcasing contest ratings and algorithmic problem-solving skills.",
        },
        {
            "site": "Google Skills",
            "title": "Niranjan Hebli - Google Skill Boost Profile",
            "url": "https://www.skills.google/public_profiles/068568ff-9859-4969-9af7-3000b7ca1f74",
            "snippet": "Google Cloud certifications, skill badges, and completed learning paths.",
        },
    ]
    for r in results:
        st.markdown(
            f"""
        <div class="glass-card result-card">
            <div class="r-site">{r['site']}</div>
            <a href="{r['url']}" class="r-title" target="_blank">{r['title']}</a>
            <p class="r-snippet">{r['snippet']}</p>
        </div>
        """,
            unsafe_allow_html=True,
        )


def render_project_showcase():
    projects = [
        {
            "title": "Agentic Q&A System",
            "desc": "Multi-agent retrieval system using LangGraph with dynamic supervisor routing and self-validation loops.",
            "tags": ["LangGraph", "Python", "RAG", "Azure"],
            "link": "https://github.com/NiranjanHebli/agentic-qna-system",
        },
        {
            "title": "NCERT Class IX Retrieval",
            "desc": "Advanced retrieval and question-answering system utilizing semantic chunking and metadata filtering.",
            "tags": ["Python", "RAG", "ChromaDB", "LangChain"],
            "link": "https://github.com/NiranjanHebli/ncert-class-ix-retrieval-system",
        },
        {
            "title": "Churn Prediction AI",
            "desc": "Machine learning pipeline that processes customer behavioral data and predicts churn probability.",
            "tags": ["Python", "scikit-learn", "XGBoost"],
            "link": "https://github.com/NiranjanHebli/churn-prediction-ai",
        },
    ]
    cards = (
        '<div class="section-label">Featured Projects</div><div class="projects-grid">'
    )
    for p in projects:
        tags = "".join(f'<span class="pc-tag">{t}</span>' for t in p["tags"])
        cards += f"""
        <div class="glass-card project-card">
          <a class="pc-title" href="{p['link']}" target="_blank">{p['title']}</a>
          <p class="pc-desc">{p['desc']}</p>
          <div class="pc-tags">{tags}</div>
        </div>"""
    cards += "</div>"
    st.markdown(cards, unsafe_allow_html=True)
