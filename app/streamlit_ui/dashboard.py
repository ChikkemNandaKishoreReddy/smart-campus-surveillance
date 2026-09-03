"""
Smart Campus Surveillance System
Analytics Dashboard
"""

import os
import sys
from pathlib import Path


# ---------------------------------------------------------
# Project Root
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


import pandas as pd
import streamlit as st

from app.analytics.analytics import Analytics


# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="Analytics | Smart Campus Surveillance",
    page_icon="AN",
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

    h1, h2, h3, h4 {
        color: white;
    }

    div[data-testid="metric-container"] {
        background: #1E1E1E;
        border-radius: 10px;
        padding: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Analytics Initialization
# ---------------------------------------------------------

analytics = Analytics()

summary = analytics.dashboard_summary()


# ---------------------------------------------------------
# Page Header
# ---------------------------------------------------------

st.title("Smart Campus Surveillance Dashboard")

st.write(
    "System-wide surveillance statistics and event analytics."
)

st.divider()


# ---------------------------------------------------------
# KPI Cards
# ---------------------------------------------------------

st.header("System Statistics")

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


st.divider()


# ---------------------------------------------------------
# Analytics Charts
# ---------------------------------------------------------

st.header("Analytics Charts")

analytics_path = PROJECT_ROOT / "data" / "analytics"

daily_chart = analytics_path / "daily_events.png"
hourly_chart = analytics_path / "hourly_events.png"
track_chart = analytics_path / "track_statistics.png"


chart_col1, chart_col2 = st.columns(2)


with chart_col1:

    if daily_chart.exists():

        st.subheader("Daily Events")

        st.image(
            str(daily_chart),
            width="stretch",
        )

    if hourly_chart.exists():

        st.subheader("Hourly Events")

        st.image(
            str(hourly_chart),
            width="stretch",
        )


with chart_col2:

    if track_chart.exists():

        st.subheader("Track Statistics")

        st.image(
            str(track_chart),
            width="stretch",
        )


if not any(
    chart.exists()
    for chart in [
        daily_chart,
        hourly_chart,
        track_chart,
    ]
):

    st.info(
        "Analytics charts are not available yet. "
        "Run the detection system to generate event data."
    )


st.divider()


# ---------------------------------------------------------
# Recent Events
# ---------------------------------------------------------

st.header("Recent Intrusion Events")

events = analytics.recent_events()


if events:

    dataframe = pd.DataFrame(events)

    st.dataframe(
        dataframe,
        width="stretch",
        hide_index=True,
    )

else:

    st.info("No intrusion events have been recorded yet.")


st.divider()


# ---------------------------------------------------------
# CSV Export
# ---------------------------------------------------------

st.header("Reports")

csv_path = PROJECT_ROOT / "data" / "csv" / "events.csv"


if csv_path.exists():

    with open(csv_path, "rb") as csv_file:

        st.download_button(
            label="Download CSV Report",
            data=csv_file,
            file_name="events.csv",
            mime="text/csv",
        )

else:

    st.info(
        "CSV report is not available yet. "
        "Run the detection system to generate event data."
    )


st.divider()


# ---------------------------------------------------------
# Refresh Dashboard
# ---------------------------------------------------------

if st.button("Refresh Dashboard"):

    st.rerun()