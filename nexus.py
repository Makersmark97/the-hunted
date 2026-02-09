import streamlit as st
import pandas as pd
import random, time, psutil, os
from datetime import datetime
from dotenv import load_dotenv

# --- 1. LOAD THE MASTER .ENV ---
load_dotenv(override=True)

# --- 2. FAIL-SAFE MEMORY ---
if "fin" not in st.session_state:
    st.session_state.fin = {
        # Load from .env or default to 0.00
        "app1_rev": float(os.getenv("APP1_REVENUE", 0.00)),
        "app2_rev": float(os.getenv("APP2_REVENUE", 0.00)),
        "hq_import": float(os.getenv("HQ_IMPORT", 0.00)),
        "logs": [],
        "phase": "STEALTH"
    }

# --- 3. INDUSTRIAL CSS ---
st.set_page_config(page_title="THE HUNTED", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #3182FF; font-family: monospace; }
    .block-container { padding-top: 1rem; }
    .fin-card { border: 1px solid #333; background: #050505; padding: 15px; text-align: center; }
    .fin-val { font-size: 2rem; font-weight: bold; color: #00FF41; }
    .fin-label { font-size: 0.8rem; color: #888; }
    .upload-zone { border: 2px dashed #3182FF; padding: 20px; text-align: center; margin-top: 20px; }
    </style>
""", unsafe_allow_html=True)

# --- 4. MASTER HUD ---
st.title("🦅 THE HUNTED // DATA FUSION")

# CALCULATE TOTALS
total_30d = st.session_state.fin["app1_rev"] + st.session_state.fin["app2_rev"] + st.session_state.fin["hq_import"]

c1, c2, c3, c4 = st.columns(4)
c1.metric("CONFIRMED TOTAL", f"${total_30d:,.2f}")
c2.metric("HQ IMPORT", f"${st.session_state.fin['hq_import']:,.2f}")
c3.metric("DISK SPACE", f"{round(psutil.disk_usage('/').free / 1e9, 2)} GB")
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

    st.write("---")
    
    # --- THE DATA INGESTION PORT ---
    st.markdown("### 📥 IMPORT HQ APP DATA")
    st.write("Drag and drop the **.env** file from your HQ App folder here to auto-sync the revenue.")
    
    uploaded_file = st.file_uploader("UPLOAD .ENV FILE", type=["env", "txt"])
    
    if uploaded_file is not None:
        # THE ROBOTIC PARSER
        try:
            content = uploaded_file.getvalue().decode("utf-8")
            hq_found = 0.0
            
            # Scan for anything looking like money
            for line in content.splitlines():
                if "=" in line and ("REV" in line or "BAL" in line or "TOTAL" in line):
                    parts = line.split("=")
                    try:
                        val = float(parts[1].strip().replace(",", "").replace("$", ""))
                        hq_found = val
                        break # Found the money
                    except:
                        continue
            
            if hq_found > 0:
                st.success(f"✅ DATA FOUND: ${hq_found:,.2f}")
                if st.button("CONFIRM MERGE"):
                    # Update Memory
                    st.session_state.fin["hq_import"] = hq_found
                    # Update Hard Drive (The Master .env)
                    with open(".env", "a") as f:
                        f.write(f"\nHQ_IMPORT={hq_found}")
                    st.toast("MERGE SUCCESSFUL")
                    time.sleep(1)
                    st.rerun()
            else:
                st.warning("⚠️ FILE SCANNED, BUT NO CLEAR REVENUE FOUND. CHECK FILE FORMAT.")
                
        except Exception as e:
            st.error(f"READ ERROR: {e}")

# STATIC TABS
with tabs[2]: st.image("https://via.placeholder.com/800x400/000/3182FF?text=FEED")
with tabs[3]: st.info("RUNNER HUD ACTIVE")
with tabs[4]: st.error("HUNTER HUD ACTIVE")
