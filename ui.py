import random
import streamlit as st

def inject_custom_css():
    """Injects custom CSS styling for the Google-like search engine interface."""
    st.markdown(
        """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        .stApp {
            font-family: 'Roboto', Arial, sans-serif;
        }

        .google-logo {
            font-family: 'Outfit', sans-serif;
            font-size: 76px;
            font-weight: 700;
            letter-spacing: -3px;
            text-align: center;
            margin-top: 40px;
            margin-bottom: 24px;
            user-select: none;
        }

        .result-logo {
            font-family: 'Outfit', sans-serif;
            font-size: 28px;
            font-weight: 700;
            letter-spacing: -1.5px;
            user-select: none;
        }

        .result-cite {
            font-size: 13px;
            color: var(--text-color);
            opacity: 0.7;
            margin-bottom: 2px;
        }

        .result-title {
            font-size: 19px;
            color: #3b82f6;
            font-weight: 500;
            text-decoration: none;
        }
        .result-title:hover {
            text-decoration: underline;
        }

        .result-snippet {
            font-size: 14px;
            color: var(--text-color);
            opacity: 0.8;
            line-height: 1.5;
            margin-top: 4px;
            margin-bottom: 20px;
        }

        .badge-container {
            display: flex;
            gap: 8px;
            margin-top: 10px;
        }

        .social-badge {
            flex: 1;
            padding: 8px;
            border: 1px solid var(--border-color, #3c4043);
            border-radius: 6px;
            text-align: center;
            font-size: 12px;
            text-decoration: none;
            color: var(--text-color);
            background-color: var(--secondary-background-color);
            transition: background-color 0.2s ease;
        }

        .social-badge:hover {
            background-color: var(--hover-color, #3c4043);
            text-decoration: none;
            color: var(--text-color);
        }

        .search-stats {
            font-size: 13px;
            color: var(--text-color);
            opacity: 0.65;
            margin-bottom: 12px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def render_search_home(click_suggestion_callback):
    """Renders the Google-like search engine homepage."""
    st.write("")
    st.write("")

    st.markdown(
        """
        <div class="google-logo" style="margin-top: 50px; margin-bottom: 5px;">
            <span style="color: #4285F4;">A</span><span style="color: #EA4335;">s</span><span style="color: #FBBC05;">k</span>
            <span style="color: #4285F4;">A</span><span style="color: #EA4335;">b</span><span style="color: #FBBC05;">o</span><span style="color: #4285F4;">u</span><span style="color: #34A853;">t</span>
            <span style="color: #EA4335;">M</span><span style="color: #4285F4;">e</span>
        </div>
        <div style="text-align: center; font-size: 18px; color: var(--text-color); opacity: 0.8; margin-bottom: 30px; font-weight: 500; font-family: 'Outfit', sans-serif;">
            About Niranjan Hebli
        </div>
        """,
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns([1.5, 3.5, 1.5])
    with c2:
        query_input = st.text_input(
            "",
            placeholder="Ask anything about Niranjan's experience or skills...",
            label_visibility="collapsed",
            key="input_search_box"
        )

        st.write("")
        b_col1, b_col2, b_col3, b_col4 = st.columns([1, 1.5, 1.5, 1])
        with b_col2:
            search_button = st.button("Search About Me", use_container_width=True)
        with b_col3:
            lucky_button = st.button("I'm Feeling Lucky", use_container_width=True)

        if search_button and query_input.strip():
            st.session_state.search_query = query_input
            st.session_state.search_clicked = True
            st.rerun()

        if query_input.strip() and not st.session_state.search_clicked:
            st.session_state.search_query = query_input
            st.session_state.search_clicked = True
            st.rerun()

        if lucky_button:
            lucky_options = [
                "What is Niranjan's tech stack?",
                "Tell me about Niranjan's experience",
                "What projects has Niranjan developed?",
                "How can I contact Niranjan?"
            ]
            st.session_state.search_query = random.choice(lucky_options)
            st.session_state.search_clicked = True
            st.rerun()

        st.write("")
        st.write("")
        st.markdown("<p style='text-align: center; color: var(--text-color); opacity: 0.65; font-size: 14px;'>Try searching or clicking these recommendations:</p>", unsafe_allow_html=True)

        s1, s2, s3, s4 = st.columns(4)
        with s1:
            st.button("Tech Stack", on_click=click_suggestion_callback, args=("What is Niranjan's tech stack?",), use_container_width=True)
        with s2:
            st.button("Experience", on_click=click_suggestion_callback, args=("Tell me about Niranjan's experience",), use_container_width=True)
        with s3:
            st.button("Projects", on_click=click_suggestion_callback, args=("What projects has Niranjan developed?",), use_container_width=True)
        with s4:
            st.button("Contact Info", on_click=click_suggestion_callback, args=("How can I contact Niranjan?",), use_container_width=True)

def render_results_header(reset_search_callback):
    """Renders the top results bar layout, including query box and navigation back to home."""
    h_col1, h_col2, h_col3 = st.columns([1.5, 5, 2.5])
    with h_col1:
        st.markdown(
            """
            <div class="result-logo" style="margin-top: 5px; font-size: 22px;">
                <span style="color: #4285F4;">A</span><span style="color: #EA4335;">s</span><span style="color: #FBBC05;">k</span>
                <span style="color: #4285F4;">A</span><span style="color: #EA4335;">b</span><span style="color: #FBBC05;">o</span><span style="color: #4285F4;">u</span><span style="color: #34A853;">t</span>
                <span style="color: #EA4335;">M</span><span style="color: #4285F4;">e</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    with h_col2:
        result_input = st.text_input(
            "",
            value=st.session_state.search_query,
            label_visibility="collapsed",
            key="input_results_box"
        )
        if result_input != st.session_state.search_query:
            st.session_state.search_query = result_input
            st.rerun()
    with h_col3:
        st.button("🏠 Search Home", on_click=reset_search_callback, use_container_width=True)

    st.markdown("<hr style='margin-top: 12px; margin-bottom: 20px; border-color: var(--border-color, #3c4043); opacity: 0.5;'>", unsafe_allow_html=True)

def render_search_stats(elapsed_time):
    """Displays calculation latency info."""
    st.markdown(f"<div class='search-stats'>About 1 result ({elapsed_time} seconds)</div>", unsafe_allow_html=True)

def render_featured_snippet(ans_content):
    """Renders the AI generated answers block in the primary section."""
    with st.container(border=True):
        st.markdown(
            """
            <div style="font-size:12px; text-transform:uppercase; color: var(--text-color); opacity: 0.6; font-weight:700; margin-bottom:8px;">
                <span>Featured snippet from the web</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(ans_content)

        st.markdown("<hr style='margin: 16px 0; opacity: 0.2;'>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class="result-cite">Azure AI Foundry › projects › default</div>
            <a class="result-title" href="#" onclick="return false;">Niranjan Hebli - Azure Deployed Knowledge Base Files</a>
            """,
            unsafe_allow_html=True
        )

def render_organic_results():
    """Renders organic external search links list."""
    st.write("")
    st.write("")

    st.markdown(
        """
        <div class="result-cite">
            <span style="border-radius:50%; background-color:#4285f4; padding:1px 5px; font-weight:bold; color:white; font-size:10px; margin-right:4px;">in</span>
            https://www.linkedin.com › in › niranjanhebli
        </div>
        <a class="result-title" href="https://linkedin.com/in/niranjanhebli" target="_blank">Niranjan Hebli - Generative AI Developer & Software Engineer</a>
        <div class="result-snippet">
            Connect with Niranjan Hebli on LinkedIn. View profiles, professional accomplishments, experience building dynamic software systems, and open opportunities.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="result-cite">
            <span style="border-radius:50%; background-color:#3c4043; padding:1px 5px; font-weight:bold; color:white; font-size:10px; margin-right:4px;">git</span>
            https://github.com › niranjanhebli
        </div>
        <a class="result-title" href="https://github.com/niranjanhebli" target="_blank">niranjanhebli (Niranjan Hebli) · GitHub</a>
        <div class="result-snippet">
            Explore open source projects, agentic workflows, machine learning repositories, and code updates by Niranjan Hebli on GitHub.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="result-cite">
            <span style="border-radius:50%; background-color:#ea4335; padding:1px 5px; font-weight:bold; color:white; font-size:10px; margin-right:4px;">AI</span>
            https://github.com › niranjanhebli › agentic-qna-system
        </div>
        <a class="result-title" href="https://github.com/niranjanhebli" target="_blank">Agentic QnA System - Built using LangGraph & LLMs</a>
        <div class="result-snippet">
            A multi-agent retrieval system that coordinates queries to specialized node endpoints. Utilizing supervisory routing configurations and self-validation.
        </div>
        """,
        unsafe_allow_html=True
    )

def render_knowledge_graph():
    """Renders the sidebar Profile Knowledge Panel component."""
    with st.container(border=True):
        st.markdown(
            """
            <div style="font-size:24px; font-weight:600; margin-bottom: 2px;">Niranjan Hebli</div>
            <div style="font-size:14px; color: var(--text-color); opacity: 0.7; margin-bottom:12px;">Generative AI Developer & Software Engineer</div>

            <div style="font-size:14px; line-height:1.5; margin-bottom: 16px;">
                Niranjan is a software engineer specializing in Generative AI, LLM orchestration, and RAG pipelines. He develops multi-agent applications using frameworks like LangGraph and LangChain.
            </div>

            <hr style="margin: 12px 0; opacity: 0.3;">

            <div style="font-size:14px; margin-bottom:8px;"><b style="color: var(--text-color);">Education:</b> Bachelor of Engineering in CS (2024)</div>
            <div style="font-size:14px; margin-bottom:8px;"><b style="color: var(--text-color);">Location:</b> India</div>
            <div style="font-size:14px; margin-bottom:8px;"><b style="color: var(--text-color);">Primary Tech Stack:</b> Python, LangGraph, FastAPI, SQL, JS</div>
            <div style="font-size:14px; margin-bottom:16px;"><b style="color: var(--text-color);">Focus Areas:</b> Agentic Systems, RAG Pipelines, Backend Development</div>

            <hr style="margin: 12px 0; opacity: 0.3;">

            <div style="font-size:13px; font-weight:700; text-transform:uppercase; color: var(--text-color); opacity:0.6; margin-bottom: 8px;">Profiles & Contact</div>

            <div class="badge-container">
                <a class="social-badge" href="https://github.com/niranjanhebli" target="_blank">🐙 GitHub</a>
                <a class="social-badge" href="https://linkedin.com/in/niranjanhebli" target="_blank">🔗 LinkedIn</a>
                <a class="social-badge" href="mailto:niranjan.hebli@example.com">✉️ Email</a>
            </div>
            """,
            unsafe_allow_html=True
        )
