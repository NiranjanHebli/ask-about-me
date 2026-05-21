
import time
import urllib.parse

import streamlit as st
import streamlit.components.v1 as components

# Autocomplete suggestion bank
AUTOCOMPLETE_SUGGESTIONS = [
    "What is Niranjan's tech stack?",
    "Tell me about Niranjan's experience",
    "What projects has Niranjan developed?",
    "How can I contact Niranjan?",
    "What are Niranjan's AI and ML skills?",
    "Tell me about Niranjan's education",
    "What programming languages does Niranjan know?",
    "What is Niranjan's experience with LLMs?",
]

# Premium Glassmorphic Theme palettes
_LIGHT = {
    "theme_name":  "light",
    "app_bg":      "#e0eafc",
    "bg_gradient": "linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%)",
    "orb1":        "rgba(168, 192, 255, 0.6)",
    "orb2":        "rgba(255, 184, 210, 0.4)",
    "glass_bg":    "rgba(255, 255, 255, 1.0)", # Solid white for search bar
    "glass_bg_hover": "rgba(255, 255, 255, 1.0)",
    "glass_border": "rgba(255, 255, 255, 0.9)",
    "glass_border_hl": "rgba(255, 255, 255, 1.0)",
    "text":        "#1e293b",
    "text_muted":  "#64748b",
    "accent":      "#6366f1",
    "accent_grad": "linear-gradient(135deg, #6366f1 0%, #a855f7 100%)",
    "shadow":      "rgba(30, 41, 59, 0.05)",
    "shadow_hover": "rgba(99, 102, 241, 0.15)",
}

_DARK = {
    "theme_name":  "dark",
    "app_bg":      "#0f111a",
    "bg_gradient": "linear-gradient(135deg, #0f111a 0%, #171124 50%, #0d142b 100%)",
    "orb1":        "rgba(99, 102, 241, 0.15)",
    "orb2":        "rgba(168, 85, 247, 0.12)",
    "glass_bg":    "rgba(30, 30, 40, 0.4)",
    "glass_bg_hover": "rgba(40, 40, 55, 0.5)",
    "glass_border": "rgba(255, 255, 255, 0.08)",
    "glass_border_hl": "rgba(255, 255, 255, 0.15)",
    "text":        "#f8fafc",
    "text_muted":  "#94a3b8",
    "accent":      "#818cf8",
    "accent_grad": "linear-gradient(135deg, #818cf8 0%, #c084fc 100%)",
    "shadow":      "rgba(0, 0, 0, 0.3)",
    "shadow_hover": "rgba(129, 140, 248, 0.25)",
}

def _c() -> dict:
    """Return the active theme palette."""
    return _DARK if st.session_state.get("theme", "light") == "dark" else _LIGHT

# CSS injection
def inject_custom_css():
    c = _c()
    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@500;700;800&display=swap');

/* Reset */
#MainMenu, footer, header {{ visibility: hidden; }}

/* Ambient Glass Background */
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stHeader"],
[data-testid="stBottom"] {{
    background: {c["bg_gradient"]} !important;
    font-family: 'Inter', sans-serif;
    position: relative;
    z-index: 0;
}}

/* Floating Ambient Orbs */
[data-testid="stAppViewContainer"]::before,
[data-testid="stAppViewContainer"]::after {{
    content: '';
    position: fixed;
    z-index: -1;
    filter: blur(100px);
    border-radius: 50%;
    animation: float 20s infinite ease-in-out alternate;
    pointer-events: none;
}}
[data-testid="stAppViewContainer"]::before {{
    width: 60vw; height: 60vh;
    top: -10%; right: -10%;
    background: {c["orb1"]};
}}
[data-testid="stAppViewContainer"]::after {{
    width: 50vw; height: 50vh;
    bottom: -10%; left: -10%;
    background: {c["orb2"]};
    animation-delay: -5s;
}}

