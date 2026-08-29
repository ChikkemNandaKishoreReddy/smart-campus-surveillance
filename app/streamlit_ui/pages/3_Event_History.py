"""
Event History Page
"""

import os
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app.analytics.analytics import Analytics


analytics = Analytics()

st.title("📋 Event History")

st.caption("Search and review all surveillance events.")

st.write("---")

events = analytics.get_all_events()

if not events:
    st.warning("No events found.")
    st.stop()

df = pd.DataFrame(events)

# -------------------------------------------------
# Filters
# -------------------------------------------------

left, right = st.columns(2)

with left:
    event_types = ["All"] + sorted(df["event_type"].unique().tolist())
    selected_type = st.selectbox(
        "Event Type",
        event_types,
    )

with right:
    track_ids = ["All"] + sorted(
        [str(x) for x in df["track_id"].unique()]
    )

    selected_track = st.selectbox(
        "Track ID",
        track_ids,
    )

search = st.text_input(
    "Search Timestamp / Screenshot",
)

filtered = df.copy()

if selected_type != "All":
    filtered = filtered[
        filtered["event_type"] == selected_type
    ]

if selected_track != "All":
    filtered = filtered[
        filtered["track_id"] == int(selected_track)
    ]

if search:
    filtered = filtered[
        filtered.astype(str)
        .apply(
            lambda row: row.str.contains(
                search,
                case=False,
            ).any(),
            axis=1,
        )
    ]

filtered = filtered.sort_values(
    by="timestamp",
    ascending=False,
)

st.write("---")

st.subheader(
    f"Events ({len(filtered)})"
)

st.dataframe(
    filtered,
    use_container_width=True,
)

st.write("---")

csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download Filtered CSV",
    csv,
    "filtered_events.csv",
    "text/csv",
)