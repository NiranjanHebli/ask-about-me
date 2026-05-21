import streamlit as st
from .theme import _c


def render_knowledge_graph():
    c = _c()

    def _get_resume_pdf() -> bytes:
        try:
            from pdf_generator import generate_resume_pdf

            return generate_resume_pdf()
        except ImportError:
            return b""

    st.markdown(
        f"""
    <div class="glass-card profile-widget">
        <div class="profile-avatar">N</div>
        <div class="profile-title">Niranjan Hebli</div>
        <div class="profile-subtitle">Generative AI Developer</div>
        <div class="profile-desc">
            Software engineer specialising in Generative AI, LLM orchestration, and RAG pipelines. Builds multi-agent applications with LangGraph and LangChain.
        </div>
        <div class="profile-detail"><b>Education:</b> B.Tech in CSE, NIT Goa (2024)</div>
        <div class="profile-detail"><b>Location:</b> India</div>
        <div class="profile-detail"><b>Tech Stack:</b> Python, LangGraph, FastAPI, SQL, JS</div>
        <div class="profile-detail"><b>Focus:</b> Agentic Systems, RAG, Backend</div>
        <div class="profile-detail" style="margin-top: 16px;">
            <b>Profiles:</b><br/>
            <a href="https://www.linkedin.com/in/niranjan-hebli-333211211/" target="_blank" style="color: {{c['accent']}}; text-decoration: none; font-weight: 600;">LinkedIn</a> &nbsp;|&nbsp; 
            <a href="https://leetcode.com/u/NiranjanHebli/" target="_blank" style="color: {{c['accent']}}; text-decoration: none; font-weight: 600;">LeetCode</a> &nbsp;|&nbsp; 
            <a href="https://github.com/NiranjanHebli" target="_blank" style="color: {{c['accent']}}; text-decoration: none; font-weight: 600;">GitHub</a>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    resume_bytes = _get_resume_pdf()
    if resume_bytes:
        st.write("")
        st.download_button(
            label="Download Resume (PDF)",
            data=resume_bytes,
            file_name="Niranjan_Hebli_Resume.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
