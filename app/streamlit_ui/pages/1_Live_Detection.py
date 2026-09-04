"""
Live Detection Page
"""

import subprocess
import sys
from pathlib import Path

import streamlit as st

st.set_page_config(
    page_title="Live Detection",
    page_icon="\U0001F3A5",
    layout="wide",
)

st.title("\U0001F3A5 Live Detection")

st.write(
    "Start the real-time YOLOv8 surveillance system using the button below."
)

st.divider()

col1, col2 = st.columns(2)

with col1:

    st.subheader("Detection Controls")

    if st.button("\u25B6 Start Detection", width="stretch"):

        project_root = Path(__file__).resolve().parents[3]
        main_file = project_root / "main.py"

        subprocess.Popen(
            [sys.executable, str(main_file)],
            cwd=project_root,
        )

        st.success("Detection started successfully.")

with col2:

    st.subheader("System Status")

    st.info("Camera : Ready")

    st.info("YOLOv8 Model : Loaded")

    st.info("Tracking : Enabled")

    st.info("Restricted Area : Enabled")

st.divider()

st.subheader("Instructions")

st.markdown(
"""
1. Click **Start Detection**.

2. The OpenCV detection window will open.

3. Press **Q** inside the OpenCV window to stop detection.

4. Return here to view analytics and reports.
"""
)
