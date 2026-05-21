import time
import streamlit as st

# Set up page configurations first
st.set_page_config(
    page_title="Ask About Me - Niranjan Hebli",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Import modular components
from query_engine import query_azure_ai_foundry
from ui import (
    inject_custom_css,
    render_search_home,
    render_results_header,
    render_search_stats,
    render_featured_snippet,
    render_organic_results,
    render_knowledge_graph
)

# Inject custom CSS styling
inject_custom_css()

# Session State Initialization
if "search_query" not in st.session_state:
    st.session_state.search_query = ""
if "search_clicked" not in st.session_state:
    st.session_state.search_clicked = False

# Callback handlers
def click_suggestion(query):
    st.session_state.search_query = query
    st.session_state.search_clicked = True

def reset_search():
    st.session_state.search_query = ""
    st.session_state.search_clicked = False

# Render view based on state
if not st.session_state.search_clicked or not st.session_state.search_query.strip():
    render_search_home(click_suggestion_callback=click_suggestion)
else:
    # Header navigation bar
    render_results_header(reset_search_callback=reset_search)
    
    # Primary view columns
    body_col1, body_col2 = st.columns([6.8, 3.2], gap="large")
    
    with body_col1:
        start_time = time.time()
        
        with st.spinner("Searching..."):
            ans_content, source_label = query_azure_ai_foundry(st.session_state.search_query)
            
        elapsed_time = round(time.time() - start_time, 2)
        
        # Display search latency info
        render_search_stats(elapsed_time)
        
        # Display featured response snippet
        render_featured_snippet(ans_content)
        
        # Display organic search results lists
        render_organic_results()
        
    with body_col2:
        # Display knowledge graph sidebar card
        render_knowledge_graph()
