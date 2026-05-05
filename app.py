"""Main entry point for the Streamlit Screen Time Dashboard application."""

import streamlit as st
import sqlite3
import os
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:%(name)s:%(message)s"
    )

logger = logging.getLogger(__name__)


st.set_page_config(
    page_title="Screen Time Dashboard", layout="wide"
)  # Configuration must be the first command to avoid Streamlit errors.

# added import for the new data entry page
from components.data_entry_page import show_data_entry
from data.database import load_data
from utils.parsers import prepare_app_dataframe
from components.layout import apply_custom_css, render_sidebar
from components.kpis import render_kpis
from components.charts import (
    render_timeline_chart,
    render_apps_stacked_bar,
    render_small_charts,
)


def main() -> None:

    logger.info("Dashboard gestartet")

    if "page" not in st.session_state:
        st.session_state["page"] = "main"

    logger.info("Aktuelle seite: %s", st.session_state["page"])

    if st.session_state["page"] == "data_entry":
        show_data_entry()
        return
    # Execute the core application logic to render the Streamlit dashboard.
    apply_custom_css()

    st.title("Screen Time Dashboard")

    st.sidebar.header("Benutzer-Auswahl")
    # Dynamically query unique users from the database instead of using a static list
    users = []
    if os.path.exists("screentime.db"):
        logger.info("Lade Benutzer aus der Datenbank")

        try:
            with sqlite3.connect("screentime.db") as conn:
                users = [
                    row[0]
                    for row in conn.execute("SELECT DISTINCT username FROM records")
                ]
        except Exception as e:
            logger.error("Fehler beim Laden der Benutzer: %s",e)
            st.error("Benutzer konnten nicht geladen werden.")

    if not users:
        st.warning("Keine Benutzer in der Datenbank (screentime.db) gefunden.")
        return

    selected_user = st.sidebar.selectbox(
        "Gruppenmitglied wählen", users
    )  # Allow team members to switch between their usage data.
    logger.info("User ausgewählt: %s", selected_user)

    # Button for Data entry page
    if st.sidebar.button("Daten eintragen"):
        st.session_state["page"] = "data_entry"
        st.rerun()

    df = load_data(selected_user)

    logger.info("Daten geladen: %d Zeilen", len(df))

    if df.empty:
        logger.warning("keine Daten für User: %s", selected_user)
        st.warning(
            f"Keine Daten für '{selected_user}' in der Datenbank (screentime.db) gefunden."
        )
        return

    selected_dates = render_sidebar(df)
    mask = (df["Datum"].dt.date >= selected_dates[0]) & (
        df["Datum"].dt.date <= selected_dates[1]
    )
    filtered_df = df.loc[mask].copy()

    logger.info("Gefilterte Daten: %d Zeilen", len(filtered_df))

    if filtered_df.empty:
        st.info("Im ausgewählten Zeitraum liegen keine Daten vor.")
        return

    st.markdown("---")

    app_df = prepare_app_dataframe(filtered_df)
    top_apps = app_df.groupby("App_Name")["App_Zeit_h"].sum().reset_index()

    render_kpis(filtered_df, top_apps)
    st.markdown("---")
    render_timeline_chart(filtered_df)
    render_apps_stacked_bar(app_df)
    render_small_charts(filtered_df, app_df)


if __name__ == "__main__":
    main()
