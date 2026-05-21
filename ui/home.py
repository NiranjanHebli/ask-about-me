import time
import streamlit as st
from .theme import _c, render_theme_toggle
from .utils import inject_autocomplete_js


def _get_google_logo_html(base_class="logo-large"):
    """Returns 'Ask About Me' with individual Google colors per letter, plus a subtitle."""
    c = _c()
    if base_class == "logo-large":
        return f"""
        <div style="text-align: center; margin-top: 8vh; margin-bottom: 32px;">
            <div class="{base_class}" style="margin-bottom: 4px; margin-top: 0;">
                <span style="color:#4285F4;">A</span><span style="color:#EA4335;">s</span><span style="color:#FBBC05;">k</span>
                &nbsp;
                <span style="color:#34A853;">A</span><span style="color:#4285F4;">b</span><span style="color:#EA4335;">o</span><span style="color:#FBBC05;">u</span><span style="color:#34A853;">t</span>
                &nbsp;
                <span style="color:#4285F4;">M</span><span style="color:#EA4335;">e</span>
            </div>
            <div style="font-size: 16px; font-weight: 600; color: {c['text_muted']}; letter-spacing: 0.5px; font-family: 'Inter', sans-serif;">Niranjan Hebli</div>
        </div>
        """
    else:
        return f"""
        <div style="display: flex; align-items: baseline; gap: 12px; height: 100%;">
            <div class="{base_class}" style="margin-bottom: 0;">
                <span style="color:#4285F4;">A</span><span style="color:#EA4335;">s</span><span style="color:#FBBC05;">k</span>
                &nbsp;
                <span style="color:#34A853;">A</span><span style="color:#4285F4;">b</span><span style="color:#EA4335;">o</span><span style="color:#FBBC05;">u</span><span style="color:#34A853;">t</span>
                &nbsp;
                <span style="color:#4285F4;">M</span><span style="color:#EA4335;">e</span>
            </div>
            <div style="font-size: 13px; font-weight: 600; color: {c['text_muted']}; letter-spacing: 0.5px; font-family: 'Inter', sans-serif;">Niranjan Hebli</div>
        </div>
        """


def render_search_home(click_suggestion_callback):
    # Theme toggle will be floated to top-right via JS injected in render_theme_toggle
    render_theme_toggle(key="home_theme")

    st.markdown(_get_google_logo_html("logo-large"), unsafe_allow_html=True)

    _, center_col, _ = st.columns([1.5, 5, 1.5])
    with center_col:
        with st.form("search_form", border=False):
            query_input = st.text_input(
                "",
                placeholder="What is Niranjan's tech stack?",
                label_visibility="collapsed",
                key="home_search",
            )
            st.write("")
            b1, b2, b3 = st.columns([1, 2, 1])
            with b2:
                if (
                    st.form_submit_button("Start Search", use_container_width=True)
                    and query_input.strip()
                ):
                    click_suggestion_callback(query_input.strip())
                    st.rerun()

        inject_autocomplete_js()

        st.markdown(
            '<div class="sugg-label">Try a quick search:</div>', unsafe_allow_html=True
        )
        s1, s2, s3, s4, s5 = st.columns(5)

        chips = [
            (s1, "Tech Stack", "What is Niranjan's tech stack?"),
            (s2, "Experience", "Tell me about Niranjan's experience"),
            (s3, "Projects", "What projects has Niranjan developed?"),
            (s4, "Education", "Tell me about Niranjan's education"),
            (s5, "Contact", "How can I contact Niranjan?"),
        ]

        for col, label, query in chips:
            with col:
                if st.button(label, use_container_width=True, key=f"chip_{label}"):
                    click_suggestion_callback(query)
                    st.rerun()
