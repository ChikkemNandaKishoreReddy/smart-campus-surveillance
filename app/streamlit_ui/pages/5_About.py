"""
About Page
"""

import streamlit as st

st.set_page_config(
    page_title="About",
    page_icon="ℹ️",
    layout="wide",
)

# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("ℹ️ About")
st.subheader("AI-Powered Smart Campus Surveillance System")

st.markdown(
    """
This project is a **real-time intelligent campus surveillance system**
developed using **YOLOv8**, **OpenCV**, **SQLite**, and **Streamlit**.

The application performs live person detection, people analytics,
restricted area monitoring, intrusion detection, automatic screenshot
capture, event logging, analytics visualization, and report generation.
"""
)

st.write("---")

# --------------------------------------------------
# Features
# --------------------------------------------------

st.header("🚀 Features")

features = [
    "Real-Time Person Detection",
    "Multiple Person Tracking",
    "Entry & Exit Counting",
    "Restricted Area Monitoring",
    "Intrusion Detection",
    "Automatic Screenshot Capture",
    "SQLite Event Database",
    "Detection History",
    "CSV Export",
    "Analytics Dashboard",
    "Professional Streamlit GUI",
]

for feature in features:
    st.markdown(f"✅ {feature}")

st.write("---")

# --------------------------------------------------
# Technology Stack
# --------------------------------------------------

st.header("🛠 Technology Stack")

tech1, tech2 = st.columns(2)

with tech1:
    st.markdown("""
- Python 3.11
- YOLOv8 (Ultralytics)
- OpenCV
- NumPy
- Pandas
""")

with tech2:
    st.markdown("""
- SQLite
- Streamlit
- Matplotlib
- VS Code
- Git & GitHub
""")

st.write("---")

# --------------------------------------------------
# Project Information
# --------------------------------------------------

st.header("📋 Project Information")

col1, col2 = st.columns(2)

with col1:
    st.metric("Version", "1.0.0")
    st.metric("Application", "Campus Surveillance")

with col2:
    st.metric("Model", "YOLOv8n")
    st.metric("Database", "SQLite")

st.write("---")

# --------------------------------------------------
# Developer
# --------------------------------------------------

st.header("👨‍💻 Developer")

st.info(
    """
**Project Title**

AI-Powered Smart Campus Surveillance System with Intrusion Detection
and People Analytics using YOLOv8

**Academic Project**

Final Year Deep Learning Project

Developed using Python, Computer Vision,
Deep Learning and Streamlit.
"""
)

st.write("---")

# --------------------------------------------------
# Footer
# --------------------------------------------------

st.caption("© 2026 Smart Campus Surveillance System | Version 1.0")