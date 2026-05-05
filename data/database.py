"""Database operations for the Screen Time Dashboard."""

import logging
import os
import sqlite3

import pandas as pd
import streamlit as st

from utils.parsers import parse_time_to_minutes

# Modul-Logger erstellen
logger = logging.getLogger(__name__)


@st.cache_data
def load_data(username: str) -> pd.DataFrame:
    """Load screen time data from SQLite database for a specific user."""
    db_path = "screentime.db"

    if not os.path.exists(db_path):
        return pd.DataFrame()

    try:
        conn = sqlite3.connect(db_path)
        query = "SELECT * FROM records WHERE username = ?"
        df = pd.read_sql_query(query, conn, params=(username,))
        conn.close()

        if df.empty:
            return df

        df["Datum"] = pd.to_datetime(df["Datum"])
        df["Gesamtzeit_min"] = df["Gesamtzeit"].apply(parse_time_to_minutes)
        df["Gesamtzeit_h"] = df["Gesamtzeit_min"] / 60

        return df

    except Exception:
        return pd.DataFrame()

def insert_data(
    username: str, datum: str, wochentag: str, gesamtzeit: str, apps: list[tuple[str, str]]
) -> None:
    """
    Fügt einen neuen Datensatz in die SQLite-Datenbank ein.

    Args:
        datum: Datum des Eintrags im ISO-Format (YYYY-MM-DD).
        username: Name des Benutzers.
        gesamtzeit: Gesamte Bildschirmzeit (z.B. '4h 20m').
        apps: Liste von genau 5 Tupeln (App-Name, App-Zeit).

    Raises:
        ValueError: Wenn nicht genau 5 Apps übergeben werden.
        sqlite3.Error: Bei Datenbankfehlern.
    """
    if len(apps) != 5:
        logger.error("Ungültige Anzahl an Apps: %d (erwartet: 5)", len(apps))
        raise ValueError(
            f"Es müssen genau 5 Apps übergeben werden, erhalten: {len(apps)}"
        )

    logger.info("Speichere Daten für Benutzer '%s' vom %s", username, datum)

    try:
        conn = sqlite3.connect("screentime.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO records (
                username, Datum, wochentag, Gesamtzeit,
                App1_Name, App1_Zeit,
                App2_Name, App2_Zeit,
                App3_Name, App3_Zeit,
                App4_Name, App4_Zeit,
                App5_Name, App5_Zeit
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                username,
                datum,
                wochentag,
                gesamtzeit,
                apps[0][0],
                apps[0][1],
                apps[1][0],
                apps[1][1],
                apps[2][0],
                apps[2][1],
                apps[3][0],
                apps[3][1],
                apps[4][0],
                apps[4][1],
            ),
        )

        conn.commit()
        logger.info("Daten erfolgreich gespeichert.")

    except sqlite3.Error as e:
        logger.error("Datenbankfehler beim Einfügen: %s", e)
        raise  # Fehler weitergeben, damit die GUI ihn anzeigen kann

    finally:
        conn.close()  # Verbindung wird immer geschlossen, auch bei Fehler