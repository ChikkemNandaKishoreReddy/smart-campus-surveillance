"""
Smart Campus Surveillance System
Home Page
"""

import os
import sys


# ---------------------------------------------------------
# Project Root
# ---------------------------------------------------------

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


import streamlit as st


# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="Smart Campus Surveillance",
    page_icon="SC",
    layout="wide",
)


# ---------------------------------------------------------
# Custom Styling
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    .main {
        background-color: #0E1117;
    }

    .title {
        text-align: center;
        font-size: 46px;
        font-weight: bold;
        color: white;
        margin-top: 20px;
        margin-bottom: 10px;
    }

    .subtitle {
        text-align: center;
        font-size: 20px;
        color: #BBBBBB;
        margin-bottom: 30px;
    }

    .feature-box {
        padding: 20px;
        border-radius: 12px;
        background: #1E1E1E;
        margin-bottom: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

st.markdown(
    "<div class='title'>Smart Campus Surveillance System</div>",
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class='subtitle'>
    AI-Powered Intrusion Detection and People Analytics using YOLOv8
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")
st.divider()


# ---------------------------------------------------------
# Project Overview
# ---------------------------------------------------------

st.header("Project Overview")

st.write(
    """
The Smart Campus Surveillance System is an AI-powered computer
vision application designed for real-time campus monitoring.

The system uses a fine-tuned YOLOv8n object detection model
to detect and track people from a live camera feed.
"""
)


# ---------------------------------------------------------
# Main Features
# ---------------------------------------------------------

st.subheader("System Features")

features = [
    "Real-Time Person Detection",
    "Persistent Person Tracking",
    "People Counting",
    "Entry and Exit Counting",
    "Restricted Area Monitoring",
    "Intrusion Detection",
    "Automatic Intrusion Screenshot Capture",
    "SQLite Event Logging",
    "Detection History",
    "CSV Report Export",
    "Analytics Dashboard",
]

columns = st.columns(3)

for index, feature in enumerate(features):
    with columns[index % 3]:
        st.markdown(
            f"""
            <div class="feature-box">
                <strong>{feature}</strong>
            </div>
            """,
            unsafe_allow_html=True,
        )


st.divider()


# ---------------------------------------------------------
# Navigation
# ---------------------------------------------------------

st.header("Application Navigation")

st.write(
    """
Use the sidebar to access the different modules of the
surveillance system.
"""
)

navigation = {
    "Live Detection": "Real-time webcam detection, tracking, "
    "people counting, entry/exit monitoring, and intrusion detection.",

    "Analytics": "View event statistics and graphical analytics.",

    "Event History": "Review previously recorded surveillance events.",

    "Settings": "Configure application parameters.",

    "About": "View project information and technical details.",
}

for page, description in navigation.items():
    st.markdown(
        f"**{page}**  \n{description}"
    )


st.divider()


# ---------------------------------------------------------
# Model Information
# ---------------------------------------------------------

st.header("AI Model")

model_col1, model_col2, model_col3 = st.columns(3)

with model_col1:
    st.metric(
        "Model",
        "Fine-Tuned YOLOv8n",
    )

with model_col2:
    st.metric(
        "Detection Class",
        "Person",
    )

with model_col3:
    st.metric(
        "mAP50",
        "73.10%",
    )


st.caption(
    "The selected model was fine-tuned using the project's custom "
    "Person detection dataset."
)


st.divider()


# ---------------------------------------------------------
# System Status
# ---------------------------------------------------------

st.header("System Status")

status_col1, status_col2, status_col3 = st.columns(3)

with status_col1:
    st.success("YOLO Model Ready")

with status_col2:
    st.success("SQLite Database Ready")

with status_col3:
    st.success("Analytics Ready")


st.divider()


# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------

st.caption(
    "Smart Campus Surveillance System | Version 1.0.0"
)