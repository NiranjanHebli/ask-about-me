import streamlit as st


def render_ai_overview_skeleton():
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(
            "<div class='glass-card ai-overview-wrap' style='opacity: 0.6;'>✨ Synthesizing AI overview...</div>",
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            "<div class='glass-card chat-widget-wrap' style='opacity: 0.6;'><div class='chat-header'>Loading Agent...</div><div class='chat-body'></div></div>",
            unsafe_allow_html=True,
        )


def render_ai_overview_and_chat(query: str, answer_text: str):
    """Renders the AI Overview and the Chat Widget side-by-side."""
    col1, col2 = st.columns([2, 1])

    with col1:
        import re

        sentences = re.split(r"(?<=[.!?])\s+", answer_text.strip())
        blurb = " ".join(sentences[:3]) if sentences else answer_text[:280]
        if len(blurb) > 320:
            blurb = blurb[:317].rstrip() + "…"

        st.markdown(
            f"""
        <div class="glass-card ai-overview-wrap">
          <div style="font-weight: 700; font-size: 15px; margin-bottom: 14px; display: flex; align-items: center; gap: 8px;">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color:var(--accent);"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
            AI Overview
          </div>
          <div style="font-size: 15px; line-height: 1.7;">
            <p style="margin:0;">{{blurb}}</p>
          </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        render_chat_widget()


def render_chat_widget():
    """Renders a static representation of the chat widget for the UI."""
    st.markdown(
        f"""
    <div class="glass-card chat-widget-wrap">
        <div class="chat-header">
            <span>🤖 Niranjan Resume Agent</span>
            <span style="font-size: 11px; opacity: 0.8; font-weight: 400;">Ask About Me</span>
        </div>
        <div class="chat-body">
            <div class="chat-msg-agent">
                Hi! I'm Niranjan's resume agent. Ask me anything about his experience, skills, or projects.
            </div>
            <div class="chat-msg-user">
                niranjan skill
            </div>
            <div class="chat-msg-agent">
                Niranjan Hebli has the following skills and expertise:<br/><br/>
                <b>Technical Skills:</b><br/>
                • Python, LangGraph, FastAPI, SQL, JS<br/>
                • Generative AI, LLM orchestration, RAG pipelines<br/>
            </div>
        </div>
        <div class="chat-input-area">
            <div style="display: flex; gap: 8px;">
                <input type="text" placeholder="niranjan skill" style="flex-grow: 1; padding: 8px 12px; border-radius: 20px; border: 1px solid var(--glass-border); background: var(--glass-bg); color: var(--text); font-family: inherit; font-size: 13px;" disabled>
                <button style="padding: 8px 16px; border-radius: 20px; border: none; background: var(--accent); color: white; font-weight: 600; font-size: 13px; cursor: not-allowed;" disabled>Send →</button>
            </div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )
