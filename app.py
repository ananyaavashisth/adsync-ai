from __future__ import annotations

import streamlit as st
import requests
from bs4 import BeautifulSoup
import json
import os
import re
from typing import List

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AdSync AI · Landing Page Optimizer",
    page_icon="🔄",
    layout="centered",
)

# ── Session State Init ───────────────────────────────────────────────────────
if "results" not in st.session_state:
    st.session_state.results = None

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Global ────────────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}
#MainMenu, footer, header {visibility: hidden;}

/* ── Hero Section ──────────────────────────────────────────────── */
.hero {
    text-align: center;
    padding: 48px 0 12px 0;
}
.hero h1 {
    font-size: 2.6rem;
    font-weight: 800;
    background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
    line-height: 1.15;
    letter-spacing: -0.5px;
}
.hero p {
    color: #64748b;
    font-size: 1.1rem;
    margin-top: 10px;
    font-weight: 400;
}

/* ── Divider ───────────────────────────────────────────────────── */
.soft-divider {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(99,102,241,0.25), transparent);
    margin: 32px 0;
}

/* ── Input Card ────────────────────────────────────────────────── */
.input-label {
    font-size: 0.85rem;
    font-weight: 600;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 6px;
}

/* ── Result Banner ─────────────────────────────────────────────── */
.result-banner {
    background: linear-gradient(135deg, #f0fdf4, #ecfdf5);
    border: 1px solid #86efac;
    border-radius: 14px;
    padding: 20px 28px;
    text-align: center;
    margin-bottom: 24px;
}
.result-banner .icon { font-size: 2rem; }
.result-banner h3 {
    margin: 8px 0 4px 0;
    font-size: 1.25rem;
    font-weight: 700;
    color: #166534;
}
.result-banner p {
    color: #15803d;
    font-size: 0.9rem;
    margin: 0;
    font-weight: 500;
}

/* ── Change Card ───────────────────────────────────────────────── */
.change-card {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 18px 22px;
    margin-bottom: 14px;
}
.change-card .change-num {
    display: inline-block;
    background: linear-gradient(135deg, #6366f1, #a855f7);
    color: white;
    width: 24px; height: 24px;
    border-radius: 50%;
    text-align: center;
    line-height: 24px;
    font-size: 0.75rem;
    font-weight: 700;
    margin-right: 8px;
    vertical-align: middle;
}
.change-card .change-title {
    font-weight: 600;
    color: #334155;
    font-size: 0.95rem;
    vertical-align: middle;
}
.before-after {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-top: 12px;
}
.ba-box {
    border-radius: 10px;
    padding: 14px 16px;
    font-size: 0.88rem;
    line-height: 1.45;
    word-wrap: break-word;
}
.ba-before {
    background: #fef2f2;
    border: 1px solid #fecaca;
    color: #991b1b;
}
.ba-after {
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    color: #166534;
}
.ba-label {
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 6px;
    opacity: 0.7;
}

/* ── Preview Frame ─────────────────────────────────────────────── */
.preview-frame {
    border: 1px solid #e2e8f0;
    border-radius: 14px 14px 0 0;
    overflow: hidden;
    box-shadow: 0 4px 24px rgba(0,0,0,0.06);
}
.preview-bar {
    background: #f1f5f9;
    padding: 10px 16px;
    display: flex;
    align-items: center;
    gap: 6px;
    border-bottom: 1px solid #e2e8f0;
}
.preview-dot {
    width: 10px; height: 10px;
    border-radius: 50%;
    display: inline-block;
}
.dot-red { background: #f87171; }
.dot-yellow { background: #fbbf24; }
.dot-green { background: #4ade80; }
.preview-url {
    margin-left: 12px;
    font-size: 0.78rem;
    color: #94a3b8;
    font-family: 'SF Mono', 'Fira Code', monospace;
}

/* ── API key info ──────────────────────────────────────────────── */
.api-info {
    background: linear-gradient(135deg, #eff6ff, #f0f9ff);
    border: 1px solid #93c5fd;
    border-radius: 12px;
    padding: 16px 20px;
    margin-top: 8px;
    font-size: 0.88rem;
    line-height: 1.55;
    color: #1e40af;
}
.api-info strong { color: #1e3a8a; }
.api-info a { color: #6366f1; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>AdSync AI</h1>
    <p>Align your landing page with your ad creative to improve conversions</p>
</div>
<hr class="soft-divider">
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# BACKEND HELPERS  (unchanged logic)
# ══════════════════════════════════════════════════════════════════════════════

def extract_meaningful_text(soup: BeautifulSoup) -> list:
    texts = []
    for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'a', 'span', 'button', 'li', 'td', 'th']):
        text = tag.get_text(strip=True)
        if text and 10 < len(text) < 500:
            texts.append(text)
    return list(dict.fromkeys(texts))


def call_gemini(api_key: str, ad_context: str, page_texts: list) -> list:
    try:
        from google import genai
        from google.genai import types
        from pydantic import BaseModel

        class Replacement(BaseModel):
            old_text: str
            new_text: str
            change_summary: str  # human-friendly label

        class OptimizationResult(BaseModel):
            replacements: List[Replacement]

        client = genai.Client(api_key=api_key)

        system_instruction = (
            "You are an expert Conversion Rate Optimization (CRO) copywriter. "
            "Your task is to personalise a landing page so its messaging aligns with "
            "the provided ad creative / hook. You will receive the Ad Context and a "
            "list of texts extracted from the landing page.\n\n"
            "Rules:\n"
            "- Return a JSON with a 'replacements' array of objects.\n"
            "- Each object must have: old_text, new_text, change_summary.\n"
            "- old_text MUST exactly match one of the provided page texts.\n"
            "- new_text should be the personalized replacement aligned to the ad.\n"
            "- change_summary should be a short human-friendly label like 'Updated headline to reflect ad messaging' or 'Strengthened call-to-action'.\n"
            "- Only modify headlines, sub-headlines, value propositions, and CTAs.\n"
            "- Do NOT change navigation links, legal text, or company/brand names.\n"
            "- Keep new_text concise, persuasive, and matched to the ad hook.\n"
            "- If a text doesn't need changes, do NOT include it.\n"
            "- Aim for 3-8 high-impact changes."
        )

        prompt = (
            f"**Ad Context / Creative:**\n{ad_context}\n\n"
            f"**Page Texts (candidates for modification):**\n{json.dumps(page_texts, indent=2)}"
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema=OptimizationResult,
                temperature=0.7,
            ),
        )

        result = json.loads(response.text)
        return result.get("replacements", [])
    except Exception as e:
        st.error(f"AI error: {e}")
        return []


def get_mock_replacements(ad_context: str, page_texts: list) -> list:
    replacements = []
    ad_snippet = ad_context[:50].rstrip()
    labels = [
        "Updated headline to reflect ad messaging",
        "Refined supporting copy to align with your ad",
        "Updated call-to-action to match your ad",
        "Adjusted value proposition for ad audience",
        "Personalized section copy for ad context",
    ]
    for i, text in enumerate(page_texts[:5]):
        if len(text) > 15:
            if i == 0:
                replacements.append({
                    "old_text": text,
                    "new_text": f"{ad_snippet} — Discover How We Can Help You",
                    "change_summary": labels[0],
                })
            elif i == 1:
                replacements.append({
                    "old_text": text,
                    "new_text": f"Built for teams who want results: {ad_snippet}",
                    "change_summary": labels[1],
                })
            elif i == 2:
                replacements.append({
                    "old_text": text,
                    "new_text": "Get Started Free — See Results in 14 Days 🎯",
                    "change_summary": labels[2],
                })
            elif i == 3:
                replacements.append({
                    "old_text": text,
                    "new_text": "Trusted by 10,000+ teams who chose speed & reliability",
                    "change_summary": labels[3],
                })
            elif i == 4:
                replacements.append({
                    "old_text": text,
                    "new_text": "Why wait? Your competitors already made the switch.",
                    "change_summary": labels[4],
                })
    return replacements


def apply_replacements(html_content: str, replacements: list) -> tuple:
    soup = BeautifulSoup(html_content, "html.parser")
    applied = 0
    for rep in replacements:
        old_val = rep["old_text"].strip()
        new_val = rep["new_text"]
        if not old_val:
            continue
        for text_node in soup.find_all(string=True):
            if text_node.parent.name in ("script", "style", "[document]"):
                continue
            if old_val in text_node:
                text_node.replace_with(text_node.replace(old_val, new_val))
                applied += 1
    return str(soup), applied


def friendly_change_label(rep: dict) -> str:
    if "change_summary" in rep and rep["change_summary"]:
        return rep["change_summary"]
    old_lower = rep["old_text"].lower()
    if any(kw in old_lower for kw in ["get started", "try", "sign up", "buy", "start", "learn more"]):
        return "Updated call-to-action to match your ad"
    if len(rep["old_text"]) < 80:
        return "Updated headline to reflect ad messaging"
    return "Refined supporting copy to align with your ad"


# ══════════════════════════════════════════════════════════════════════════════
# INPUT SECTION
# ══════════════════════════════════════════════════════════════════════════════

st.markdown('<p class="input-label">Your Ad Creative</p>', unsafe_allow_html=True)
ad_creative = st.text_area(
    "ad_creative",
    value=(
        "Tired of slow websites killing your conversions? "
        "Our ultra-fast CDN boosts load speed by 3× and lifts conversion rates 20%. "
        "Try free for 14 days!"
    ),
    height=120,
    label_visibility="collapsed",
    placeholder="Paste your ad copy or hook here…",
)

st.markdown('<p class="input-label">Landing Page URL</p>', unsafe_allow_html=True)
target_url = st.text_input(
    "target_url",
    value="https://example.com",
    label_visibility="collapsed",
    placeholder="https://your-landing-page.com",
)

st.markdown("")
generate_btn = st.button("🚀  Optimize Page for This Ad", type="primary", use_container_width=True)

# ── Advanced Settings (collapsed) ────────────────────────────────────────────
with st.expander("Advanced Settings ⚙️"):
    api_key_input = st.text_input(
        "Gemini API Key",
        value=os.environ.get("GEMINI_API_KEY", ""),
        type="password",
        help="Required for real AI-powered optimizations. Get a free key from Google AI Studio.",
    )
    st.markdown("""
    <div class="api-info">
        <strong>What does the Gemini API key do?</strong><br>
        The API key connects this app to Google's Gemini AI. The AI reads your ad creative 
        and the landing page content, then intelligently rewrites headlines, CTAs, and copy 
        to match your ad's messaging — like having a CRO expert on demand.<br><br>
        <strong>Without a key:</strong> The app runs in demo mode with sample changes.<br>
        <strong>With a key:</strong> You get real, AI-generated personalizations tailored to your ad.<br><br>
        👉 <a href="https://aistudio.google.com/apikey" target="_blank">Get a free API key here</a> (takes 30 seconds)
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PROCESSING
# ══════════════════════════════════════════════════════════════════════════════

if generate_btn:
    if not target_url:
        st.error("Please enter a landing page URL to continue.")
        st.stop()

    with st.spinner("Analyzing your page and applying improvements…"):
        debug_log = []
        try:
            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0.0.0 Safari/537.36"
                )
            }
            resp = requests.get(target_url, headers=headers, timeout=15)
            resp.raise_for_status()
            original_html = resp.text
            debug_log.append(f"✔ Fetched {len(original_html):,} bytes from {target_url}")
        except Exception as e:
            st.error(f"We couldn't reach that URL. Please double-check and try again.\n\n`{e}`")
            st.stop()

        soup = BeautifulSoup(original_html, "html.parser")
        page_texts = extract_meaningful_text(soup)
        debug_log.append(f"✔ Extracted {len(page_texts)} content sections")

        use_live = api_key_input and len(api_key_input) > 10
        if use_live:
            replacements = call_gemini(api_key_input, ad_creative, page_texts)
            debug_log.append("✔ Gemini AI generated optimizations")
        else:
            replacements = get_mock_replacements(ad_creative, page_texts)
            debug_log.append("✔ Demo mode — used sample improvements")

        if not replacements:
            st.warning("The optimizer didn't find content to improve on this page. Try a different URL with more text content.")
            st.stop()

        modified_html, applied = apply_replacements(original_html, replacements)
        debug_log.append(f"✔ Applied {applied} improvements")

        mod_soup = BeautifulSoup(modified_html, "html.parser")
        if mod_soup.head and not mod_soup.head.find("base"):
            base_tag = mod_soup.new_tag("base", href=target_url)
            mod_soup.head.insert(0, base_tag)
        final_html = str(mod_soup)

    st.session_state.results = {
        "replacements": replacements,
        "applied": applied,
        "final_html": final_html,
        "target_url": target_url,
        "page_texts": page_texts,
        "debug_log": debug_log,
        "used_ai": use_live,
    }


# ══════════════════════════════════════════════════════════════════════════════
# RESULTS SECTION
# ══════════════════════════════════════════════════════════════════════════════

if st.session_state.results:
    r = st.session_state.results
    replacements = r["replacements"]
    applied = r["applied"]
    final_html = r["final_html"]
    url = r["target_url"]
    page_texts = r["page_texts"]
    debug_log = r["debug_log"]
    used_ai = r.get("used_ai", False)

    st.markdown('<hr class="soft-divider">', unsafe_allow_html=True)

    # ── Success Banner ───────────────────────────────────────────────────
    mode_label = "AI-powered" if used_ai else "Demo"
    st.markdown(f"""
    <div class="result-banner">
        <div class="icon">🎯</div>
        <h3>Your page has been optimized to match your ad</h3>
        <p>{len(replacements)} improvement{"s" if len(replacements) != 1 else ""} applied · {mode_label} mode</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Changes Summary ──────────────────────────────────────────────────
    st.markdown("#### What we changed")

    for i, rep in enumerate(replacements, 1):
        label = friendly_change_label(rep)
        old_display = rep["old_text"][:140] + ("…" if len(rep["old_text"]) > 140 else "")
        new_display = rep["new_text"][:140] + ("…" if len(rep["new_text"]) > 140 else "")

        st.markdown(f"""
        <div class="change-card">
            <span class="change-num">{i}</span>
            <span class="change-title">{label}</span>
            <div class="before-after">
                <div class="ba-box ba-before">
                    <div class="ba-label">Before</div>
                    {old_display}
                </div>
                <div class="ba-box ba-after">
                    <div class="ba-label">After</div>
                    {new_display}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Optimized Page Preview ───────────────────────────────────────────
    st.markdown('<hr class="soft-divider">', unsafe_allow_html=True)
    st.markdown("#### Optimized Page Preview")

    st.markdown(f"""
    <div class="preview-frame">
        <div class="preview-bar">
            <span class="preview-dot dot-red"></span>
            <span class="preview-dot dot-yellow"></span>
            <span class="preview-dot dot-green"></span>
            <span class="preview-url">{url}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.components.v1.html(final_html, height=650, scrolling=True)

    # ── Debug Log ────────────────────────────────────────────────────────
    with st.expander("Debug Log 🔍"):
        for line in debug_log:
            st.text(line)
        st.markdown("**Raw Replacement Rules (JSON)**")
        clean_reps = [{"old_text": r["old_text"], "new_text": r["new_text"]} for r in replacements]
        st.json(clean_reps)
        st.markdown("**Extracted Page Texts**")
        for idx, t in enumerate(page_texts, 1):
            st.text(f"{idx}. {t}")
else:
    st.markdown("")
    st.info("👆 Paste your ad copy and a landing page URL, then click **Optimize** to see the personalized page.")