@keyframes float {{
    0% {{ transform: translate(0, 0) scale(1); }}
    50% {{ transform: translate(-3vw, 5vh) scale(1.05); }}
    100% {{ transform: translate(2vw, -2vh) scale(0.95); }}
}}

/* Global Text */
.stMarkdown, .stMarkdown p, .stMarkdown li,
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{
    color: {c["text"]} !important;
}}

/* Remove default top padding */
[data-testid="stAppViewContainer"] > .main > .block-container {{
    padding-top: 2rem !important;
    max-width: 1200px !important;
}}

/* ── Top Nav & Search Bar ── */
/* Explicitly strip background and borders from ALL outer Streamlit containers */
[data-testid="stForm"] {{
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}}
[data-testid="stTextInput"] {{
    background: transparent !important;
}}
[data-testid="stTextInput"] > div {{
    background: transparent !important;
    background-color: transparent !important;
}}
[data-testid="stTextInput"] > div > div {{
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
}}

/* Fix for the black corners: strip background from the baseweb wrapper */
[data-testid="stTextInput"] div[data-baseweb="input"] {{
    background-color: transparent !important;
    background: transparent !important;
    border: none !important;
}}

/* Clean Pill-Shaped Glassmorphic Search Bar applied ONLY to the inner base-input */
[data-testid="stTextInput"] div[data-baseweb="base-input"] {{
    background: {c["glass_bg"]} !important;
    backdrop-filter: blur(16px) saturate(180%) !important;
    -webkit-backdrop-filter: blur(16px) saturate(180%) !important;
    border: 1px solid {c["glass_border"]} !important;
    border-radius: 30px !important;
    box-shadow: 0 8px 32px {c["shadow"]} !important;
    padding: 6px 12px !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}}
[data-testid="stTextInput"] div[data-baseweb="base-input"]:focus-within {{
    background: {c["glass_bg_hover"]} !important;
    border-color: {c["accent"]} !important;
    box-shadow: 0 0 0 3px {c["shadow_hover"]}, 0 8px 32px {c["shadow"]} !important;
    transform: translateY(-1px) !important;
}}
[data-testid="stTextInput"] input {{
    background-color: transparent !important;
    color: {c["text"]} !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 16px !important;
    font-weight: 500 !important;
}}
[data-testid="stTextInput"] input::placeholder {{
    color: {c["text_muted"]} !important;
    opacity: 0.7 !important;
}}
div[data-testid="InputInstructions"] {{ display: none !important; }}

/* Glass Buttons (Includes suggestion chips) */
.stButton > button, .stFormSubmitButton > button {{
    background: {c["glass_bg"]} !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    color: {c["text"]} !important;
    border: 1px solid {c["glass_border"]} !important;
    border-radius: 20px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    padding: 8px 16px !important;
    box-shadow: 0 4px 12px {c["shadow"]} !important;
    transition: all 0.2s ease !important;
}}
.stButton > button:hover, .stFormSubmitButton > button:hover {{
    background: {c["glass_bg_hover"]} !important;
    border-color: {c["accent"]} !important;
    color: {c["accent"]} !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 16px {c["shadow_hover"]} !important;
}}

/* Download button special styling */
.stDownloadButton > button {{
    background: {c["accent_grad"]} !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    width: 100% !important;
    box-shadow: 0 8px 24px {c["shadow_hover"]} !important;
}}
.stDownloadButton > button:hover {{
    color: white !important;
    opacity: 0.9 !important;
    border-color: transparent !important;
}}

/* Premium Logos */
.logo-large {{
    font-family: 'Outfit', sans-serif;
    font-size: 56px;
    font-weight: 800;
    letter-spacing: -2px;
    text-align: center;
    filter: drop-shadow(0 4px 12px {c["shadow_hover"]});
}}
.logo-compact {{
    font-family: 'Outfit', sans-serif;
    font-size: 28px;
    font-weight: 800;
    letter-spacing: -1px;
    white-space: nowrap;
    display: flex;
    align-items: center;
}}

