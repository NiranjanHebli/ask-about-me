import json
import urllib.parse

import streamlit as st
import streamlit.components.v1 as components

from .theme import AUTOCOMPLETE_SUGGESTIONS, _c


def inject_autocomplete_js():
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
    return """
<style>
.loader-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 30px;
}
.dots-wrapper {
    display: flex;
    gap: 12px;
    margin-bottom: 16px;
}
.g-dot {
    width: 16px;
    height: 16px;
    border-radius: 50%;
    animation: bounce 1.4s infinite ease-in-out both;
}
.g-dot:nth-child(1) { background-color: #4285F4; animation-delay: -0.32s; }
.g-dot:nth-child(2) { background-color: #EA4335; animation-delay: -0.16s; }
.g-dot:nth-child(3) { background-color: #FBBC05; animation-delay: 0s; }
.g-dot:nth-child(4) { background-color: #34A853; animation-delay: 0.16s; }

@keyframes bounce {
    0%, 80%, 100% { transform: scale(0); }
    40% { transform: scale(1); }
}
.loader-text {
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: 15px;
    color: #64748b;
    letter-spacing: 0.5px;
    animation: pulse 1.5s infinite;
}
@keyframes pulse {
    0% { opacity: 0.5; }
    50% { opacity: 1; }
    100% { opacity: 0.5; }
}
</style>
<div class='glass-card' style='text-align: center; padding: 50px 20px; border-radius: 20px;'>
    <div class='loader-container'>
        <div class='dots-wrapper'>
            <div class='g-dot'></div>
            <div class='g-dot'></div>
            <div class='g-dot'></div>
            <div class='g-dot'></div>
        </div>
        <div class='loader-text'>Fetching insights...</div>
    </div>
</div>
"""
