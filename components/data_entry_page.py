import streamlit as st
from data.database import insert_data
from datetime import date


def show_data_entry() -> None:
    st.title("Daten eintragen")

    datum = st.date_input("Datum", value=date.today())
    username = st.text_input("User")
    gesamtzeit = st.text_input("Gesamtzeit (z.B. 4h 20m)")

    st.write("### Die 5 meist genutzten Apps eingeben:")

    apps = []
    for i in range(1, 6):
        name = st.text_input(f"App {i} Name")
        zeit = st.text_input(f"App {i} Zeit (z.B. 1h 10m)")
        apps.append((name, zeit))

    if st.button("Speichern"):
        insert_data(datum.isoformat(), username, gesamtzeit, apps)
        st.success("Gespeichert!")

    if st.button("Zurück zum Dashboard"):
        st.session_state["page"] = "main"
        st.rerun()