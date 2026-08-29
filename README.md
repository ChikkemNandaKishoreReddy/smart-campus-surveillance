# 🎥 AI-Powered Smart Campus Surveillance System

### Real-Time Intrusion Detection and People Analytics using YOLOv8

---

## 📌 Project Overview

The **AI-Powered Smart Campus Surveillance System** is a real-time computer vision application designed to improve security monitoring in campus environments.

The system uses **YOLOv8** for real-time person detection and tracking. It monitors people entering a defined restricted area, detects potential intrusions, records surveillance events, captures evidence screenshots, and stores event information in an SQLite database.

A professional **Streamlit-based graphical user interface** provides access to live detection, analytics, event history, system settings, and project information.

The system is designed as a modular Python application suitable for academic demonstration, further development, and deployment as a smart surveillance solution.

---

# ✨ Features

## 🎥 Real-Time Detection

- Real-time webcam surveillance
- YOLOv8 object detection
- Person-only detection
- Detection confidence display
- Bounding boxes around detected people

## 👤 People Analytics

- Real-time people counting
- Persistent tracking IDs
- Entry counting
- Exit counting
- Track-based event analysis

## 🚨 Intrusion Detection

- Configurable restricted surveillance area
- Automatic intrusion detection
- Visual intrusion indication
- Intrusion event generation
- Track ID associated with detected intrusion

## 📸 Evidence Capture

- Automatic screenshot capture during intrusion events
- Timestamp-based screenshot filenames
- Screenshots stored locally for later review

## 🗄️ Database

- SQLite-based event storage
- Event type
- Track ID
- Timestamp
- Screenshot path
- Detection history retrieval

## 📊 Analytics

- Total event count
- Total intrusion count
- Unique tracked people
- Daily event statistics
- Hourly event statistics
- Track-based statistics
- Analytics charts

## 📋 Event History

- Complete event history
- Event type filtering
- Track ID filtering
- Timestamp/search filtering
- Filtered event display
- Filtered CSV download

## 📥 CSV Export

- Export surveillance events to CSV
- Download complete event reports
- Download filtered event history

## ⚙️ Settings

- Detection confidence threshold
- Camera index
- Screenshot configuration
- Event logging configuration
- Dashboard refresh configuration
- Database path
- CSV export path
- Persistent JSON-based settings

## 🖥️ Streamlit GUI

The application provides a multi-page Streamlit interface:

- 🏠 Home
- 🎥 Live Detection
- 📊 Analytics
- 📋 Event History
- ⚙️ Settings
- ℹ️ About

---

# 🏗️ System Architecture

The system follows a modular architecture.

```text
                    ┌─────────────────────────┐
                    │       Webcam Input      │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │       YOLOv8 Model      │
                    │    Person Detection     │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │    Person Tracking      │
                    │     Track ID Creation   │
                    └────────────┬────────────┘
                                 │
                 ┌───────────────┴───────────────┐
                 │                               │
                 ▼                               ▼
       ┌───────────────────┐          ┌────────────────────┐
       │ People Analytics  │          │ Restricted Area    │
       │ Entry / Exit      │          │ Monitoring         │
       │ People Count      │          └─────────┬──────────┘
       └───────────────────┘                    │
                                                ▼
                                     ┌────────────────────┐
                                     │ Intrusion Detection│
                                     └─────────┬──────────┘
                                               │
                         ┌─────────────────────┼────────────────────┐
                         │                     │                    │
                         ▼                     ▼                    ▼
                ┌────────────────┐    ┌────────────────┐   ┌───────────────┐
                │ Screenshot     │    │ Event Manager  │   │ SQLite        │
                │ Capture        │    │                │   │ Database      │
                └────────────────┘    └───────┬────────┘   └───────┬───────┘
                                               │                    │
                                               └─────────┬──────────┘
                                                         ▼
                                               ┌──────────────────┐
                                               │ Analytics Module │
                                               └────────┬─────────┘
                                                        │
                                                        ▼
                                               ┌──────────────────┐
                                               │ Streamlit GUI    │
                                               │ Dashboard        │
                                               └──────────────────┘