/* Search Stats */
.search-stats {{
    font-size: 13px;
    color: {c["text_muted"]};
    margin-top: 32px;
    margin-bottom: 16px;
    padding-bottom: 12px;
    border-bottom: 1px solid {c["glass_border"]};
}}

/* ── Distinct Component Widgets (Glass Cards) ── */
.glass-card {{
    background: {c["glass_bg"]};
    backdrop-filter: blur(20px) saturate(180%);
    -webkit-backdrop-filter: blur(20px) saturate(180%);
    border: 1px solid {c["glass_border"]};
    border-radius: 20px;
    padding: 26px;
    box-shadow: 0 8px 32px {c["shadow"]};
    transition: all 0.3s ease;
}}
.glass-card:hover {{
    border-color: {c["glass_border_hl"]};
    box-shadow: 0 12px 40px {c["shadow_hover"]};
}}

/* Profile Sidebar Widget */
.profile-widget {{
    padding: 24px;
    margin-bottom: 24px;
}}
.profile-avatar {{
    width: 72px;
    height: 72px;
    background: {c["accent_grad"]};
    border-radius: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 32px;
    font-weight: 800;
    font-family: 'Outfit', sans-serif;
    margin-bottom: 24px;
    box-shadow: 0 8px 24px {c["shadow_hover"]};
}}
.profile-title {{
    font-size: 26px;
    font-weight: 800;
    color: {c["text"]};
    margin-bottom: 4px;
    font-family: 'Outfit', sans-serif;
}}
.profile-subtitle {{
    font-size: 14px;
    font-weight: 600;
    color: {c["accent"]};
    margin-bottom: 18px;
}}
.profile-desc {{
    font-size: 14px;
    color: {c["text_muted"]};
    line-height: 1.6;
    margin-bottom: 24px;
}}
.profile-detail {{
    font-size: 13px;
    color: {c["text"]};
    margin-bottom: 12px;
    line-height: 1.5;
}}
.profile-detail b {{
    font-weight: 600;
    color: {c["text"]};
}}

/* AI Overview Widget */
.ai-overview-wrap {{
    position: relative;
    overflow: hidden;
    padding: 24px;
    margin-bottom: 24px;
    height: 100%; /* Ensure it fills column height */
}}
.ai-overview-wrap::before {{
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0; width: 4px;
    background: {c["accent_grad"]};
}}

/* Chat Widget */
.chat-widget-wrap {{
    display: flex;
    flex-direction: column;
    height: 100%;
    padding: 0; /* Remove padding for header styling */
    overflow: hidden;
}}
.chat-header {{
    background: {c["accent"]};
    color: white;
    padding: 12px 16px;
    font-weight: 600;
    font-size: 14px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}}
.chat-body {{
    padding: 16px;
    flex-grow: 1;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 12px;
    font-size: 14px;
}}
.chat-msg-agent {{
    background: {c["glass_bg_hover"]};
    padding: 10px 14px;
    border-radius: 12px;
    border-top-left-radius: 4px;
    color: {c["text"]};
    align-self: flex-start;
    max-width: 85%;
    border: 1px solid {c["glass_border"]};
}}
.chat-msg-user {{
    background: {c["accent"]};
    color: white;
    padding: 10px 14px;
    border-radius: 12px;
    border-top-right-radius: 4px;
    align-self: flex-end;
    max-width: 85%;
}}
.chat-input-area {{
    padding: 12px;
    border-top: 1px solid {c["glass_border"]};
}}

