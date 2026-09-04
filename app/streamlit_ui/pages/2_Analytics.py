"""
Analytics Dashboard
"""

import os
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[3]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.analytics.analytics import Analytics

# ----------------------------------------------------
# Page Config
# ----------------------------------------------------

st.set_page_config(
    page_title="Analytics",
    page_icon="\U0001F4CA",
    layout="wide",
)

analytics = Analytics()
summary = analytics.dashboard_summary()

# ----------------------------------------------------
# Title
# ----------------------------------------------------

st.title("\U0001F4CA Analytics Dashboard")
st.caption("Campus Surveillance Statistics")

st.divider()

# ----------------------------------------------------
# KPI Cards
# ----------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "\U0001F4C4 Total Events",
        summary["total_events"],
    )

with col2:
    st.metric(
        "\U0001F6A8 Intrusions",
        summary["total_intrusions"],
    )

with col3:
    st.metric(
        "\U0001F464 Unique People",
        summary["unique_people"],
    )

with col4:
    screenshot_count = len(
        list((PROJECT_ROOT / "data" / "screenshots").glob("*.jpg"))
    )

    st.metric(
        "\U0001F4F7 Screenshots",
        screenshot_count,
    )

st.divider()

# ----------------------------------------------------
# Charts
# ----------------------------------------------------

st.header("Analytics Charts")

analytics_path = PROJECT_ROOT / "data" / "analytics"

daily = analytics_path / "daily_events.png"
hourly = analytics_path / "hourly_events.png"
track = analytics_path / "track_statistics.png"

left, right = st.columns(2)

with left:

    if daily.exists():
        st.image(daily, width="stretch")

    if hourly.exists():
        st.image(hourly, width="stretch")

with right:

    if track.exists():
        st.image(track, width="stretch")

st.divider()

# ----------------------------------------------------
# Recent Events
# ----------------------------------------------------

st.header("Recent Intrusion Events")

events = analytics.recent_events()

if events:

    df = pd.DataFrame(events)

    st.dataframe(
        df,
        width="stretch",
        hide_index=True,
    )

else:

    st.info("No events available.")

st.divider()

# ----------------------------------------------------
# Download CSV
# ----------------------------------------------------

csv_file = PROJECT_ROOT / "data" / "csv" / "events.csv"

if csv_file.exists():

    with open(csv_file, "rb") as file:

        st.download_button(
            "\U0001F4E5 Download CSV Report",
            file,
            file_name="events.csv",
            mime="text/csv",
        )

st.divider()

# ----------------------------------------------------
# Refresh
# ----------------------------------------------------

if st.button(
    "\U0001F504 Refresh Dashboard",
    width="stretch",
):

    st.rerun()
