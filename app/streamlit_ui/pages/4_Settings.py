"""
Settings Page
"""

import streamlit as st

from app.utils.settings_manager import SettingsManager


st.set_page_config(
    page_title="Settings",
    page_icon="⚙️",
    layout="wide",
)

# ---------------------------------------------------------
# Load Saved Settings
# ---------------------------------------------------------

settings_manager = SettingsManager()

settings = settings_manager.load()

# ---------------------------------------------------------
# Page Title
# ---------------------------------------------------------

st.title("⚙️ Settings")
st.caption("Configure surveillance system preferences.")

st.write("---")

# ---------------------------------------------------------
# Detection Settings
# ---------------------------------------------------------

st.header("Detection Settings")

confidence = st.slider(
    "Detection Confidence Threshold",
    min_value=0.10,
    max_value=1.00,
    value=float(settings["confidence"]),
    step=0.05,
)

camera_index = st.number_input(
    "Camera Index",
    min_value=0,
    max_value=10,
    value=int(settings["camera_index"]),
)

save_screenshots = st.checkbox(
    "Save Intrusion Screenshots",
    value=settings["save_screenshots"],
)

enable_logs = st.checkbox(
    "Enable Event Logging",
    value=settings["enable_logs"],
)

st.write("---")

# ---------------------------------------------------------
# Dashboard
# ---------------------------------------------------------

st.header("Dashboard")

auto_refresh = st.checkbox(
    "Enable Auto Refresh",
    value=settings["auto_refresh"],
)

refresh_interval = st.slider(
    "Refresh Interval (seconds)",
    5,
    60,
    int(settings["refresh_interval"]),
)

st.write("---")

# ---------------------------------------------------------
# Database
# ---------------------------------------------------------

st.header("Database")

database_path = st.text_input(
    "Database Path",
    value=settings["database_path"],
)

csv_path = st.text_input(
    "CSV Export Folder",
    value=settings["csv_path"],
)

st.write("---")

# ---------------------------------------------------------
# Save Button
# ---------------------------------------------------------

if st.button("💾 Save Settings", use_container_width=True):

    updated_settings = {
        "confidence": confidence,
        "camera_index": camera_index,
        "save_screenshots": save_screenshots,
        "enable_logs": enable_logs,
        "auto_refresh": auto_refresh,
        "refresh_interval": refresh_interval,
        "database_path": database_path,
        "csv_path": csv_path,
    }

    settings_manager.save(updated_settings)

    st.success("✅ Settings saved successfully!")

    settings = updated_settings

st.write("---")

# ---------------------------------------------------------
# Current Configuration
# ---------------------------------------------------------

st.subheader("Current Configuration")

st.json(settings_manager.load())