/* Organic Results Widgets */
.result-card {{
    padding: 20px 24px;
    margin-bottom: 16px;
    cursor: default;
}}
.result-card:hover {{
    transform: translateY(-3px);
    border-color: {c["accent"]};
}}
.r-site {{ font-size: 13px; color: {c["text"]}; font-weight: 600; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.5px; opacity: 0.8;}}
.r-title {{ font-size: 18px; font-weight: 600; color: {c["accent"]}; text-decoration: none; display: block; margin-bottom: 10px; line-height: 1.3; }}
.r-snippet {{ font-size: 14.5px; color: {c["text_muted"]}; line-height: 1.6; margin: 0; }}

/* Project Cards */
.section-label {{
    font-size: 18px;
    font-weight: 700;
    color: {c["text"]};
    margin: 32px 0 20px;
    font-family: 'Outfit', sans-serif;
    letter-spacing: -0.5px;
}}
.projects-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 16px;
    margin-bottom: 24px;
}}
.project-card {{
    padding: 22px;
}}
.project-card:hover {{
    transform: translateY(-4px);
    border-color: {c["accent"]};
}}
.pc-title {{
    font-size: 17px;
    font-weight: 700;
    color: {c["text"]};
    margin-bottom: 10px;
    display: block;
    text-decoration: none;
    font-family: 'Outfit', sans-serif;
}}
.pc-title:hover {{ color: {c["accent"]}; }}
.pc-desc {{
    font-size: 14px;
    color: {c["text_muted"]};
    line-height: 1.6;
    margin-bottom: 18px;
}}
.pc-tags {{ display: flex; flex-wrap: wrap; gap: 8px; }}
.pc-tag {{
    font-size: 11px;
    font-weight: 600;
    padding: 4px 10px;
    border-radius: 8px;
    background: {c["glass_bg_hover"]};
    color: {c["text"]};
    border: 1px solid {c["glass_border"]};
}}

/* Autocomplete Dropdown - Glass */
.custom-suggestions-dropdown {{
    position: absolute;
    background: {c["glass_bg"]} !important;
    backdrop-filter: blur(24px) saturate(180%) !important;
    -webkit-backdrop-filter: blur(24px) saturate(180%) !important;
    border: 1px solid {c["glass_border"]} !important;
    border-radius: 20px !important;
    box-shadow: 0 12px 40px {c["shadow"]} !important;
    margin-top: 8px !important;
    padding: 8px !important;
    z-index: 999999 !important;
    display: none;
}}
.custom-suggestion-item {{
    padding: 12px 20px !important;
    cursor: pointer !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 15px !important;
    font-weight: 500 !important;
    color: {c["text"]} !important;
    border-radius: 12px !important;
    transition: all 0.2s !important;
}}
.custom-suggestion-item:hover, .custom-suggestion-item.active {{
    background: {c["glass_bg_hover"]} !important;
    color: {c["accent"]} !important;
    transform: translateX(4px) !important;
}}

