"""
Smart Campus Surveillance System
Home Page
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st

# ----------------------------------------------------
# Page Configuration
# ----------------------------------------------------

st.set_page_config(
    page_title="Smart Campus Surveillance",
    page_icon="🎥",
    layout="wide",
)

# ----------------------------------------------------
# Custom CSS
# ----------------------------------------------------

st.markdown(
    """
    <style>

    .main {
        background-color: #0E1117;
    }

    .title {
        text-align: center;
        font-size: 50px;
        font-weight: bold;
        color: white;
    }

    .subtitle {
        text-align: center;
        font-size: 20px;
        color: #BBBBBB;
    }

    .feature-box{
        padding:20px;
        border-radius:12px;
        background:#1E1E1E;
        margin-bottom:15px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------
# Title
# ----------------------------------------------------

st.markdown(
    "<div class='title'>🎥 Smart Campus Surveillance System</div>",
    unsafe_allow_html=True,
)

st.markdown(
    "<div class='subtitle'>AI-Powered Intrusion Detection and People Analytics using YOLOv8</div>",
    unsafe_allow_html=True,
)

st.write("")
st.write("---")

# ----------------------------------------------------
# Project Overview
# ----------------------------------------------------

st.header("Project Overview")

st.write(
    """
This system performs real-time surveillance using **YOLOv8**.

### Features

- ✅ Real-Time Person Detection
- ✅ People Tracking
- ✅ Entry & Exit Counting
- ✅ Restricted Area Monitoring
- ✅ Intrusion Detection
- ✅ Automatic Screenshot Capture
- ✅ SQLite Database
- ✅ Detection History
- ✅ CSV Export
- ✅ Analytics Dashboard
"""
)

st.write("---")

# ----------------------------------------------------
# Navigation
# ----------------------------------------------------

st.header("Navigation")

st.info(
    """
Use the **left sidebar** to navigate between pages.

📹 Live Detection

📊 Analytics

📜 Event History

⚙️ Settings

ℹ️ About
"""
)

st.write("---")

# ----------------------------------------------------
# System Status
# ----------------------------------------------------

st.header("System Status")

col1, col2, col3 = st.columns(3)

col1.success("YOLO Model Ready")

col2.success("SQLite Connected")

col3.success("Analytics Enabled")

st.write("---")

st.caption("Version 1.0.0")