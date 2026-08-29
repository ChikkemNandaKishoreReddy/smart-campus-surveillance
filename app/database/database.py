"""
SQLite Database Manager
"""

import sqlite3
from pathlib import Path

import pandas as pd

from app.utils.logger import logger


class DatabaseManager:

    def __init__(self):

        db_dir = Path("data/database")
        db_dir.mkdir(parents=True, exist_ok=True)

        self.db_path = db_dir / "surveillance.db"

        self.connection = sqlite3.connect(
            self.db_path,
            check_same_thread=False,
        )

        self.connection.row_factory = sqlite3.Row

        self.cursor = self.connection.cursor()

        self.create_tables()

        logger.info("SQLite database initialized.")

    def create_tables(self):

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS events (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                event_type TEXT NOT NULL,

                track_id INTEGER,

                timestamp TEXT,

                screenshot TEXT

            )
            """
        )

        self.connection.commit()

    def insert_event(
        self,
        event_type,
        track_id,
        timestamp,
        screenshot,
    ):

        self.cursor.execute(
            """
            INSERT INTO events
            (
                event_type,
                track_id,
                timestamp,
                screenshot
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                event_type,
                track_id,
                timestamp,
                screenshot,
            ),
        )

        self.connection.commit()

        logger.info("Event inserted into SQLite database.")

    def get_all_events(self):

        self.cursor.execute(
            """
            SELECT *
            FROM events
            ORDER BY id DESC
            """
        )

        return self.cursor.fetchall()

    def get_latest_events(self, limit=10):

        self.cursor.execute(
            """
            SELECT *
            FROM events
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        )

        return self.cursor.fetchall()

    def get_events_by_track(self, track_id):

        self.cursor.execute(
            """
            SELECT *
            FROM events
            WHERE track_id = ?
            ORDER BY id DESC
            """,
            (track_id,),
        )

        return self.cursor.fetchall()

    def get_events_by_type(self, event_type):

        self.cursor.execute(
            """
            SELECT *
            FROM events
            WHERE event_type = ?
            ORDER BY id DESC
            """,
            (event_type,),
        )

        return self.cursor.fetchall()

    def export_csv(self):

        query = """
        SELECT *
        FROM events
        ORDER BY id DESC
        """

        df = pd.read_sql_query(query, self.connection)

        output_dir = Path("data/csv")
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / "events.csv"

        df.to_csv(output_file, index=False)

        logger.info("CSV exported: %s", output_file)

        return output_file

    def close(self):

        self.connection.close()