# app.py
# FREE Streamlit RPA Simulator for Call Center WFM (learn RPA using dummy data)
# Run: streamlit run app.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from io import BytesIO
import time

# -----------------------------
# Page setup
# -----------------------------
st.set_page_config(
    page_title="WFM RPA Simulator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# MODERN CSS SYSTEM
# ============================================================
st.markdown("""
<style>
/* ── Reset & Base ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600&display=swap');

:root {
    --cyan: #00e5ff;
    --cyan-dim: rgba(0, 229, 255, 0.12);
    --cyan-glow: rgba(0, 229, 255, 0.25);
    --violet: #8b5cf6;
    --violet-dim: rgba(139, 92, 246, 0.12);
    --magenta: #e040fb;
    --magenta-dim: rgba(224, 64, 251, 0.10);
    --bg-deepest: #060d1f;
    --bg-deep: #0c1631;
    --bg-card: #111d38;
    --bg-card-hover: #152244;
    --bg-surface: #182848;
    --text-primary: #eef2f7;
    --text-secondary: #c0d0e4;
    --text-muted: #6b7fa0;
    --border-subtle: rgba(160, 200, 255, 0.1);
    --border-glow: rgba(0, 229, 255, 0.22);
}

/* ── Page background with subtle grid ── */
.stApp {
    background: linear-gradient(175deg, #0b1628 0%, #0f1e38 30%, #122244 60%, #0e1a34 100%) !important;
    color: #d8e2f0 !important;
}
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        radial-gradient(ellipse 80% 50% at 50% 0%, rgba(0, 229, 255, 0.05) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 80%, rgba(139, 92, 246, 0.04) 0%, transparent 50%),
        linear-gradient(rgba(100, 180, 255, 0.02) 1px, transparent 1px),
        linear-gradient(90deg, rgba(100, 180, 255, 0.02) 1px, transparent 1px);
    background-size: 100% 100%, 100% 100%, 60px 60px, 60px 60px;
    pointer-events: none;
    z-index: 0;
}

/* ── Global text readability ── */
.stApp, .stApp p, .stApp li, .stApp span, .stApp div, .stApp label {
    font-family: 'Inter', sans-serif !important;
}
.stApp p, .stApp li { color: #c8d6e8 !important; font-size: 0.92rem; line-height: 1.65; }
.stApp h1, .stApp h2, .stApp h3 { color: #ffffff !important; }
.stMarkdown p { color: #c8d6e8 !important; }
label, .stSlider label, .stSelectbox label, .stNumberInput label, .stTextInput label,
[data-testid="stWidgetLabel"] p { color: #b8c8dd !important; font-weight: 500 !important; }
.stRadio label span { color: #c8d6e8 !important; }
.stRadio [data-testid="stMarkdownContainer"] p { color: #c8d6e8 !important; }

.block-container { padding-top: 1rem; padding-bottom: 2rem; max-width: 1200px; position: relative; z-index: 1; }
/* ── Hide sidebar completely ── */
[data-testid="stSidebar"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
button[kind="headerNoPadding"] { display: none !important; }
header[data-testid="stHeader"] { background: transparent !important; }

/* ── Hero Section ── */
.hero-wrapper {
    background: linear-gradient(135deg, #0e1a38 0%, #142448 35%, #17285a 60%, #122042 100%);
    border-radius: 24px;
    padding: 48px 44px 40px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
    border: 1px solid rgba(0, 229, 255, 0.15);
    box-shadow: 0 0 80px -20px rgba(0, 229, 255, 0.1), 0 4px 32px -8px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.04);
}
.hero-wrapper::before {
    content: '';
    position: absolute;
    top: -60%;
    right: -15%;
    width: 600px;
    height: 600px;
    background: radial-gradient(circle, rgba(0, 229, 255, 0.1) 0%, rgba(139, 92, 246, 0.06) 40%, transparent 70%);
    pointer-events: none;
}
.hero-wrapper::after {
    content: '';
    position: absolute;
    bottom: -40%;
    left: -10%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(224, 64, 251, 0.07) 0%, transparent 70%);
    pointer-events: none;
}
.hero-title {
    font-family: 'Inter', sans-serif;
    font-size: 2.6rem;
    font-weight: 900;
    background: linear-gradient(135deg, #ffffff 0%, #80f0ff 50%, #00e5ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.15;
    margin-bottom: 10px;
    letter-spacing: -0.02em;
}
.hero-sub {
    font-family: 'Inter', sans-serif;
    font-size: 1.1rem;
    color: var(--text-secondary);
    font-weight: 400;
    max-width: 620px;
    line-height: 1.6;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 14px;
    border-radius: 999px;
    background: var(--cyan-dim);
    border: 1px solid var(--cyan-glow);
    color: var(--cyan);
    font-size: 0.82rem;
    font-weight: 700;
    margin-bottom: 16px;
    letter-spacing: 0.06em;
    text-shadow: 0 0 12px rgba(0, 229, 255, 0.3);
}
.hero-steps {
    display: flex;
    gap: 12px;
    margin-top: 22px;
    flex-wrap: wrap;
}
.hero-step-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 8px 16px;
    border-radius: 12px;
    background: rgba(0, 229, 255, 0.08);
    border: 1px solid rgba(0, 229, 255, 0.18);
    color: #d0f0f8;
    font-size: 0.85rem;
    font-weight: 500;
    backdrop-filter: blur(8px);
    transition: all 0.25s ease;
}
.hero-step-pill:hover {
    background: var(--cyan-dim);
    border-color: var(--cyan-glow);
    color: var(--cyan);
    transform: translateY(-2px);
    box-shadow: 0 4px 20px -6px rgba(0, 229, 255, 0.2);
}

/* ── Navigation Cards ── */
.nav-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 18px;
    margin-bottom: 32px;
}
@media (max-width: 768px) {
    .nav-grid { grid-template-columns: repeat(2, 1fr); }
}
.nav-card {
    background: linear-gradient(160deg, #162545 0%, #112040 100%);
    border: 1px solid rgba(160, 200, 255, 0.14);
    border-radius: 20px;
    padding: 28px 24px;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
    text-decoration: none;
}
.nav-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--cyan), transparent);
    opacity: 0;
    transition: opacity 0.3s ease;
}
.nav-card:hover {
    border-color: rgba(0, 229, 255, 0.35);
    background: linear-gradient(160deg, #1c3058 0%, #162848 100%);
    transform: translateY(-5px);
    box-shadow: 0 20px 50px -15px rgba(0, 229, 255, 0.18), 0 0 40px -10px rgba(0, 229, 255, 0.08);
}
.nav-card:hover::before { opacity: 1; }
.nav-card.active {
    border-color: rgba(0, 229, 255, 0.35);
    background: linear-gradient(160deg, rgba(0, 229, 255, 0.08) 0%, #0e1830 100%);
    box-shadow: 0 8px 32px -8px rgba(0, 229, 255, 0.2);
}
.nav-icon {
    font-size: 2rem;
    margin-bottom: 12px;
    display: block;
}
.nav-label {
    font-family: 'Inter', sans-serif;
    font-size: 1.0rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 6px;
}
.nav-desc {
    font-family: 'Inter', sans-serif;
    font-size: 0.82rem;
    color: var(--text-secondary);
    line-height: 1.5;
}
.nav-arrow {
    position: absolute;
    top: 20px;
    right: 20px;
    color: #4a6080;
    font-size: 1.1rem;
    transition: all 0.3s ease;
}
.nav-card:hover .nav-arrow { color: var(--cyan); transform: translateX(4px); }

/* ── Glass Card ── */
.glass-card {
    background: linear-gradient(160deg, #162545 0%, #112040 100%);
    border: 1px solid rgba(160, 200, 255, 0.1);
    border-radius: 20px;
    padding: 24px 26px;
    backdrop-filter: blur(12px);
    margin-bottom: 16px;
    transition: all 0.25s ease;
}
.glass-card:hover {
    border-color: rgba(0, 229, 255, 0.2);
    background: linear-gradient(160deg, #1a2c50 0%, #142440 100%);
}
.glass-card-accent {
    background: linear-gradient(160deg, rgba(0, 229, 255, 0.07) 0%, #162545 100%);
    border: 1px solid var(--border-glow);
    border-radius: 20px;
    padding: 24px 26px;
    backdrop-filter: blur(12px);
    margin-bottom: 16px;
}

/* ── Metric Cards ── */
.metric-row {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 12px;
    margin-bottom: 24px;
}
@media (max-width: 768px) {
    .metric-row { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
.metric-card {
    background: linear-gradient(160deg, #162545 0%, #112040 100%);
    border: 1px solid rgba(160, 200, 255, 0.1);
    border-radius: 16px;
    padding: 18px 12px;
    text-align: center;
    transition: all 0.25s ease;
    position: relative;
    overflow: visible;
    min-width: 0;
}
.metric-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, rgba(0,229,255,0.3), transparent);
    opacity: 0;
    transition: opacity 0.3s ease;
}
.metric-card:hover {
    border-color: var(--border-glow);
    transform: translateY(-3px);
    box-shadow: 0 12px 36px -10px rgba(0, 229, 255, 0.1);
}
.metric-card:hover::after { opacity: 1; }
.metric-value {
    font-family: 'JetBrains Mono', 'Inter', monospace;
    font-size: 1.6rem;
    font-weight: 800;
    color: var(--text-primary);
    line-height: 1.2;
    word-break: keep-all;
}
.metric-label {
    font-family: 'Inter', sans-serif;
    font-size: 0.7rem;
    color: #b8c8dd;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    font-weight: 600;
    margin-top: 6px;
    line-height: 1.3;
    word-break: keep-all;
}
.metric-card.ok { border-left: 3px solid #00e676; }
.metric-card.ok .metric-value { color: #00e676; text-shadow: 0 0 20px rgba(0, 230, 118, 0.15); }
.metric-card.bad { border-left: 3px solid #ff1744; }
.metric-card.bad .metric-value { color: #ff5252; text-shadow: 0 0 20px rgba(255, 23, 68, 0.15); }
.metric-card.warn { border-left: 3px solid #ffab00; }
.metric-card.warn .metric-value { color: #ffd740; text-shadow: 0 0 20px rgba(255, 171, 0, 0.15); }
.metric-card.info { border-left: 3px solid var(--cyan); }
.metric-card.info .metric-value { color: var(--cyan); text-shadow: 0 0 20px rgba(0, 229, 255, 0.15); }

/* ── Section Headers ── */
.section-header {
    font-family: 'Inter', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 16px;
    padding-bottom: 12px;
    border-bottom: 1px solid rgba(160, 200, 255, 0.08);
    display: flex;
    align-items: center;
    gap: 10px;
}
.section-sub {
    font-family: 'Inter', sans-serif;
    font-size: 0.85rem;
    color: var(--text-secondary);
    margin-bottom: 16px;
}

/* ── Status Banners ── */
.status-banner {
    border-radius: 16px;
    padding: 20px 24px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 14px;
    font-family: 'Inter', sans-serif;
}
.status-ok {
    background: linear-gradient(135deg, rgba(0, 230, 118, 0.08) 0%, rgba(0, 230, 118, 0.02) 100%);
    border: 1px solid rgba(0, 230, 118, 0.2);
    color: #00e676;
}
.status-risk {
    background: linear-gradient(135deg, rgba(255, 23, 68, 0.08) 0%, rgba(255, 23, 68, 0.02) 100%);
    border: 1px solid rgba(255, 82, 82, 0.25);
    color: #ff5252;
}
.status-icon { font-size: 1.5rem; }
.status-text { font-size: 1.05rem; font-weight: 700; }
.status-detail { font-size: 0.85rem; opacity: 0.8; font-weight: 400; }

/* ── Timeline / Use Case Card ── */
.uc-card {
    background: linear-gradient(160deg, #162545 0%, #112040 100%);
    border: 1px solid rgba(160, 200, 255, 0.1);
    border-radius: 18px;
    padding: 22px 24px;
    margin-bottom: 14px;
    transition: all 0.25s ease;
}
.uc-card:hover {
    border-color: var(--border-glow);
    transform: translateX(4px);
    box-shadow: 0 8px 24px -8px rgba(0, 229, 255, 0.1);
}
.uc-title {
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    font-size: 1.0rem;
    color: var(--text-primary);
    margin-bottom: 6px;
}
.uc-goal {
    font-family: 'Inter', sans-serif;
    font-size: 0.85rem;
    color: var(--text-secondary);
    margin-bottom: 10px;
}
.tag {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 4px 10px;
    border-radius: 8px;
    font-size: 0.75rem;
    font-weight: 600;
    margin-right: 6px;
    margin-bottom: 6px;
}
.tag-input { background: rgba(0, 229, 255, 0.08); color: var(--cyan); border: 1px solid rgba(0, 229, 255, 0.15); }
.tag-rule  { background: rgba(255, 171, 0, 0.08); color: #ffd740; border: 1px solid rgba(255, 171, 0, 0.15); }
.tag-output { background: rgba(0, 230, 118, 0.08); color: #00e676; border: 1px solid rgba(0, 230, 118, 0.15); }
.tag-action { background: rgba(224, 64, 251, 0.08); color: #e040fb; border: 1px solid rgba(224, 64, 251, 0.15); }

/* ── Bot Progress ── */
.bot-step {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 16px;
    border-radius: 12px;
    margin-bottom: 6px;
    font-family: 'Inter', sans-serif;
    font-size: 0.88rem;
    transition: all 0.3s ease;
}
.bot-step-done {
    background: rgba(0, 230, 118, 0.06);
    border: 1px solid rgba(0, 230, 118, 0.12);
    color: #00e676;
}
.bot-step-active {
    background: var(--cyan-dim);
    border: 1px solid var(--cyan-glow);
    color: var(--cyan);
    animation: pulse-step 1.5s ease-in-out infinite;
}
@keyframes pulse-step {
    0%, 100% { opacity: 0.7; box-shadow: 0 0 0 0 rgba(0, 229, 255, 0); }
    50% { opacity: 1; box-shadow: 0 0 16px -4px rgba(0, 229, 255, 0.15); }
}

/* ── Glossary ── */
.glossary-item {
    padding: 18px 22px;
    border-radius: 14px;
    background: linear-gradient(160deg, #162545 0%, #112040 100%);
    border: 1px solid rgba(160, 200, 255, 0.1);
    margin-bottom: 12px;
    transition: all 0.25s ease;
}
.glossary-item:hover {
    border-color: var(--border-glow);
    box-shadow: 0 8px 24px -8px rgba(0, 229, 255, 0.08);
}
.glossary-term {
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    font-size: 0.95rem;
    color: var(--cyan);
    margin-bottom: 4px;
}
.glossary-def {
    font-family: 'Inter', sans-serif;
    font-size: 0.85rem;
    color: var(--text-secondary);
    line-height: 1.5;
}

/* ── Run Button ── */
.stButton > button {
    background: linear-gradient(135deg, #00b8d4 0%, #0097a7 40%, #00838f 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 14px 28px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1.0rem !important;
    letter-spacing: 0.02em !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 4px 20px -4px rgba(0, 229, 255, 0.35) !important;
    text-shadow: 0 1px 2px rgba(0,0,0,0.2) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px -4px rgba(0, 229, 255, 0.45) !important;
    background: linear-gradient(135deg, #00e5ff 0%, #00b8d4 40%, #0097a7 100%) !important;
}

/* ── Download Button ── */
.stDownloadButton > button {
    background: linear-gradient(135deg, #162545 0%, #112040 100%) !important;
    border: 1px solid var(--border-glow) !important;
    border-radius: 12px !important;
    color: var(--cyan) !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    transition: all 0.25s ease !important;
}
.stDownloadButton > button:hover {
    border-color: rgba(0, 229, 255, 0.45) !important;
    background: linear-gradient(135deg, rgba(0, 229, 255, 0.1) 0%, #162545 100%) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px -6px rgba(0, 229, 255, 0.15) !important;
}

/* ── Selectbox / Slider ── */
.stSelectbox > div > div { border-radius: 12px !important; }
/* ── Toggle section titles ── */
.toggle-section-title {
    font-family: 'Inter', sans-serif;
    font-size: 0.88rem;
    font-weight: 700;
    color: #d8e2f0;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin: 20px 0 6px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.toggle-section-title .toggle-icon {
    font-size: 1rem;
}
.toggle-section-box {
    background: linear-gradient(160deg, #162545 0%, #112040 100%);
    border: 1px solid rgba(160, 200, 255, 0.10);
    border-radius: 14px;
    padding: 16px;
    margin-bottom: 12px;
}

/* ── Dataframe ── */
.stDataFrame { border-radius: 14px; overflow: hidden; }

/* ── Footer ── */
.footer {
    text-align: center;
    padding: 28px 0 12px;
    color: var(--text-secondary);
    font-size: 0.78rem;
    font-family: 'Inter', sans-serif;
    border-top: 1px solid var(--border-subtle);
    margin-top: 40px;
}

/* ── Learning Path ── */
.path-step {
    display: flex;
    align-items: flex-start;
    gap: 14px;
    padding: 14px 0;
    border-bottom: 1px solid rgba(160, 200, 255, 0.06);
}
.path-step:last-child { border-bottom: none; }
.path-dot {
    width: 32px;
    height: 32px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.8rem;
    font-weight: 800;
    color: white;
    flex-shrink: 0;
}
.path-dot-1 { background: linear-gradient(135deg, #00e5ff, #0097a7); }
.path-dot-2 { background: linear-gradient(135deg, #448aff, #2962ff); }
.path-dot-3 { background: linear-gradient(135deg, #00e676, #00c853); }
.path-dot-4 { background: linear-gradient(135deg, #ffab00, #ff6d00); }
.path-dot-5 { background: linear-gradient(135deg, #e040fb, #aa00ff); }
.path-label {
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: 0.9rem;
    color: var(--text-primary);
}
.path-desc {
    font-family: 'Inter', sans-serif;
    font-size: 0.8rem;
    color: var(--text-secondary);
}

/* ── Divider ── */
.spacer { height: 12px; }
.spacer-lg { height: 28px; }

/* ── Back Button ── */
.back-btn {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 8px 18px;
    border-radius: 10px;
    background: rgba(0, 229, 255, 0.04);
    border: 1px solid rgba(0, 229, 255, 0.1);
    color: var(--text-secondary);
    font-size: 0.85rem;
    font-weight: 500;
    cursor: pointer;
    text-decoration: none;
    margin-bottom: 16px;
    transition: all 0.2s ease;
}
.back-btn:hover {
    background: var(--cyan-dim);
    border-color: var(--cyan-glow);
    color: var(--cyan);
}

/* ── PRO CTA CARD ── */
.pro-card-wrapper {
    position: relative;
    border-radius: 22px;
    padding: 2px;
    background: linear-gradient(135deg, var(--cyan), var(--violet), var(--magenta), var(--cyan));
    background-size: 300% 300%;
    animation: gradient-border 6s ease infinite;
    margin-bottom: 16px;
    box-shadow: 0 0 40px -12px rgba(0, 229, 255, 0.2), 0 0 40px -12px rgba(224, 64, 251, 0.1);
}
@keyframes gradient-border {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
.pro-card-inner {
    background: linear-gradient(160deg, #112040 0%, #152444 40%, #112038 100%);
    border-radius: 20px;
    padding: 28px 30px;
    position: relative;
    overflow: hidden;
}
.pro-card-inner::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(0, 229, 255, 0.06) 0%, rgba(224, 64, 251, 0.03) 50%, transparent 70%);
    pointer-events: none;
}
.pro-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px 12px;
    border-radius: 8px;
    background: linear-gradient(135deg, rgba(224, 64, 251, 0.15), rgba(0, 229, 255, 0.15));
    border: 1px solid rgba(224, 64, 251, 0.25);
    color: #e040fb;
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 14px;
}
.pro-title {
    font-family: 'Inter', sans-serif;
    font-weight: 800;
    font-size: 1.15rem;
    color: var(--text-primary);
    margin-bottom: 10px;
    line-height: 1.3;
}
.pro-desc {
    font-family: 'Inter', sans-serif;
    font-size: 0.88rem;
    color: var(--text-secondary);
    line-height: 1.6;
    margin-bottom: 16px;
}
.pro-features {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 18px;
}
.pro-feature-tag {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 6px 12px;
    border-radius: 10px;
    background: rgba(139, 92, 246, 0.08);
    border: 1px solid rgba(139, 92, 246, 0.18);
    color: #b39ddb;
    font-size: 0.8rem;
    font-weight: 600;
    transition: all 0.2s ease;
}
.pro-feature-tag:hover {
    background: rgba(139, 92, 246, 0.15);
    border-color: rgba(139, 92, 246, 0.3);
    transform: translateY(-1px);
}
.pro-email-row {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 14px 18px;
    border-radius: 14px;
    background: linear-gradient(135deg, rgba(0, 229, 255, 0.06) 0%, rgba(224, 64, 251, 0.04) 100%);
    border: 1px solid rgba(0, 229, 255, 0.12);
}
.pro-email-icon {
    font-size: 1.3rem;
    flex-shrink: 0;
}
.pro-email-text {
    font-family: 'Inter', sans-serif;
    font-size: 0.85rem;
    color: var(--text-secondary);
}
.pro-email-link {
    color: var(--cyan);
    font-weight: 700;
    text-decoration: none;
    transition: all 0.2s ease;
    text-shadow: 0 0 10px rgba(0, 229, 255, 0.2);
}
.pro-email-link:hover {
    color: #80f0ff;
    text-shadow: 0 0 16px rgba(0, 229, 255, 0.4);
}

/* ── Pros & Cons Cards ── */
.proscons-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin-bottom: 20px;
}
@media (max-width: 768px) {
    .proscons-grid { grid-template-columns: 1fr; }
}
.pros-card {
    background: linear-gradient(160deg, rgba(0, 230, 118, 0.06) 0%, #162545 100%);
    border: 1px solid rgba(0, 230, 118, 0.18);
    border-radius: 18px;
    padding: 22px 24px;
}
.cons-card {
    background: linear-gradient(160deg, rgba(255, 171, 0, 0.05) 0%, #162545 100%);
    border: 1px solid rgba(255, 171, 0, 0.15);
    border-radius: 18px;
    padding: 22px 24px;
}
.limits-card {
    background: linear-gradient(160deg, rgba(255, 82, 82, 0.05) 0%, #162545 100%);
    border: 1px solid rgba(255, 82, 82, 0.15);
    border-radius: 18px;
    padding: 22px 24px;
}
.pc-title {
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    font-size: 1.0rem;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.pc-title.green { color: #00e676; }
.pc-title.amber { color: #ffd740; }
.pc-title.red   { color: #ff7043; }
.pc-item {
    font-family: 'Inter', sans-serif;
    font-size: 0.85rem;
    color: #c8d6e8;
    padding: 6px 0;
    line-height: 1.5;
    display: flex;
    align-items: flex-start;
    gap: 8px;
}
.pc-icon { flex-shrink: 0; font-size: 0.85rem; margin-top: 1px; }
</style>
""", unsafe_allow_html=True)


# ============================================================
# HELPERS
# ============================================================
def _now_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log_add(logs, msg):
    logs.append(f"[{_now_str()}] {msg}")

def bytes_download_excel(dfs: dict, filename: str):
    bio = BytesIO()
    with pd.ExcelWriter(bio, engine="openpyxl") as writer:
        for sheet, df in dfs.items():
            df.to_excel(writer, sheet_name=sheet[:31], index=False)
    bio.seek(0)
    st.download_button(
        "📥  Download Excel Report",
        data=bio.getvalue(),
        file_name=filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )

def bytes_download_csv(df: pd.DataFrame, filename: str):
    bio = BytesIO()
    bio.write(df.to_csv(index=False).encode("utf-8"))
    bio.seek(0)
    st.download_button(
        "📥  Download CSV",
        data=bio.getvalue(),
        file_name=filename,
        mime="text/csv",
        use_container_width=True,
    )

def make_intervals(start_dt: datetime, periods: int = 48, minutes: int = 30):
    times = [start_dt + timedelta(minutes=minutes * i) for i in range(periods)]
    return pd.DataFrame({
        "interval_start": times,
        "interval_label": [t.strftime("%H:%M") for t in times]
    })

def make_dummy_intraday(periods=48, seed=42):
    np.random.seed(seed)
    base = make_intervals(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
                          periods=periods, minutes=30)
    hour = base["interval_start"].dt.hour + base["interval_start"].dt.minute / 60
    curve = 0.6 * np.exp(-((hour - 12) / 4.2) ** 2) + 0.5 * np.exp(-((hour - 19) / 3.5) ** 2) + 0.25
    volume_fcst = (curve * 800 + np.random.normal(0, 35, size=periods)).clip(50).round()
    aht_sec = (np.random.normal(420, 35, size=periods)).clip(240, 650).round()
    workload_sec = (volume_fcst * aht_sec).astype(int)
    shrink = (np.random.normal(0.28, 0.04, size=periods)).clip(0.15, 0.45)
    base_needed = (workload_sec / 1800)
    needed_staff = (base_needed / (1 - shrink)).clip(1).round().astype(int)
    volume_act = (volume_fcst * np.random.normal(1.0, 0.06, size=periods) + np.random.normal(0, 18, size=periods)).clip(20).round()
    staff_act = (needed_staff * np.random.normal(0.98, 0.07, size=periods) + np.random.normal(0, 2.0, size=periods)).clip(0).round().astype(int)
    gap = staff_act - needed_staff
    asa = (np.maximum(10, 25 + (-gap.clip(upper=0)) * 18 + np.random.normal(0, 6, size=periods))).round().astype(int)
    sl = (np.clip(0.92 + (gap / needed_staff.replace(0, 1)) * 0.35 - (asa / 300) * 0.25 + np.random.normal(0, 0.03, size=periods), 0.05, 0.99) * 100).round(1)
    df = pd.DataFrame({
        "interval_start": base["interval_start"],
        "interval_label": base["interval_label"],
        "volume_fcst": volume_fcst.astype(int),
        "volume_act": volume_act.astype(int),
        "aht_sec": aht_sec.astype(int),
        "shrinkage": (shrink * 100).round(1),
        "needed_staff": needed_staff,
        "actual_staff": staff_act,
        "staffing_gap": (staff_act - needed_staff).astype(int),
        "asa_sec_est": asa,
        "service_level_est_pct": sl,
    })
    return df

def make_dummy_adherence(n_agents=120, seed=42):
    np.random.seed(seed)
    agents = [f"A{str(i).zfill(4)}" for i in range(1, n_agents + 1)]
    tenure = np.random.choice(["New", "Mid", "Tenured"], size=n_agents, p=[0.30, 0.45, 0.25])
    sched_min = np.random.choice([240, 300, 360, 420, 480], size=n_agents, p=[0.05, 0.10, 0.30, 0.30, 0.25])
    base = np.where(tenure == "Tenured", 0.92, np.where(tenure == "Mid", 0.88, 0.83))
    adher = np.clip(base + np.random.normal(0, 0.05, size=n_agents), 0.55, 0.98)
    out = (sched_min * (1 - adher)).round().astype(int)
    df = pd.DataFrame({
        "agent_id": agents,
        "tenure_band": tenure,
        "scheduled_minutes": sched_min,
        "adherence_pct": (adher * 100).round(1),
        "out_of_adherence_minutes": out,
    })
    reasons = ["Late In", "Extended Break", "Meeting Overrun", "System Issue", "Unplanned Aux", "Training Overrun"]
    df["top_reason"] = np.where(df["adherence_pct"] < 85, np.random.choice(reasons, size=n_agents), "OK")
    return df.sort_values(["adherence_pct", "out_of_adherence_minutes"], ascending=[True, False])

def make_dummy_shrinkage(days=14, seed=42):
    np.random.seed(seed)
    dates = [datetime.now().date() - timedelta(days=i) for i in range(days)][::-1]
    planned = np.clip(np.random.normal(0.30, 0.02, size=days), 0.22, 0.38)
    actual = np.clip(planned + np.random.normal(0.01, 0.02, size=days), 0.18, 0.45)
    df = pd.DataFrame({
        "date": dates,
        "planned_shrinkage_pct": (planned * 100).round(1),
        "actual_shrinkage_pct": (actual * 100).round(1),
        "variance_pp": ((actual - planned) * 100).round(1),
    })
    return df

def rpa_steps_simulator(step_titles, logs, speed=0.25, container=None):
    target = container or st
    prog = target.progress(0, text="Initializing bot...")
    status_area = target.empty()
    for i, title in enumerate(step_titles, start=1):
        log_add(logs, f"Step {i}/{len(step_titles)}: {title}")
        pct = int(i / len(step_titles) * 100)
        prog.progress(pct, text=f"Step {i}/{len(step_titles)}: {title}")
        step_html = ""
        for j, s in enumerate(step_titles[:i], start=1):
            icon = "✅" if j < i else "⚡"
            cls = "bot-step-done" if j < i else "bot-step-active"
            step_html += f"<div class='bot-step {cls}'>{icon} <b>Step {j}</b> &mdash; {s}</div>"
        status_area.markdown(step_html, unsafe_allow_html=True)
        time.sleep(speed)
    prog.empty()
    # Final all-done
    done_html = ""
    for j, s in enumerate(step_titles, start=1):
        done_html += f"<div class='bot-step bot-step-done'>✅ <b>Step {j}</b> &mdash; {s}</div>"
    status_area.markdown(done_html, unsafe_allow_html=True)


def render_metric_row(metrics):
    """metrics = [(value, label, style_class), ...]"""
    html = "<div class='metric-row'>"
    for val, label, cls in metrics:
        html += f"<div class='metric-card {cls}'><div class='metric-value'>{val}</div><div class='metric-label'>{label}</div></div>"
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def plotly_theme(fig):
    """Apply consistent dark tech theme to plotly figures."""
    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor="rgba(10,18,36,0.6)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", size=12, color="#d0dff0"),
        title_font=dict(family="Inter, sans-serif", size=15, color="#ffffff"),
        margin=dict(l=24, r=24, t=50, b=24),
        legend=dict(
            bgcolor="rgba(16,28,52,0.85)",
            borderwidth=0,
            font=dict(size=11, color="#d8e2f0"),
            orientation="h",
            yanchor="bottom",
            y=-0.22,
            xanchor="center",
            x=0.5,
        ),
        xaxis=dict(
            gridcolor="rgba(0,229,255,0.04)",
            zerolinecolor="rgba(0,229,255,0.08)",
            title_font=dict(color="#c8d6e8"),
            tickfont=dict(color="#b0c4de"),
        ),
        yaxis=dict(
            gridcolor="rgba(0,229,255,0.04)",
            zerolinecolor="rgba(0,229,255,0.08)",
            title_font=dict(color="#c8d6e8"),
            tickfont=dict(color="#b0c4de"),
        ),
    )
    return fig


