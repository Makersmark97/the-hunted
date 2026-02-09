import streamlit as st
import pandas as pd
import random, time, psutil, os
from datetime import datetime
from dotenv import load_dotenv

# --- 1. HYBRID DATA LOADER (LOCAL + CLOUD) ---
load_dotenv()

def get_config(key, default=0.0):
    # Try Cloud Secrets first (Streamlit Cloud)
    if key in st.secrets:
        return float(st.secrets[key])
    # Try Local Environment second (.env file)
    return float(os.getenv(key, default))

# --- 2. FAIL-SAFE MEMORY ---
if "fin" not in st.session_state:
    st.session_state.fin = {
        "app1_rev": get_config("APP1_REVENUE"),
        "app2_rev": get_config("APP2_REVENUE"),
        "hq_import": get_config("HQ_IMPORT"),
        "logs": [],
        "phase": "STEALTH"
    }

# --- 3. INDUSTRIAL DASHBOARD ---
st.set_page_config(page_title="THE HUNTED", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #3182FF; font-family: monospace; }
    .block-container { padding-top: 1rem; }
    .fin-card { border: 1px solid #333; background: #050505; padding: 15px; text-align: center; }
    .fin-val { font-size: 2rem; font-weight: bold; color: #00FF41; }
    .fin-label { font-size: 0.8rem; color: #888; }
    </style>
""", unsafe_allow_html=True)

# --- 4. MASTER HUD ---
st.title("🦅 THE HUNTED // GLOBAL OMNI-LINK")

total_30d = st.session_state.fin["app1_rev"] + st.session_state.fin["app2_rev"] + st.session_state.fin["hq_import"]

c1, c2, c3, c4 = st.columns(4)
c1.metric("GLOBAL REVENUE", f"${total_30d:,.2f}")
c2.metric("SERVER STATUS", "ONLINE")
c3.metric("SOURCE", "CLOUD SECRETS" if "APP1_REVENUE" in st.secrets else "LOCAL ENV")
c4.metric("PHASE", st.session_state.fin["phase"])

tabs = st.tabs(["🎮 DIRECTOR", "💰 FINANCIAL LEDGER", "📺 VIEWER", "🏃 RUNNER", "🎯 HUNTER"])

with tabs[0]:
    st.info("🎥 24-CHANNEL SWITCHER READY")
    g = st.columns(6)
    for i in range(1, 25):
        with g[(i-1)%6]:
            if st.button(f"{i:02d}", key=f"c{i}"): pass

with tabs[1]:
    st.markdown("### 📊 REVENUE STREAMS")
    f1, f2, f3 = st.columns(3)
    with f1:
        st.markdown(f'<div class="fin-card"><div class="fin-label">APP #1</div><div class="fin-val">${st.session_state.fin["app1_rev"]:,.2f}</div></div>', unsafe_allow_html=True)
    with f2:
        st.markdown(f'<div class="fin-card"><div class="fin-label">APP #2</div><div class="fin-val">${st.session_state.fin["app2_rev"]:,.2f}</div></div>', unsafe_allow_html=True)
    with f3:
        st.markdown(f'<div class="fin-card"><div class="fin-label">HQ IMPORT</div><div class="fin-val">${st.session_state.fin["hq_import"]:,.2f}</div></div>', unsafe_allow_html=True)

# STATIC TABS
with tabs[2]: st.image("https://via.placeholder.com/800x400/000/3182FF?text=FEED")
with tabs[3]: st.info("RUNNER HUD ACTIVE")
with tabs[4]: st.error("HUNTER HUD ACTIVE")