/* Suggestion Label below Search Bar */
.sugg-label {{
    text-align: center;
    font-size: 13px;
    font-weight: 500;
    color: {c["text_muted"]};
    margin: 24px 0 12px 0;
}}
</style>
""", unsafe_allow_html=True)


# Theme Toggle
def render_theme_toggle(key: str = "theme_toggle_default"):
    current = st.session_state.get("theme", "light")
    label = "🌙 Dark" if current == "light" else "☀️ Light"
    if st.button(label, key=key):
        st.session_state.theme = "dark" if current == "light" else "light"
        st.session_state.cached_query = ""
        st.session_state.cached_response = None
        st.rerun()


# JS Injection for Autocomplete
def inject_autocomplete_js():
    import json
    suggestions_json = json.dumps(AUTOCOMPLETE_SUGGESTIONS)
    js_code = f"""
    <script>
    (function() {{
        try {{
            const parentDoc = window.parent.document;
            const suggestions = {suggestions_json};
            let dropdown = parentDoc.getElementById('custom-global-suggestions-dropdown');
            if (!dropdown) {{
                dropdown = parentDoc.createElement('div');
                dropdown.id = 'custom-global-suggestions-dropdown';
                dropdown.className = 'custom-suggestions-dropdown';
                parentDoc.body.appendChild(dropdown);
            }}
            
            let activeInput = null;
            let activeIndex = -1;
            
            const positionDropdown = (input) => {{
                const rect = input.getBoundingClientRect();
                const win = parentDoc.defaultView || window;
                dropdown.style.top = (rect.bottom + win.scrollY) + 'px';
                dropdown.style.left = (rect.left + win.scrollX) + 'px';
                dropdown.style.width = rect.width + 'px';
            }};
            
            const showSuggestions = (input) => {{
                activeInput = input;
                const val = input.value.trim().toLowerCase();
                let filtered = val === "" ? suggestions.slice(0, 5) : suggestions.filter(s => s.toLowerCase().includes(val));
                
                if (filtered.length === 0) {{ dropdown.style.display = 'none'; return; }}
                
                dropdown.innerHTML = filtered.map((s, idx) => `
                    <div class="custom-suggestion-item" data-val="${{encodeURIComponent(s)}}" data-index="${{idx}}">${{s}}</div>
                `).join('');
                positionDropdown(input);
                dropdown.style.display = 'block';
                activeIndex = -1;
            }};
            
            const selectSuggestion = (input, val) => {{
                const valueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
                const protoSetter = Object.getOwnPropertyDescriptor(Object.getPrototypeOf(input), "value").set;
                (valueSetter && valueSetter !== protoSetter ? protoSetter : valueSetter).call(input, val);
                input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                dropdown.style.display = 'none';
                
                const form = input.closest('form');
                if (form) {{
                    const btn = form.querySelector('button[type="submit"]');
                    if(btn) btn.click(); else form.requestSubmit();
                }} else {{
                    input.dispatchEvent(new KeyboardEvent('keydown', {{ key: 'Enter', keyCode: 13, bubbles: true }}));
                }}
            }};
            
            const initInput = (input) => {{
                if (input.dataset.customSuggestions) return;
                input.dataset.customSuggestions = "true";
                input.setAttribute('autocomplete', 'off');
                input.addEventListener('focus', () => showSuggestions(input));
                input.addEventListener('input', () => showSuggestions(input));
                input.addEventListener('blur', () => setTimeout(() => {{ if(activeInput===input) dropdown.style.display='none'; }}, 200));
                
                input.addEventListener('keydown', (e) => {{
                    const items = dropdown.querySelectorAll('.custom-suggestion-item');
                    if (dropdown.style.display === 'none' || !items.length) return;
                    if (e.key === 'ArrowDown') {{ e.preventDefault(); activeIndex = (activeIndex+1)%items.length; updateActive(items); }}
                    else if (e.key === 'ArrowUp') {{ e.preventDefault(); activeIndex = (activeIndex-1+items.length)%items.length; updateActive(items); }}
                    else if (e.key === 'Enter' && activeIndex >= 0) {{
                        e.preventDefault();
                        selectSuggestion(input, decodeURIComponent(items[activeIndex].dataset.val));
                    }}
                }});
            }};
            
            const updateActive = (items) => {{
                items.forEach((item, idx) => item.classList.toggle('active', idx === activeIndex));
            }};
            
            dropdown.addEventListener('mousedown', (e) => {{
                const item = e.target.closest('.custom-suggestion-item');
                if (item && activeInput) {{ e.preventDefault(); selectSuggestion(activeInput, decodeURIComponent(item.dataset.val)); }}
            }});
            
            if (!parentDoc._customSuggestionsInitialized) {{
                parentDoc._customSuggestionsInitialized = true;
                parentDoc.querySelectorAll('input[type="text"]').forEach(initInput);
                new MutationObserver(() => parentDoc.querySelectorAll('input[type="text"]').forEach(initInput))
                    .observe(parentDoc.body, {{ childList: true, subtree: true }});
            }}
        }} catch (e) {{}}
    }})();
    </script>
    """
    components.html(js_code, height=0, width=0)


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


# Home page
def render_search_home(click_suggestion_callback):
    _, toggle_col = st.columns([10, 1])
    with toggle_col:
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
                if st.form_submit_button("Start Search", use_container_width=True) and query_input.strip():
                    with st.spinner("Searching for insights..."):
                        time.sleep(0.3) # Brief pause to display the loader smoothly
                        click_suggestion_callback(query_input.strip())
                    st.rerun()
                    
        inject_autocomplete_js()
        
        # Add 5 suggestions below the search bar
        st.markdown('<div class="sugg-label">Try a quick search:</div>', unsafe_allow_html=True)
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
                # Swapped to standard button to allow spinner rendering
                if st.button(label, use_container_width=True, key=f"chip_{label}"):
                    with st.spinner("Searching for insights..."):
                        time.sleep(0.3)
                        click_suggestion_callback(query)
                    st.rerun()


# Results Header 
def render_results_header(reset_search_callback):
    col1, col2, col3, col4 = st.columns([3, 5.5, 1.5, 1]) # Slightly adjusted column width to fit subtitle

    with col1:
        st.markdown(_get_google_logo_html("logo-compact"), unsafe_allow_html=True)
    
    with col2:
        val = st.text_input("", value=st.session_state.search_query, label_visibility="collapsed", key="res_search")
        if val != st.session_state.search_query:
            with st.spinner("Searching..."):
                time.sleep(0.3)
                st.session_state.search_query = val
            st.rerun()
        inject_autocomplete_js()
    
    with col3:
        st.button("Back Home", on_click=reset_search_callback, use_container_width=True)
    
    with col4:
        render_theme_toggle(key="res_theme")


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


# --- AI Overview & Chat Section ---

def render_ai_overview_skeleton():
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("<div class='glass-card ai-overview-wrap' style='opacity: 0.6;'>✨ Synthesizing AI overview...</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='glass-card chat-widget-wrap' style='opacity: 0.6;'><div class='chat-header'>Loading Agent...</div><div class='chat-body'></div></div>", unsafe_allow_html=True)


def render_ai_overview_and_chat(query: str, answer_text: str):
    """Renders the AI Overview and the Chat Widget side-by-side."""
    col1, col2 = st.columns([2, 1])
    
    with col1:
        import re
        sentences = re.split(r'(?<=[.!?])\s+', answer_text.strip())
        blurb = " ".join(sentences[:3]) if sentences else answer_text[:280]
        if len(blurb) > 320:
            blurb = blurb[:317].rstrip() + "…"

        st.markdown(f"""
        <div class="glass-card ai-overview-wrap">
          <div style="font-weight: 700; font-size: 15px; margin-bottom: 14px; display: flex; align-items: center; gap: 8px;">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color:var(--accent);"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
            AI Overview
          </div>
          <div style="font-size: 15px; line-height: 1.7;">
            <p style="margin:0;">{blurb}</p>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        render_chat_widget()

