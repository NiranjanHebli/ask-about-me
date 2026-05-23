import time
import threading
import streamlit as st
from src.query_engine import query_llm
from src.rag_engine import get_vector_store
from src.ui import (
    inject_custom_css,
    render_featured_snippet,
    render_knowledge_graph,
    render_organic_results,
    render_project_showcase,
    render_results_header,
    render_search_home,
    render_search_stats,
    render_share_button,
    render_skeleton_loader,
)

# Spin up a background thread to pre-load Hugging Face embeddings and FAISS index
threading.Thread(target=get_vector_store, daemon=True).start()


# Page config (must be first Streamlit call)
st.set_page_config(
    page_title="Ask About Me - Niranjan Hebli",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Session state defaults
if "theme" not in st.session_state:
    st.session_state.theme = "dark"
if "search_query" not in st.session_state:
    st.session_state.search_query = ""
if "search_clicked" not in st.session_state:
    st.session_state.search_clicked = False
if "cached_query" not in st.session_state:
    st.session_state.cached_query = ""
if "cached_response" not in st.session_state:
    st.session_state.cached_response = None


# Inject CSS for the current theme
inject_custom_css()

# Handle URL query params (share links & autocomplete navigation)
q_param = st.query_params.get("q", "")
if q_param and not st.session_state.search_clicked:
    st.session_state.search_query = q_param
    st.session_state.search_clicked = True


# Callbacks
def click_suggestion(query: str):
    st.session_state.search_query = query
    st.session_state.search_clicked = True


def reset_search():
    st.session_state.search_query = ""
    st.session_state.search_clicked = False
    st.session_state.cached_query = ""
    st.session_state.cached_response = None
    st.query_params.clear()


# Home page
if not st.session_state.search_clicked or not st.session_state.search_query.strip():
    render_search_home(click_suggestion_callback=click_suggestion)

# Results page
else:
    query = st.session_state.search_query
    render_results_header(reset_search_callback=reset_search)

    body_col1, body_col2 = st.columns([6.8, 3.2], gap="large")

    with body_col2:
        render_knowledge_graph()

    with body_col1:
        start_time = time.time()
        need_fetch = query != st.session_state.cached_query

        if need_fetch:
            loader_ph = st.empty()
            loader_ph.markdown(render_skeleton_loader(), unsafe_allow_html=True)

            # Yield slightly to allow Streamlit to flush the fully constructed layout
            # (including col2) to the frontend before the blocking API call.
            time.sleep(0.05)

            ans_content, source_label = query_llm(query)

            elapsed_time = round(time.time() - start_time, 2)

            # Cache result so theme toggles don't re-fetch or re-animate
            st.session_state.cached_query = query
            st.session_state.cached_response = (ans_content, source_label, elapsed_time)

            loader_ph.empty()
            animate = True
        else:
            ans_content, source_label, elapsed_time = st.session_state.cached_response
            animate = False

        render_search_stats(elapsed_time)
        render_featured_snippet(ans_content, animate=animate)
        render_organic_results()
        render_project_showcase()
        render_share_button(query)
