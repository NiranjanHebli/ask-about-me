import streamlit as st
import streamlit.components.v1 as components

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

_LIGHT = {
    "theme_name": "light",
    "app_bg": "#e0eafc",
    "bg_gradient": "linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%)",
    "orb1": "rgba(168, 192, 255, 0.6)",
    "orb2": "rgba(255, 184, 210, 0.4)",
    "glass_bg": "rgba(255, 255, 255, 1.0)",
    "glass_bg_hover": "rgba(255, 255, 255, 1.0)",
    "glass_border": "rgba(255, 255, 255, 0.9)",
    "glass_border_hl": "rgba(255, 255, 255, 1.0)",
    "text": "#1e293b",
    "text_muted": "#64748b",
    "accent": "#6366f1",
    "accent_grad": "linear-gradient(135deg, #6366f1 0%, #a855f7 100%)",
    "shadow": "rgba(30, 41, 59, 0.05)",
    "shadow_hover": "rgba(99, 102, 241, 0.15)",
}

_DARK = {
    "theme_name": "dark",
    "app_bg": "#0f111a",
    "bg_gradient": "linear-gradient(135deg, #0f111a 0%, #171124 50%, #0d142b 100%)",
    "orb1": "rgba(99, 102, 241, 0.15)",
    "orb2": "rgba(168, 85, 247, 0.12)",
    "glass_bg": "rgba(30, 30, 40, 0.4)",
    "glass_bg_hover": "rgba(40, 40, 55, 0.5)",
    "glass_border": "rgba(255, 255, 255, 0.08)",
    "glass_border_hl": "rgba(255, 255, 255, 0.15)",
    "text": "#f8fafc",
    "text_muted": "#94a3b8",
    "accent": "#818cf8",
    "accent_grad": "linear-gradient(135deg, #818cf8 0%, #c084fc 100%)",
    "shadow": "rgba(0, 0, 0, 0.3)",
    "shadow_hover": "rgba(129, 140, 248, 0.25)",
}


def _c() -> dict:
    return _DARK if st.session_state.get("theme", "light") == "dark" else _LIGHT


def inject_custom_css():
    c = _c()
    st.markdown(
        f"""
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
    overflow: visible !important;
}}
[data-testid="stTextInput"] > div {{
    background: transparent !important;
    background-color: transparent !important;
    overflow: visible !important;
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
""",
        unsafe_allow_html=True,
    )


def render_theme_toggle(key: str = "theme_toggle_default"):
    current = st.session_state.get("theme", "light")
    label = "🌙 Dark" if current == "light" else "☀️ Light"

    if st.button(label, key=key):
        st.session_state.theme = "dark" if current == "light" else "light"
        st.rerun()

    # Dynamically find this button and float it exactly top-right
    # using a MutationObserver to ensure it applies even after re-renders
    components.html(
        """
        <script>
        const doc = window.parent.document;
        const styleThemeToggle = () => {
            const buttons = doc.querySelectorAll('button');
            buttons.forEach(btn => {
                if (btn.innerText.includes('🌙 Dark') || btn.innerText.includes('☀️ Light')) {
                    const container = btn.closest('div[data-testid="stElementContainer"]');
                    if (container && container.style.position !== 'fixed') {
                        container.style.position = 'fixed';
                        container.style.top = '16px';
                        container.style.right = '24px';
                        container.style.zIndex = '999999';
                        container.style.width = 'auto';
                    }
                }
            });
        };
        styleThemeToggle();
        const observer = new MutationObserver(styleThemeToggle);
        observer.observe(doc.body, { childList: true, subtree: true });
        </script>
        """,
        height=0,
        width=0,
    )
