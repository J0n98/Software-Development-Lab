import logging
import sqlite3
from datetime import date

import streamlit as st

from data.database import insert_data

# Modul-Logger erstellen
logger = logging.getLogger(__name__)


def show_data_entry() -> None:
    """
    Zeigt die Streamlit-Seite zur Dateneingabe.

    Der Benutzer gibt Datum, Username, Gesamtzeit und
    die 5 meist genutzten Apps mit Zeiten ein.
    """
    st.title("Daten eintragen")

    datum = st.date_input("Datum", value=date.today())
    username = st.text_input("User")
    gesamtzeit = st.text_input("Gesamtzeit (z.B. 4h 20m)")

    st.write("### Die 5 meist genutzten Apps eingeben:")

    # App-Namen und Zeiten einsammeln
    apps: list[tuple[str, str]] = []
    for i in range(1, 6):
        name = st.text_input(f"App {i} Name")
        zeit = st.text_input(f"App {i} Zeit (z.B. 1h 10m)")
        apps.append((name, zeit))

    if st.button("Speichern"):
        # Eingabevalidierung: Pflichtfelder prüfen
        if not username.strip():
            st.warning("Bitte einen Benutzernamen eingeben.")
            logger.warning("Speichern abgebrochen: Kein Benutzername angegeben.")
        elif not gesamtzeit.strip():
            st.warning("Bitte die Gesamtzeit eingeben.")
            logger.warning("Speichern abgebrochen: Keine Gesamtzeit angegeben.")
        else:
            try:
                insert_data(datum.isoformat(), username, gesamtzeit, apps)
                st.success("Gespeichert!")
            except sqlite3.Error:
                # Datenbankfehler dem User anzeigen
                st.error("Datenbankfehler – Eintrag konnte nicht gespeichert werden.")
                logger.error(
                    "Datenbankfehler beim Speichern für Benutzer '%s'.", username
                )
            except ValueError as e:
                st.error(f"Eingabefehler: {e}")
                logger.error("Eingabefehler: %s", e)

    if st.button("Zurück zum Dashboard"):
        st.session_state["page"] = "main"
        st.rerun()
