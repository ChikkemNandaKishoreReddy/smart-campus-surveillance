"""
Analytics Dashboard
"""
import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pathlib import Path

import pandas as pd
import streamlit as st

from app.analytics.analytics import Analytics


# ----------------------------------------------------
# Page Configuration
# ----------------------------------------------------

st.set_page_config(
    page_title="Smart Campus Surveillance",
    page_icon="🎥",
    layout="wide",
)

# ----------------------------------------------------
# Dark Theme Styling
# ----------------------------------------------------

st.markdown(
    """
    <style>
        .main{
            background-color:#0E1117;
        }

        h1,h2,h3,h4{
            color:white;
        }

        div[data-testid="metric-container"]{
            background:#1E1E1E;
            border-radius:10px;
            padding:15px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

analytics = Analytics()

summary = analytics.dashboard_summary()

st.title("🎥 Smart Campus Surveillance Dashboard")

st.write("---")

# ----------------------------------------------------
# KPI Cards
# ----------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Events",
        summary["total_events"],
    )

with col2:
    st.metric(
        "Total Intrusions",
        summary["total_intrusions"],
    )

with col3:
    st.metric(
        "Unique People",
        summary["unique_people"],
    )

st.write("---")

# ----------------------------------------------------
# Charts
# ----------------------------------------------------

st.header("Analytics Charts")

analytics_path = Path("data/analytics")

daily = analytics_path / "daily_events.png"
hourly = analytics_path / "hourly_events.png"
track = analytics_path / "track_statistics.png"

c1, c2 = st.columns(2)

with c1:
    if daily.exists():
        st.image(str(daily), use_container_width=True)

    if hourly.exists():
        st.image(str(hourly), use_container_width=True)

with c2:
    if track.exists():
        st.image(str(track), use_container_width=True)

st.write("---")

# ----------------------------------------------------
# Recent Events
# ----------------------------------------------------

st.header("Recent Intrusion Events")

events = analytics.recent_events()

if events:
    df = pd.DataFrame(events)
    st.dataframe(df, use_container_width=True)
else:
    st.info("No events found.")

st.write("---")

# ----------------------------------------------------
# CSV Download
# ----------------------------------------------------

csv_path = Path("data/csv/events.csv")

if csv_path.exists():

    with open(csv_path, "rb") as file:

        st.download_button(
            label="📥 Download CSV Report",
            data=file,
            file_name="events.csv",
            mime="text/csv",
        )

st.write("---")

# ----------------------------------------------------
# Refresh
# ----------------------------------------------------

if st.button("🔄 Refresh Dashboard"):
    st.rerun()