# ============================================================
# SESSION STATE
# ============================================================
if "seed" not in st.session_state:
    st.session_state.seed = 42
if "logs" not in st.session_state:
    st.session_state.logs = []
if "page" not in st.session_state:
    st.session_state.page = "home"


def nav_to(page_name):
    st.session_state.page = page_name


# ============================================================
# SIDEBAR (minimal — supplementary info)
# ============================================================
# Sidebar removed — seed input moved into Simulator config panel


# ============================================================
# HERO HEADER (always visible)
# ============================================================
page = st.session_state.page

if page == "home":
    # ── Hero ──
    st.markdown("""
    <div class="hero-wrapper">
        <div class="hero-badge">🤖 WFM RPA SIMULATOR</div>
        <div class="hero-title">RPA in Workforce Management:<br>Watch It Run — Learn Through Simulators</div>
        <div class="hero-sub">
            This interactive simulator teaches how an RPA bot works in call center WFM using safe dummy data.
            No code, no risk — just play, learn, and understand.
        </div>
        <div class="hero-steps">
            <div class="hero-step-pill">📥 Get Data</div>
            <div class="hero-step-pill">🧮 Compute Rules</div>
            <div class="hero-step-pill">🚦 Decide</div>
            <div class="hero-step-pill">📤 Act</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Navigation Cards ──
    st.markdown("<div class='section-header'>🧭 Where do you want to go?</div>", unsafe_allow_html=True)

    nav_cols = st.columns(4, gap="medium")
    nav_items = [
        ("guide", "📖", "Start Here", "Learn how the simulator works and what RPA means in WFM.", nav_cols[0]),
        ("library", "📚", "Use Case Library", "Browse 5 real WFM bot ideas with inputs, rules & outputs.", nav_cols[1]),
        ("simulator", "🧪", "Simulator", "Run a fake bot with dummy data and see the full pipeline.", nav_cols[2]),
        ("glossary", "❓", "RPA Glossary", "Quick reference of RPA and WFM terms in plain language.", nav_cols[3]),
    ]

    for key, icon, label, desc, col in nav_items:
        with col:
            st.markdown(f"""
            <div class="nav-card" id="nav-{key}">
                <span class="nav-arrow">→</span>
                <span class="nav-icon">{icon}</span>
                <div class="nav-label">{label}</div>
                <div class="nav-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Open {label}", key=f"btn_{key}", use_container_width=True):
                nav_to(key)
                st.rerun()

    st.markdown("<div class='spacer-lg'></div>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════
    # INTERACTIVE: Live Scenario Preview
    # ══════════════════════════════════════════════════════════
    st.markdown("<div class='section-header'>⚡ Live Scenario Preview</div>", unsafe_allow_html=True)
    st.markdown("<p style='color:#c8d6e8; font-size:0.9rem; margin-top:-10px; margin-bottom:16px;'>Change the scenario or threshold and watch the data update instantly.</p>", unsafe_allow_html=True)

    ctrl1, ctrl2, ctrl3 = st.columns([0.3, 0.35, 0.35], gap="medium")
    with ctrl1:
        st.markdown("<div class='glass-card' style='padding:18px 20px;'>", unsafe_allow_html=True)
        preview_seed = st.number_input(
            "🎲 Scenario Seed", min_value=1, max_value=9999,
            value=int(st.session_state.seed), key="home_seed",
            help="Each seed = a unique scenario. Try different numbers!"
        )
        if preview_seed != st.session_state.seed:
            st.session_state.seed = preview_seed
        if st.button("🔀 Randomize Scenario", key="randomize_btn", use_container_width=True):
            st.session_state.seed = int(np.random.randint(1, 9999))
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with ctrl2:
        st.markdown("<div class='glass-card' style='padding:18px 20px;'>", unsafe_allow_html=True)
        home_sl = st.slider("🎯 Service Level Target (%)", 60, 95, 80, 1, key="home_sl")
        home_gap = st.slider("👥 Staffing Gap Alert", 1, 20, 5, 1, key="home_gap")
        st.markdown("</div>", unsafe_allow_html=True)

    with ctrl3:
        # Live stats from current seed
        preview_df = make_dummy_intraday(periods=48, seed=int(st.session_state.seed))
        preview_df["is_risk"] = (
            (preview_df["staffing_gap"] <= -home_gap) |
            (preview_df["service_level_est_pct"] < home_sl)
        )
        n_risk = preview_df["is_risk"].sum()
        avg_sl = preview_df["service_level_est_pct"].mean()
        worst_gap = preview_df["staffing_gap"].min()
        total_vol = preview_df["volume_act"].sum()

        risk_cls = "bad" if n_risk > 10 else "warn" if n_risk > 3 else "ok"
        sl_cls = "ok" if avg_sl >= home_sl else "warn" if avg_sl >= home_sl - 5 else "bad"

        render_metric_row([
            (f"{n_risk}", "Risk Intervals", risk_cls),
            (f"{avg_sl:.1f}%", "Avg Service Level", sl_cls),
            (f"{worst_gap:+d}", "Worst Gap", "bad" if worst_gap < -home_gap else "ok"),
            (f"{total_vol:,}", "Total Calls", "info"),
        ])

    # ── Live Mini Chart ──
    ch_left, ch_right = st.columns(2, gap="medium")
    with ch_left:
        fig_preview = go.Figure()
        fig_preview.add_trace(go.Scatter(
            x=preview_df["interval_label"], y=preview_df["service_level_est_pct"],
            name="Service Level %",
            line=dict(color="#00e5ff", width=2.5),
            fill="tozeroy", fillcolor="rgba(0,229,255,0.06)"
        ))
        fig_preview.add_hline(y=home_sl, line_dash="dash", line_color="#ffd740",
                              annotation_text=f"Target ({home_sl}%)")
        fig_preview.update_layout(title="Service Level — Live Preview", height=280)
        plotly_theme(fig_preview)
        st.plotly_chart(fig_preview, use_container_width=True)

    with ch_right:
        gap_colors = ["#ff5252" if g <= -home_gap else "#00e676" if g >= 0 else "#ffd740" for g in preview_df["staffing_gap"]]
        fig_gap_preview = go.Figure(go.Bar(
            x=preview_df["interval_label"], y=preview_df["staffing_gap"],
            marker_color=gap_colors
        ))
        fig_gap_preview.add_hline(y=-home_gap, line_dash="dash", line_color="#ff5252",
                                  annotation_text=f"Alert (-{home_gap})")
        fig_gap_preview.update_layout(title="Staffing Gap — Live Preview", height=280)
        plotly_theme(fig_gap_preview)
        st.plotly_chart(fig_gap_preview, use_container_width=True)

    # ── Quick Health Check Demo ──
    st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

    qc1, qc2 = st.columns([0.6, 0.4], gap="large")
    with qc1:
        st.markdown("<div class='section-header'>🏥 Quick Health Check</div>", unsafe_allow_html=True)
        st.markdown("<p style='color:#c8d6e8; font-size:0.88rem; margin-top:-10px;'>Click below to run a 3-second bot check using the current scenario. See what the bot would flag.</p>", unsafe_allow_html=True)
        if st.button("⚡ Run Quick Health Check", key="quick_check", use_container_width=True):
            with st.spinner("Bot is scanning intervals..."):
                time.sleep(0.8)
            # Compute results
            qdf = preview_df.copy()
            qdf["flag"] = qdf["is_risk"]
            risk_rows = qdf[qdf["flag"]]
            if len(risk_rows) == 0:
                st.markdown("""
                <div class="status-banner status-ok">
                    <span class="status-icon">✅</span>
                    <div><div class="status-text">ALL CLEAR</div><div class="status-detail">No risk intervals. Your scenario looks healthy!</div></div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="status-banner status-risk">
                    <span class="status-icon">🚨</span>
                    <div><div class="status-text">{len(risk_rows)} Risk Intervals Found</div><div class="status-detail">Bot would alert the intraday team. Try the full Simulator for details.</div></div>
                </div>""", unsafe_allow_html=True)
                # Show top 5 worst
                worst = risk_rows.nsmallest(5, "service_level_est_pct")
                for _, r in worst.iterrows():
                    parts = []
                    if r["staffing_gap"] <= -home_gap:
                        parts.append(f"Gap **{int(r['staffing_gap'])}**")
                    if r["service_level_est_pct"] < home_sl:
                        parts.append(f"SL **{r['service_level_est_pct']}%**")
                    st.markdown(f"- **{r['interval_label']}**: {' · '.join(parts)}")

            st.markdown("")
            if st.button("🧪 Open Full Simulator for deeper analysis", key="qc_to_sim", use_container_width=True):
                nav_to("simulator")
                st.rerun()

    with qc2:
        st.markdown("<div class='section-header'>🎯 What is RPA?</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="glass-card-accent" style="padding:22px 24px;">
            <div style="font-size:0.92rem; color:#eef2f7; line-height:1.7;">
                <b>Repeatable steps + rules + automatic actions.</b>
            </div>
            <div style="margin-top:12px; font-size:0.85rem; color:#c8d6e8; line-height:1.7;">
                <b style="color:#00e5ff;">📥 Get</b> data →
                <b style="color:#ffd740;">🧮 Compute</b> rules →
                <b style="color:#e040fb;">🚦 Decide</b> →
                <b style="color:#00e676;">📤 Act</b>
            </div>
            <div style="margin-top:14px; font-size:0.82rem; color:#c8d6e8; line-height:1.6;">
                Can be low-code (UiPath, Power Automate) or Python scripts on a schedule.
                Every WFM bot follows this same pattern.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="glass-card" style="padding:18px 22px;">
            <div style="font-weight:700; color:#eef2f7; font-size:0.9rem; margin-bottom:8px;">🧪 Safe Sandbox</div>
            <div style="font-size:0.82rem; color:#c8d6e8; line-height:1.6;">
                All data is randomly generated. No real systems are touched.
                Hit <b style="color:#00e5ff;">Randomize</b> above to get a brand new scenario.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Pro Features CTA Card (highlighted) ──
    st.markdown("<div class='spacer-lg'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="pro-card-wrapper">
        <div class="pro-card-inner">
            <div class="pro-badge">⚡ ADVANCED FEATURES</div>
            <div class="pro-title">Need more power? Unlock the full WFM RPA platform.</div>
            <div class="pro-desc">
                This free simulator covers the basics. For production-ready automation — including
                visual bot building, live system connectors, and a full rules editor — reach out to our team.
            </div>
            <div class="pro-features">
                <div class="pro-feature-tag">🔧 Bot Builder</div>
                <div class="pro-feature-tag">🔌 Connectors</div>
                <div class="pro-feature-tag">📐 Rules Editor</div>
                <div class="pro-feature-tag">📊 BI Integrations</div>
                <div class="pro-feature-tag">🔄 Orchestration</div>
                <div class="pro-feature-tag">🔐 Enterprise SSO</div>
            </div>
            <div class="pro-email-row">
                <span class="pro-email-icon">📧</span>
                <div class="pro-email-text">
                    Interested or need more information? Contact us at
                    <a href="mailto:support@wfmcommons.com" class="pro-email-link">support@wfmcommons.com</a>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='footer'>WFM RPA Simulator — Built for learning. No real data is used or stored.</div>", unsafe_allow_html=True)

# ============================================================
# PAGE: GUIDE
# ============================================================
elif page == "guide":
    if st.button("← Back to Home", key="back_guide"):
        nav_to("home")
        st.rerun()

    st.markdown("""
    <div class="hero-wrapper" style="padding:32px 36px 28px;">
        <div class="hero-badge">📖 GETTING STARTED</div>
        <div class="hero-title" style="font-size:2rem;">How to Use This Simulator</div>
        <div class="hero-sub">Think of it like having a tiny robot helper that does the boring stuff for you every 30 minutes.</div>
    </div>
    """, unsafe_allow_html=True)

    left, right = st.columns([0.58, 0.42], gap="large")

    with left:
        st.markdown("<div class='section-header'>🤖 Your Robot Helper</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="glass-card">
            <div style="font-size:0.92rem; color:#eef2f7; line-height:1.8;">
                <b>Imagine you have a tiny robot helper.</b> Every 30 minutes, your robot does the boring stuff for you:
                <br><br>
                <span style="color:#00e5ff;">📂</span> Opens the data (forecast, actual, schedules)<br>
                <span style="color:#ffd740;">🔍</span> Checks rules (like: "Are we short staffed?")<br>
                <span style="color:#ff5252;">🚨</span> If something is wrong, it shouts: "Hey! Fix this interval!"
                <br><br>
                <b style="color:#00e676;">You still make the decision.</b> The robot just saves time.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='section-header'>📚 What You'll Learn</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="glass-card">
            <div style="font-size:0.92rem; color:#c8d6e8; line-height:1.8;">
                ✅ What "RPA steps" look like in real WFM work<br>
                ✅ What a <b style="color:#eef2f7;">rules engine</b> is (simple if/then logic)<br>
                ✅ What the bot outputs (alerts, exceptions, files)
            </div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown("<div class='section-header'>🗓️ 5-Day Learning Path</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="glass-card-accent">
            <div class="path-step">
                <div class="path-dot path-dot-1">1</div>
                <div><div class="path-label">Intraday Health Check</div><div class="path-desc">Learn how bots flag risk intervals in real time.</div></div>
            </div>
            <div class="path-step">
                <div class="path-dot path-dot-2">2</div>
                <div><div class="path-label">Forecast vs Actual</div><div class="path-desc">Understand how bots explain forecast misses.</div></div>
            </div>
            <div class="path-step">
                <div class="path-dot path-dot-3">3</div>
                <div><div class="path-label">Adherence Sweep</div><div class="path-desc">See how bots catch non-adherent agents.</div></div>
            </div>
            <div class="path-step">
                <div class="path-dot path-dot-4">4</div>
                <div><div class="path-label">Shrinkage Watch</div><div class="path-desc">Monitor shrinkage drift automatically.</div></div>
            </div>
            <div class="path-step">
                <div class="path-dot path-dot-5">5</div>
                <div><div class="path-label">Combine into 1 Bot Run</div><div class="path-desc">Chain all use cases into one scheduled pipeline.</div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("")
        if st.button("🧪  Jump to Simulator", key="guide_to_sim", use_container_width=True):
            nav_to("simulator")
            st.rerun()
        if st.button("📚  Browse Use Cases", key="guide_to_lib", use_container_width=True):
            nav_to("library")
            st.rerun()


# ============================================================
# PAGE: USE CASE LIBRARY
# ============================================================
elif page == "library":
    if st.button("← Back to Home", key="back_lib"):
        nav_to("home")
        st.rerun()

    st.markdown("""
    <div class="hero-wrapper" style="padding:28px 36px 24px;">
        <div class="hero-badge">📚 USE CASE LIBRARY</div>
        <div class="hero-title" style="font-size:1.8rem;">WFM RPA Bot Ideas</div>
        <div class="hero-sub">Pick a use case to explore its full pipeline: inputs → rules → outputs → actions.</div>
    </div>
    """, unsafe_allow_html=True)

    use_cases = [
        {
            "name": "Intraday Health Check",
            "freq": "Every 30 min",
            "icon": "🏥",
            "goal": "Detect risk intervals (low SL / high ASA / staffing gaps) and alert in real time.",
            "inputs": ["Forecast volume & AHT", "Actual volume", "Actual staffing", "Shrinkage plan"],
            "rules": ["If staffing gap ≤ -5 OR SL < target OR ASA > limit → Flag interval"],
            "outputs": ["Exception table", "Priority actions list", "Alert message text"],
            "actions": ["Send Teams/Email alert", "Save exception file", "Update BI feed"],
        },
        {
            "name": "Forecast vs Actual Variance",
            "freq": "Hourly",
            "icon": "📊",
            "goal": "Automatically explain why you missed forecast (volume, AHT, staffing).",
            "inputs": ["Forecast vs Actual", "AHT", "Staffing", "Campaign tags (optional)"],
            "rules": ["If variance > threshold → generate reason hints"],
            "outputs": ["Variance report", "Top drivers", "Suggested adjustments"],
            "actions": ["Email daily summary", "Post to channel"],
        },
        {
            "name": "Adherence Sweep",
            "freq": "Every 30–60 min",
            "icon": "👤",
            "goal": "Find low adherence agents and surface top reasons.",
            "inputs": ["Agent schedule", "Agent states", "Adherence calculation"],
            "rules": ["If adherence < 85% and OOA > X mins → escalate"],
            "outputs": ["Worst offenders list", "Reason codes", "Supervisor actions"],
            "actions": ["Send list to supervisors", "Create coaching queue"],
        },
        {
            "name": "Shrinkage Watch",
            "freq": "Daily",
            "icon": "📉",
            "goal": "Catch shrinkage risk early and protect staffing plan.",
            "inputs": ["Planned shrinkage", "Actual shrinkage", "Time-off usage"],
            "rules": ["If actual > planned by > 2pp → notify planners"],
            "outputs": ["Variance trend", "Risk score", "Next-day warning"],
            "actions": ["Send planning alert", "Recommend OT/skills move"],
        },
        {
            "name": "WFM Report Builder",
            "freq": "Daily / Weekly",
            "icon": "📋",
            "goal": "Auto-generate leadership-ready report packs.",
            "inputs": ["KPIs", "Trends", "Exception summaries"],
            "rules": ["Always build same report template"],
            "outputs": ["Excel report pack", "Charts", "Narrative bullets"],
            "actions": ["Email to stakeholders", "Drop to shared folder"],
        }
    ]

    # Use case selector as tabs
    uc_names = [f"{u['icon']} {u['name']}" for u in use_cases]
    selected_tab = st.radio("Select a use case", uc_names, horizontal=True, label_visibility="collapsed")
    idx = uc_names.index(selected_tab)
    uc = use_cases[idx]

    st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

    # Use Case Detail
    st.markdown(f"""
    <div class="uc-card" style="border-left: 3px solid #00e5ff;">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap;">
            <div class="uc-title" style="font-size:1.15rem;">{uc['icon']} {uc['name']}</div>
            <span class="tag tag-action">{uc['freq']}</span>
        </div>
        <div class="uc-goal" style="margin-top:6px;">{uc['goal']}</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="large")

    with c1:
        st.markdown("<div class='section-header'>📥 Inputs</div>", unsafe_allow_html=True)
        inp_html = "<div class='glass-card'>"
        for x in uc["inputs"]:
            inp_html += f"<span class='tag tag-input'>📥 {x}</span>"
        inp_html += "</div>"
        st.markdown(inp_html, unsafe_allow_html=True)

        st.markdown("<div class='section-header'>🧮 Rules (Bot Brain)</div>", unsafe_allow_html=True)
        rule_html = "<div class='glass-card'>"
        for x in uc["rules"]:
            rule_html += f"<div style='color:#ffd740; font-size:0.9rem; padding:6px 0;'>⚡ {x}</div>"
        rule_html += "</div>"
        st.markdown(rule_html, unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='section-header'>📤 Outputs</div>", unsafe_allow_html=True)
        out_html = "<div class='glass-card'>"
        for x in uc["outputs"]:
            out_html += f"<span class='tag tag-output'>📤 {x}</span>"
        out_html += "</div>"
        st.markdown(out_html, unsafe_allow_html=True)

        st.markdown("<div class='section-header'>🚀 Actions</div>", unsafe_allow_html=True)
        act_html = "<div class='glass-card'>"
        for x in uc["actions"]:
            act_html += f"<span class='tag tag-action'>🚀 {x}</span>"
        act_html += "</div>"
        st.markdown(act_html, unsafe_allow_html=True)

    st.markdown("<div class='spacer-lg'></div>", unsafe_allow_html=True)
    if st.button("🧪  Try this in the Simulator", key="lib_to_sim", use_container_width=True):
        nav_to("simulator")
        st.rerun()


# ============================================================
# PAGE: SIMULATOR
# ============================================================
elif page == "simulator":
    if st.button("← Back to Home", key="back_sim"):
        nav_to("home")
        st.rerun()

    st.markdown("""
    <div class="hero-wrapper" style="padding:28px 36px 24px;">
        <div class="hero-badge">🧪 SIMULATOR</div>
        <div class="hero-title" style="font-size:1.8rem;">Run a Bot Simulation</div>
        <div class="hero-sub">Pick a bot, set your rules, and watch the full RPA pipeline execute with dummy data.</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Bot Selector ──
    bot_options = {
        "🏥 Intraday Health Check": "Intraday Health Check",
        "📊 Forecast vs Actual Variance": "Forecast vs Actual Variance",
        "👤 Adherence Sweep": "Adherence Sweep",
        "📉 Shrinkage Watch": "Shrinkage Watch",
    }
    bot_display = st.radio("Select Bot", list(bot_options.keys()), horizontal=True, label_visibility="collapsed")
    bot = bot_options[bot_display]

    # Clear stale results if user switches bots
    if st.session_state.get("sim_bot") and st.session_state.sim_bot != bot:
        st.session_state.sim_ran = False

    st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

    # ── Config Panel ──
    cfg1, cfg2 = st.columns([0.6, 0.4], gap="large")

    # Defaults for all thresholds (so they exist even when a different bot's sliders are shown)
    sl_target = 80
    asa_limit = 60
    gap_limit = 5
    adh_target = 85
    ooa_limit = 30
    shrink_pp = 2

    with cfg1:
        st.markdown("<div class='section-header'>🎛️ Rules & Thresholds</div>", unsafe_allow_html=True)
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        if bot in ["Intraday Health Check", "Forecast vs Actual Variance"]:
            rc1, rc2, rc3 = st.columns(3)
            with rc1:
                sl_target = st.slider("SL Target (%)", 60, 95, 80, 1)
            with rc2:
                asa_limit = st.slider("ASA Limit (sec)", 20, 180, 60, 5)
            with rc3:
                gap_limit = st.slider("Gap Alert (heads)", 1, 30, 5, 1)
        elif bot == "Adherence Sweep":
            rc1, rc2 = st.columns(2)
            with rc1:
                adh_target = st.slider("Adherence Threshold (%)", 70, 95, 85, 1)
            with rc2:
                ooa_limit = st.slider("OOA Limit (min)", 5, 120, 30, 5)
        else:
            shrink_pp = st.slider("Shrinkage Variance Alert (pp)", 1, 10, 2, 1)
        st.markdown("</div>", unsafe_allow_html=True)

    with cfg2:
        st.markdown("<div class='section-header'>⚡ Run Settings</div>", unsafe_allow_html=True)
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        speed = st.select_slider("Simulation Speed", options=["Fast", "Normal", "Slow"], value="Normal")
        speed_map = {"Fast": 0.08, "Normal": 0.18, "Slow": 0.30}
        intervals = st.selectbox("Intervals (Intraday)", [24, 48, 96], index=1)
        st.session_state.seed = st.number_input(
            "Data Seed", min_value=1, max_value=9999,
            value=int(st.session_state.seed),
            help="Change to generate a different random scenario"
        )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

    run = st.button("▶️  Run Bot Simulation", use_container_width=True)

    # Store simulation state so results survive checkbox re-runs
    if run:
        st.session_state.sim_ran = True
        st.session_state.sim_bot = bot
        st.session_state.sim_seed = int(st.session_state.seed)
        st.session_state.sim_sl_target = sl_target
        st.session_state.sim_asa_limit = asa_limit
        st.session_state.sim_gap_limit = gap_limit
        st.session_state.sim_adh_target = adh_target
        st.session_state.sim_ooa_limit = ooa_limit
        st.session_state.sim_shrink_pp = shrink_pp
        st.session_state.sim_intervals = intervals
        st.session_state.logs = []

    if run:
        # Only show animation on fresh button click
        logs = st.session_state.logs
        seed = st.session_state.sim_seed
        st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)
        st.markdown("<div class='section-header'>🤖 Bot Execution</div>", unsafe_allow_html=True)
        steps = [
            "Connect to data source",
            "Validate input schema",
            "Compute derived metrics",
            "Apply rule engine",
            "Generate exceptions",
            "Rank & prioritize",
            "Build output artifacts",
            "Dispatch alerts (simulated)",
        ]
        with st.container():
            rpa_steps_simulator(steps, logs, speed=speed_map[speed])
        st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

    if st.session_state.get("sim_ran"):
        logs = st.session_state.logs
        seed = st.session_state.sim_seed
        bot = st.session_state.sim_bot
        sl_target = st.session_state.get("sim_sl_target", 80)
        asa_limit = st.session_state.get("sim_asa_limit", 60)
        gap_limit = st.session_state.get("sim_gap_limit", 5)
        adh_target = st.session_state.get("sim_adh_target", 85)
        ooa_limit = st.session_state.get("sim_ooa_limit", 30)
        shrink_pp = st.session_state.get("sim_shrink_pp", 2)
        intervals = st.session_state.get("sim_intervals", 48)
        is_fresh = run  # True only on button click, False on checkbox re-runs

        # ── INTRADAY HEALTH CHECK ──
        if bot == "Intraday Health Check":
            df = make_dummy_intraday(periods=intervals, seed=seed)
            if is_fresh:
                log_add(logs, f"Loaded intraday table: {len(df):,} intervals")

            df["flag_staffing"] = df["staffing_gap"] <= -gap_limit
            df["flag_sl"] = df["service_level_est_pct"] < sl_target
            df["flag_asa"] = df["asa_sec_est"] > asa_limit
            df["is_risk"] = df[["flag_staffing", "flag_sl", "flag_asa"]].any(axis=1)

            risk = df[df["is_risk"]].copy()
            risk["priority"] = (
                (risk["flag_staffing"].astype(int) * 3) +
                (risk["flag_sl"].astype(int) * 2) +
                (risk["flag_asa"].astype(int) * 1)
            )
            risk = risk.sort_values(["priority", "service_level_est_pct", "staffing_gap"], ascending=[False, True, True])

            total_risk = len(risk)
            if total_risk == 0:
                st.markdown("""
                <div class="status-banner status-ok">
                    <span class="status-icon">✅</span>
                    <div><div class="status-text">ALL CLEAR</div><div class="status-detail">No risk intervals detected. Bot would post: All good.</div></div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="status-banner status-risk">
                    <span class="status-icon">🚨</span>
                    <div><div class="status-text">ACTION NEEDED — {total_risk} Risk Intervals</div><div class="status-detail">Bot would immediately alert the intraday team with exception details.</div></div>
                </div>""", unsafe_allow_html=True)

            render_metric_row([
                (f"{len(df):,}", "Intervals Checked", "info"),
                (f"{total_risk:,}", "Risk Intervals", "bad" if total_risk else "ok"),
                (f"{risk['service_level_est_pct'].min():.1f}%" if total_risk else "—", "Worst SL", "warn" if total_risk else ""),
                (f"{risk['staffing_gap'].min():,}" if total_risk else "—", "Worst Gap", "bad" if total_risk else ""),
            ])

            # ── Charts ──
            st.markdown("<div class='section-header'>📈 Visual Analysis</div>", unsafe_allow_html=True)
            ch1, ch2 = st.columns(2, gap="medium")

            with ch1:
                fig_vol = go.Figure()
                fig_vol.add_trace(go.Scatter(
                    x=df["interval_label"], y=df["volume_fcst"],
                    name="Forecast", line=dict(color="#00e5ff", width=2),
                    fill="tozeroy", fillcolor="rgba(0,229,255,0.06)"
                ))
                fig_vol.add_trace(go.Scatter(
                    x=df["interval_label"], y=df["volume_act"],
                    name="Actual", line=dict(color="#e040fb", width=2, dash="dot")
                ))
                fig_vol.update_layout(title="Volume: Forecast vs Actual", height=320)
                plotly_theme(fig_vol)
                st.plotly_chart(fig_vol, use_container_width=True)

            with ch2:
                colors = ["#ff5252" if g < -gap_limit else "#00e676" if g >= 0 else "#ffd740" for g in df["staffing_gap"]]
                fig_gap = go.Figure(go.Bar(
                    x=df["interval_label"], y=df["staffing_gap"],
                    marker_color=colors, name="Gap"
                ))
                fig_gap.add_hline(y=-gap_limit, line_dash="dash", line_color="#ff5252",
                                  annotation_text=f"Alert threshold (-{gap_limit})")
                fig_gap.update_layout(title="Staffing Gap by Interval", height=320)
                plotly_theme(fig_gap)
                st.plotly_chart(fig_gap, use_container_width=True)

            ch3, ch4 = st.columns(2, gap="medium")
            with ch3:
                fig_sl = go.Figure()
                fig_sl.add_trace(go.Scatter(
                    x=df["interval_label"], y=df["service_level_est_pct"],
                    name="SL %", line=dict(color="#00e676", width=2),
                    fill="tozeroy", fillcolor="rgba(0,230,118,0.06)"
                ))
                fig_sl.add_hline(y=sl_target, line_dash="dash", line_color="#ffd740",
                                 annotation_text=f"Target ({sl_target}%)")
                fig_sl.update_layout(title="Service Level %", height=300)
                plotly_theme(fig_sl)
                st.plotly_chart(fig_sl, use_container_width=True)

            with ch4:
                fig_asa = go.Figure()
                fig_asa.add_trace(go.Scatter(
                    x=df["interval_label"], y=df["asa_sec_est"],
                    name="ASA (sec)", line=dict(color="#ff5252", width=2),
                    fill="tozeroy", fillcolor="rgba(255,82,82,0.06)"
                ))
                fig_asa.add_hline(y=asa_limit, line_dash="dash", line_color="#ffd740",
                                  annotation_text=f"Limit ({asa_limit}s)")
                fig_asa.update_layout(title="ASA (Seconds)", height=300)
                plotly_theme(fig_asa)
                st.plotly_chart(fig_asa, use_container_width=True)

            # ── Data Tables ──
            st.markdown('<div class="toggle-section-title"><span class="toggle-icon">📋</span> Bot Inputs (full data)</div>', unsafe_allow_html=True)
            if st.checkbox("Show / Hide", value=False, key="chk_bot_inputs"):
                st.dataframe(df, use_container_width=True, height=350)

            st.markdown('<div class="toggle-section-title"><span class="toggle-icon">🚨</span> Exceptions (what the bot would send)</div>', unsafe_allow_html=True)
            if st.checkbox("Show / Hide", value=False, key="chk_exceptions"):
                if total_risk:
                    show_cols = [
                        "interval_label", "volume_act", "needed_staff", "actual_staff", "staffing_gap",
                        "asa_sec_est", "service_level_est_pct", "flag_staffing", "flag_sl", "flag_asa", "priority"
                    ]
                    st.dataframe(risk[show_cols], use_container_width=True, height=350)
                else:
                    st.success("No exceptions. This is the best kind of bot run.")

            # ── Actions ──
            if total_risk:
                st.markdown("<div class='section-header'>💡 Suggested Actions</div>", unsafe_allow_html=True)
                top = risk.head(6)
                for _, r in top.iterrows():
                    parts = []
                    if r["flag_staffing"]:
                        parts.append(f"Short by **{abs(int(r['staffing_gap']))}** heads")
                    if r["flag_sl"]:
                        parts.append(f"SL **{r['service_level_est_pct']}%** < {sl_target}%")
                    if r["flag_asa"]:
                        parts.append(f"ASA **{int(r['asa_sec_est'])}s** > {asa_limit}s")
                    st.markdown(f"- **{r['interval_label']}**: {' · '.join(parts)} → Consider OT / skill move / VTO pause")

            # ── Downloads ──
            st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)
            dl1, dl2 = st.columns(2)
            with dl1:
                bytes_download_excel(
                    {"Intraday": df, "Exceptions": risk if total_risk else df.head(0)},
                    filename="wfm_rpa_intraday_simulator.xlsx",
                )
            with dl2:
                bytes_download_csv(risk if total_risk else df.head(0), "wfm_rpa_intraday_exceptions.csv")

        # ── FORECAST VS ACTUAL VARIANCE ──
        elif bot == "Forecast vs Actual Variance":
            df = make_dummy_intraday(periods=intervals, seed=seed)
            if is_fresh:
                log_add(logs, f"Loaded forecast/actual table: {len(df):,} intervals")

            df["vol_var_pct"] = np.where(df["volume_fcst"] > 0,
                                         (df["volume_act"] - df["volume_fcst"]) / df["volume_fcst"] * 100, 0.0).round(1)
            df["gap_pct"] = np.where(df["needed_staff"] > 0,
                                     (df["actual_staff"] - df["needed_staff"]) / df["needed_staff"] * 100, 0.0).round(1)

            def driver(row):
                drivers = []
                if abs(row["vol_var_pct"]) >= 8:
                    drivers.append("Volume")
                if row["aht_sec"] >= 480:
                    drivers.append("AHT")
                if row["staffing_gap"] <= -5:
                    drivers.append("Staffing")
                return ", ".join(drivers) if drivers else "Minor/Normal"

            df["top_driver_hint"] = df.apply(driver, axis=1)
            df["is_miss"] = (df["service_level_est_pct"] < sl_target) | (df["asa_sec_est"] > asa_limit)
            miss = df[df["is_miss"]].copy()
            miss = miss.sort_values(["service_level_est_pct", "asa_sec_est"], ascending=[True, False])

            st.markdown("""
            <div class="status-banner status-ok">
                <span class="status-icon">📊</span>
                <div><div class="status-text">Variance Analysis Complete</div><div class="status-detail">Bot identified drivers for each interval and flagged misses.</div></div>
            </div>""", unsafe_allow_html=True)

            render_metric_row([
                (f"{len(df):,}", "Intervals Checked", "info"),
                (f"{len(miss):,}", "Miss Intervals", "bad" if len(miss) else "ok"),
                (f"{df['vol_var_pct'].mean():.1f}%", "Avg Vol Variance", "warn"),
                (miss["top_driver_hint"].mode().iloc[0] if len(miss) else "—", "Top Driver", ""),
            ])

            # Charts
            ch1, ch2 = st.columns(2, gap="medium")
            with ch1:
                fig = go.Figure()
                fig.add_trace(go.Bar(x=df["interval_label"], y=df["volume_fcst"], name="Forecast",
                                     marker_color="rgba(0,229,255,0.55)"))
                fig.add_trace(go.Bar(x=df["interval_label"], y=df["volume_act"], name="Actual",
                                     marker_color="rgba(224,64,251,0.5)"))
                fig.update_layout(title="Volume Comparison", barmode="group", height=320)
                plotly_theme(fig)
                st.plotly_chart(fig, use_container_width=True)

            with ch2:
                var_colors = ["#ff5252" if abs(v) > 10 else "#ffd740" if abs(v) > 5 else "#00e676" for v in df["vol_var_pct"]]
                fig2 = go.Figure(go.Bar(x=df["interval_label"], y=df["vol_var_pct"], marker_color=var_colors))
                fig2.update_layout(title="Volume Variance %", height=320)
                plotly_theme(fig2)
                st.plotly_chart(fig2, use_container_width=True)

            show = df[["interval_label", "volume_fcst", "volume_act", "vol_var_pct",
                        "aht_sec", "needed_staff", "actual_staff", "staffing_gap",
                        "asa_sec_est", "service_level_est_pct", "top_driver_hint"]]

            st.markdown('<div class="toggle-section-title"><span class="toggle-icon">📋</span> Full Variance Table</div>', unsafe_allow_html=True)
            if st.checkbox("Show / Hide", value=False, key="chk_variance_table"):
                st.dataframe(show, use_container_width=True, height=350)

            st.markdown('<div class="toggle-section-title"><span class="toggle-icon">🚨</span> Miss Intervals</div>', unsafe_allow_html=True)
            if st.checkbox("Show / Hide", value=False, key="chk_miss_intervals"):
                if len(miss):
                    st.dataframe(miss[show.columns], use_container_width=True, height=350)
                else:
                    st.success("No big misses based on your targets. Nice!")

            st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)
            dl1, dl2 = st.columns(2)
            with dl1:
                bytes_download_excel({"Variance": show, "Misses": miss[show.columns]}, "wfm_rpa_variance_simulator.xlsx")
            with dl2:
                bytes_download_csv(miss[show.columns], "wfm_rpa_variance_misses.csv")

        # ── ADHERENCE SWEEP ──
        elif bot == "Adherence Sweep":
            df = make_dummy_adherence(n_agents=140, seed=seed)
            if is_fresh:
                log_add(logs, f"Loaded adherence table: {len(df):,} agents")

            df["is_alert"] = (df["adherence_pct"] < adh_target) & (df["out_of_adherence_minutes"] >= ooa_limit)
            alerts = df[df["is_alert"]].copy()

            total_alerts = len(alerts)
            if total_alerts == 0:
                st.markdown("""
                <div class="status-banner status-ok">
                    <span class="status-icon">✅</span>
                    <div><div class="status-text">ALL CLEAR</div><div class="status-detail">No adherence alerts based on current thresholds.</div></div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="status-banner status-risk">
                    <span class="status-icon">🚨</span>
                    <div><div class="status-text">{total_alerts} Agents Flagged</div><div class="status-detail">Bot would send this list to team leaders for coaching action.</div></div>
                </div>""", unsafe_allow_html=True)

            render_metric_row([
                (f"{len(df):,}", "Agents Checked", "info"),
                (f"{total_alerts:,}", "Alerts", "bad" if total_alerts else "ok"),
                (f"{df['adherence_pct'].min():.1f}%", "Worst Adherence", "warn"),
                (alerts["top_reason"].mode().iloc[0] if total_alerts else "—", "Top Reason", ""),
            ])

            # Charts
            ch1, ch2 = st.columns(2, gap="medium")
            with ch1:
                fig = px.histogram(df, x="adherence_pct", nbins=25,
                                   color_discrete_sequence=["#00b8d4"],
                                   title="Adherence Distribution")
                fig.add_vline(x=adh_target, line_dash="dash", line_color="#ffd740",
                              annotation_text=f"Threshold ({adh_target}%)")
                plotly_theme(fig)
                fig.update_layout(height=320)
                st.plotly_chart(fig, use_container_width=True)

            with ch2:
                tenure_avg = df.groupby("tenure_band")["adherence_pct"].mean().reset_index()
                fig2 = px.bar(tenure_avg, x="tenure_band", y="adherence_pct",
                              color="tenure_band",
                              color_discrete_map={"New": "#ff5252", "Mid": "#ffd740", "Tenured": "#00e676"},
                              title="Avg Adherence by Tenure")
                plotly_theme(fig2)
                fig2.update_layout(height=320, showlegend=False)
                st.plotly_chart(fig2, use_container_width=True)

            if total_alerts:
                # Reason breakdown
                reason_counts = alerts["top_reason"].value_counts().reset_index()
                reason_counts.columns = ["reason", "count"]
                fig3 = px.pie(reason_counts, values="count", names="reason",
                              title="Alert Reasons Breakdown",
                              color_discrete_sequence=px.colors.qualitative.Pastel)
                plotly_theme(fig3)
                fig3.update_layout(
                    height=380,
                    legend=dict(
                        orientation="h",
                        yanchor="top",
                        y=-0.08,
                        xanchor="center",
                        x=0.5,
                        font=dict(size=12, color="#c8d6e8"),
                    ),
                    margin=dict(l=20, r=20, t=44, b=80),
                )
                st.plotly_chart(fig3, use_container_width=True)

            st.markdown('<div class="toggle-section-title"><span class="toggle-icon">📋</span> All Agents</div>', unsafe_allow_html=True)
            if st.checkbox("Show / Hide", value=False, key="chk_all_agents"):
                st.dataframe(df, use_container_width=True, height=350)

            st.markdown('<div class="toggle-section-title"><span class="toggle-icon">🚨</span> Alerts (what bot sends to TLs)</div>', unsafe_allow_html=True)
            if st.checkbox("Show / Hide", value=False, key="chk_alerts_tl"):
                if total_alerts:
                    st.dataframe(alerts, use_container_width=True, height=350)
                else:
                    st.success("No alerts based on your thresholds.")

            st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)
            dl1, dl2 = st.columns(2)
            with dl1:
                bytes_download_excel({"Adherence": df, "Alerts": alerts}, "wfm_rpa_adherence_simulator.xlsx")
            with dl2:
                bytes_download_csv(alerts, "wfm_rpa_adherence_alerts.csv")

        # ── SHRINKAGE WATCH ──
        else:
            df = make_dummy_shrinkage(days=14, seed=seed)
            if is_fresh:
                log_add(logs, f"Loaded shrinkage table: {len(df):,} days")

            df["is_alert"] = df["variance_pp"] >= shrink_pp
            alerts = df[df["is_alert"]].copy()
            total_alerts = len(alerts)

            if total_alerts == 0:
                st.markdown("""
                <div class="status-banner status-ok">
                    <span class="status-icon">✅</span>
                    <div><div class="status-text">NO SHRINKAGE RISK</div><div class="status-detail">All days within threshold. No planner alerts needed.</div></div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="status-banner status-risk">
                    <span class="status-icon">🚨</span>
                    <div><div class="status-text">{total_alerts} Days Over Threshold</div><div class="status-detail">Bot would notify planners to validate time-off and adjust staffing.</div></div>
                </div>""", unsafe_allow_html=True)

            render_metric_row([
                (f"{len(df):,}", "Days Checked", "info"),
                (f"{total_alerts:,}", "Alert Days", "bad" if total_alerts else "ok"),
                (f"{df['variance_pp'].max():.1f}pp", "Max Variance", "warn"),
                (f"{df.iloc[-1]['actual_shrinkage_pct']:.1f}%", "Latest Actual", ""),
            ])

            # Chart
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df["date"].astype(str), y=df["planned_shrinkage_pct"],
                name="Planned", line=dict(color="#00e5ff", width=2)
            ))
            fig.add_trace(go.Scatter(
                x=df["date"].astype(str), y=df["actual_shrinkage_pct"],
                name="Actual", line=dict(color="#ff5252", width=2),
                fill="tonexty", fillcolor="rgba(255,82,82,0.06)"
            ))
            fig.update_layout(title="Shrinkage: Planned vs Actual (14-Day Trend)", height=360)
            plotly_theme(fig)
            st.plotly_chart(fig, use_container_width=True)

            # Variance bar
            var_colors = ["#ff5252" if v >= shrink_pp else "#00e676" for v in df["variance_pp"]]
            fig2 = go.Figure(go.Bar(
                x=df["date"].astype(str), y=df["variance_pp"],
                marker_color=var_colors
            ))
            fig2.add_hline(y=shrink_pp, line_dash="dash", line_color="#ffd740",
                           annotation_text=f"Alert threshold ({shrink_pp}pp)")
            fig2.update_layout(title="Daily Variance (pp)", height=300)
            plotly_theme(fig2)
            st.plotly_chart(fig2, use_container_width=True)

            st.markdown('<div class="toggle-section-title"><span class="toggle-icon">📋</span> Full Trend Data</div>', unsafe_allow_html=True)
            if st.checkbox("Show / Hide", value=False, key="chk_trend_data"):
                st.dataframe(df, use_container_width=True)

            st.markdown('<div class="toggle-section-title"><span class="toggle-icon">🚨</span> Alert Days</div>', unsafe_allow_html=True)
            if st.checkbox("Show / Hide", value=False, key="chk_alert_days"):
                if total_alerts:
                    st.dataframe(alerts, use_container_width=True)
                    st.warning("Suggested: validate time-off, check unplanned AUX, adjust staffing/OT plan.")
                else:
                    st.success("No shrinkage risk days based on your threshold.")

            st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)
            dl1, dl2 = st.columns(2)
            with dl1:
                bytes_download_excel({"Shrinkage": df, "Alerts": alerts}, "wfm_rpa_shrinkage_simulator.xlsx")
            with dl2:
                bytes_download_csv(alerts, "wfm_rpa_shrinkage_alerts.csv")

        # ── Bot Logs (all bots) ──
        st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)
        st.markdown('<div class="toggle-section-title"><span class="toggle-icon">📜</span> Bot Run Logs</div>', unsafe_allow_html=True)
        if st.checkbox("Show / Hide", value=False, key="chk_bot_logs"):
            st.code("\n".join(st.session_state.logs[-60:]) if st.session_state.logs else "No logs yet.")

        st.markdown("""
        <div class="glass-card-accent" style="margin-top:16px;">
            <div style="font-weight:700; color:#eef2f7; margin-bottom:6px;">💡 Next Step Ideas</div>
            <div style="font-size:0.88rem; color:#c8d6e8; line-height:1.7;">
                Replace dummy data with your Excel files → Schedule it to run every 30 min (Task Scheduler / cron) → Push outputs to Power BI or Teams.
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Pro CTA mini card ──
        st.markdown("""
        <div class="pro-card-wrapper" style="margin-top:20px;">
            <div class="pro-card-inner" style="padding:22px 26px;">
                <div style="display:flex; align-items:center; gap:12px; flex-wrap:wrap;">
                    <div class="pro-badge" style="margin-bottom:0;">⚡ ADVANCED</div>
                    <div style="font-size:0.9rem; color:#eef2f7; font-weight:600;">Need Bot Builder, Connectors, or Rules Editor?</div>
                </div>
                <div style="margin-top:10px; font-size:0.85rem; color:#c8d6e8;">
                    📧 Contact <a href="mailto:support@wfmcommons.com" class="pro-email-link">support@wfmcommons.com</a> for advanced features and enterprise options.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ============================================================
# PAGE: GLOSSARY
# ============================================================
elif page == "glossary":
    if st.button("← Back to Home", key="back_gloss"):
        nav_to("home")
        st.rerun()

    st.markdown("""
    <div class="hero-wrapper" style="padding:28px 36px 24px;">
        <div class="hero-badge">❓ REFERENCE</div>
        <div class="hero-title" style="font-size:1.8rem;">RPA & WFM Glossary</div>
        <div class="hero-sub">Key terms explained in plain language. Bookmark this page for quick reference.</div>
    </div>
    """, unsafe_allow_html=True)

    glossary_items = [
        ("RPA (Robotic Process Automation)", "A software robot that repeats computer steps for you — like a macro on steroids."),
        ("Bot Run", "One full execution cycle: get data → compute → decide → act. Usually runs on a schedule."),
        ("Rules Engine", 'The "IF this happens, THEN do that" brain of the bot. Pure logic, no AI needed.'),
        ("Exceptions", "The problem rows the bot finds — bad intervals, low adherence, high variance, etc."),
        ("Artifacts", "Files the bot creates as output — Excel reports, CSV exports, logs, summaries."),
        ("Triggers / Scheduling", "When the bot runs: every 30 minutes, daily at 6 AM, on-demand, or event-driven."),
        ("Orchestration", "Managing many bots — who runs when, success/fail handling, retries, dependencies."),
        ("Service Level (SL)", "% of calls answered within a target time (e.g., 80% in 20 seconds)."),
        ("ASA (Average Speed of Answer)", "The average time a caller waits before being connected to an agent."),
        ("Shrinkage", "The % of scheduled time agents are NOT available (breaks, meetings, training, etc.)."),
        ("Adherence", "How closely agents follow their assigned schedule — measured as a percentage."),
        ("Intraday Management", "Real-time adjustments during the day to keep performance on track."),
    ]

    # Search filter
    search = st.text_input("🔍 Search terms...", placeholder="Type to filter...", label_visibility="collapsed")

    filtered = glossary_items
    if search:
        filtered = [(t, d) for t, d in glossary_items if search.lower() in t.lower() or search.lower() in d.lower()]

    col1, col2 = st.columns(2, gap="medium")
    for i, (term, defn) in enumerate(filtered):
        with col1 if i % 2 == 0 else col2:
            st.markdown(f"""
            <div class="glossary-item">
                <div class="glossary-term">{term}</div>
                <div class="glossary-def">{defn}</div>
            </div>
            """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════
    # PROS, CONS & LIMITATIONS
    # ══════════════════════════════════════════════════════════
    st.markdown("<div class='spacer-lg'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-header'>⚖️ Pros, Considerations & Limitations</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="proscons-grid">
        <div class="pros-card">
            <div class="pc-title green">✅ Pros</div>
            <div class="pc-item"><span class="pc-icon">🎯</span> Reduces repetitive manual tasks — analysts save 2–4 hours per day on routine checks.</div>
            <div class="pc-item"><span class="pc-icon">⚡</span> Faster reaction time — bots detect issues within minutes, not hours.</div>
            <div class="pc-item"><span class="pc-icon">📊</span> Consistent outputs — same rules, same format every time. No human variability.</div>
            <div class="pc-item"><span class="pc-icon">📈</span> Scalable — one bot can monitor hundreds of intervals, agents, or queues simultaneously.</div>
            <div class="pc-item"><span class="pc-icon">🧪</span> Safe to learn — this simulator uses dummy data, so there's zero risk to production systems.</div>
            <div class="pc-item"><span class="pc-icon">💡</span> Low barrier — can start with Python scripts before investing in enterprise RPA tools.</div>
        </div>
        <div class="cons-card">
            <div class="pc-title amber">⚠️ Considerations</div>
            <div class="pc-item"><span class="pc-icon">🔧</span> Rules need tuning — thresholds must be calibrated to your site's reality, not just defaults.</div>
            <div class="pc-item"><span class="pc-icon">👤</span> Human judgment still required — the bot flags problems, but decisions remain with the analyst.</div>
            <div class="pc-item"><span class="pc-icon">🔄</span> Maintenance overhead — rules, data sources, and integrations need periodic updates.</div>
            <div class="pc-item"><span class="pc-icon">📋</span> Change management — teams need training and buy-in to trust automated alerts.</div>
            <div class="pc-item"><span class="pc-icon">🔌</span> Integration complexity — connecting to live WFM/ACD systems requires IT involvement.</div>
        </div>
    </div>
    <div class="limits-card" style="margin-bottom:24px;">
        <div class="pc-title red">🚧 Limitations of This Simulator</div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:4px 24px;">
            <div class="pc-item"><span class="pc-icon">🔢</span> Uses randomly generated dummy data — not connected to real WFM/ACD systems.</div>
            <div class="pc-item"><span class="pc-icon">📡</span> No live integrations — cannot send real alerts to Teams, Email, or BI tools.</div>
            <div class="pc-item"><span class="pc-icon">🧱</span> No custom rule builder — thresholds are pre-defined sliders, not flexible logic.</div>
            <div class="pc-item"><span class="pc-icon">📂</span> Cannot upload your own files — data is generated internally only.</div>
            <div class="pc-item"><span class="pc-icon">🔐</span> No multi-user or role-based access — designed for individual learning only.</div>
            <div class="pc-item"><span class="pc-icon">⏱️</span> No scheduling or orchestration — bot runs are manual, on-demand clicks.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════
    # WHAT TO BUILD NEXT
    # ══════════════════════════════════════════════════════════
    st.markdown("<div class='section-header'>🔨 What to Build Next</div>", unsafe_allow_html=True)

    next_items = [
        ("📤 Upload Excel", "Use your own forecast/actual file instead of dummy data."),
        ("🗺️ Column Mapping", "Choose your column names so the bot understands your format."),
        ("💬 Teams Webhook", "Send real notifications to a Microsoft Teams channel."),
        ("📊 Power BI Feed", "Export clean tables that Power BI can refresh automatically."),
    ]

    nc = st.columns(4, gap="medium")
    for i, (title, desc) in enumerate(next_items):
        with nc[i]:
            st.markdown(f"""
            <div class="glass-card" style="text-align:center; padding:22px 16px;">
                <div style="font-size:1.3rem; margin-bottom:8px;">{title.split(' ')[0]}</div>
                <div style="font-weight:700; color:#eef2f7; font-size:0.88rem; margin-bottom:4px;">{' '.join(title.split(' ')[1:])}</div>
                <div style="font-size:0.8rem; color:#c8d6e8;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Pro CTA on glossary page ──
    st.markdown("<div class='spacer-lg'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="pro-card-wrapper">
        <div class="pro-card-inner" style="padding:22px 26px;">
            <div style="display:flex; align-items:center; gap:12px; flex-wrap:wrap;">
                <div class="pro-badge" style="margin-bottom:0;">⚡ ADVANCED FEATURES</div>
                <div style="font-size:0.9rem; color:#eef2f7; font-weight:600;">Ready for production-grade WFM automation?</div>
            </div>
            <div style="margin-top:10px; font-size:0.85rem; color:#c8d6e8;">
                Get access to <b style="color:#b39ddb;">Bot Builder</b>, <b style="color:#b39ddb;">Connectors</b>,
                <b style="color:#b39ddb;">Rules Editor</b> and more.
                📧 <a href="mailto:support@wfmcommons.com" class="pro-email-link">support@wfmcommons.com</a>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Footer ──
st.markdown("<div class='footer'>WFM RPA Simulator — Built for learning. No real data is used or stored.</div>", unsafe_allow_html=True)