def render_chat_widget():
    """Renders a static representation of the chat widget for the UI."""
    st.markdown(f"""
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
    """, unsafe_allow_html=True)


# Profile Widget 
def render_knowledge_graph():
    c = _c()
    
    def _get_resume_pdf() -> bytes:
        try:
            from pdf_generator import generate_resume_pdf
            return generate_resume_pdf()
        except ImportError:
            return b""
            
    st.markdown(f"""
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
            <a href="https://www.linkedin.com/in/niranjan-hebli-333211211/" target="_blank" style="color: {c['accent']}; text-decoration: none; font-weight: 600;">LinkedIn</a> &nbsp;|&nbsp; 
            <a href="https://leetcode.com/u/NiranjanHebli/" target="_blank" style="color: {c['accent']}; text-decoration: none; font-weight: 600;">LeetCode</a> &nbsp;|&nbsp; 
            <a href="https://github.com/NiranjanHebli" target="_blank" style="color: {c['accent']}; text-decoration: none; font-weight: 600;">GitHub</a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
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
        }
    ]
    for r in results:
        st.markdown(f"""
        <div class="glass-card result-card">
            <div class="r-site">{r['site']}</div>
            <a href="{r['url']}" class="r-title" target="_blank">{r['title']}</a>
            <p class="r-snippet">{r['snippet']}</p>
        </div>
        """, unsafe_allow_html=True)


def render_project_showcase():
    projects = [
        {
            "title": "Agentic Q&A System",
            "desc":  "Multi-agent retrieval system using LangGraph with dynamic supervisor routing and self-validation loops.",
            "tags":  ["LangGraph", "Python", "RAG", "Azure"],
            "link":  "https://github.com/NiranjanHebli/agentic-qna-system",
        },
        {
            "title": "NCERT Class IX Retrieval",
            "desc":  "Advanced retrieval and question-answering system utilizing semantic chunking and metadata filtering.",
            "tags":  ["Python", "RAG", "ChromaDB", "LangChain"],
            "link":  "https://github.com/NiranjanHebli/ncert-class-ix-retrieval-system",
        },
        {
            "title": "Churn Prediction AI",
            "desc":  "Machine learning pipeline that processes customer behavioral data and predicts churn probability.",
            "tags":  ["Python", "scikit-learn", "XGBoost"],
            "link":  "https://github.com/NiranjanHebli/churn-prediction-ai",
        },
    ]
    cards = '<div class="section-label">Featured Projects</div><div class="projects-grid">'
    for p in projects:
        tags = "".join(f'<span class="pc-tag">{t}</span>' for t in p["tags"])
        cards += f"""
        <div class="glass-card project-card">
          <a class="pc-title" href="{p["link"]}" target="_blank">{p["title"]}</a>
          <p class="pc-desc">{p["desc"]}</p>
          <div class="pc-tags">{tags}</div>
        </div>"""
    cards += "</div>"
    st.markdown(cards, unsafe_allow_html=True)


def render_share_button(query: str):
    c = _c()
    encoded = urllib.parse.quote(query, safe="")
    html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>
body{{margin:0;padding:4px 0;font-family:'Inter',sans-serif;background:transparent;overflow:hidden;}}
.btn{{display:inline-flex;align-items:center;gap:8px;padding:10px 20px;
  background:{c["glass_bg"]};color:{c["text"]};border:1px solid {c["glass_border"]};
  backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
  border-radius:24px;font-size:13px;font-weight:600;cursor:pointer;font-family:inherit;
  box-shadow: 0 4px 12px {c["shadow"]}; transition:all .2s;}}
.btn:hover{{background:{c["glass_bg_hover"]};border-color:{c["accent"]};transform:translateY(-2px);
  box-shadow: 0 6px 16px {c["shadow_hover"]}; color:{c["accent"]};}}
.ok{{display:none;font-size:12px;font-weight:600;color:{c["accent"]};margin-left:12px;}}
</style></head><body>
<button class="btn" onclick="share()">
  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor"
    stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
    <path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/>
    <polyline points="16 6 12 2 8 6"/>
    <line x1="12" y1="2" x2="12" y2="15"/>
  </svg>
  Share Result
</button>
<span class="ok" id="ok">Link copied! ✨</span>
<script>
function share(){{
  try{{
    const url=window.parent.location.origin+window.parent.location.pathname+'?q={encoded}';
    navigator.clipboard.writeText(url).then(()=>{{
      const ok=document.getElementById('ok');
      ok.style.display='inline';
      setTimeout(()=>ok.style.display='none',2000);
    }});
  }}catch(e){{}}
}}
</script></body></html>"""
    components.html(html, height=60, scrolling=False)


def render_skeleton_loader() -> str:
    return "<div class='glass-card answer-box' style='opacity: 0.5;'>Loading insights...</div>"
