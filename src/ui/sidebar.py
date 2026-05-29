import streamlit as st

from .theme import _c


def render_knowledge_graph():
    c = _c()

    def _get_resume_pdf() -> bytes:
        import os
        pdf_path = os.path.join("data", "Niranjan_Hebli.pdf")
        if os.path.exists(pdf_path):
            try:
                with open(pdf_path, "rb") as f:
                    return f.read()
            except Exception:
                pass
        try:
            from pdf_generator import generate_resume_pdf

            return generate_resume_pdf()
        except ImportError:
            return b""

    import base64
    import os
    img_path = os.path.join("assets", "niranjan_hebli.png")
    avatar_html = '<div class="profile-avatar">N</div>'
    if os.path.exists(img_path):
        try:
            with open(img_path, "rb") as image_file:
                img_base64 = base64.b64encode(image_file.read()).decode('utf-8')
                avatar_html = f'<img class="profile-avatar" src="data:image/png;base64,{img_base64}" style="object-fit: cover;" />'
        except Exception:
            pass

    st.markdown(
        f"""
    <div class="glass-card profile-widget">
        {avatar_html}
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
            <a href="https://www.linkedin.com/in/niranjan-hebli-333211211/" target="_blank" style="color: {c['accent']}; text-decoration: none; font-weight: 600;">LinkedIn</a> &nbsp;|&nbsp; 
            <a href="https://leetcode.com/u/NiranjanHebli/" target="_blank" style="color: {c['accent']}; text-decoration: none; font-weight: 600;">LeetCode</a> &nbsp;|&nbsp; 
            <a href="https://github.com/NiranjanHebli" target="_blank" style="color: {c['accent']}; text-decoration: none; font-weight: 600;">GitHub</a>
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
