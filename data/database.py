import sqlite3
import pandas as pd
import os
import streamlit as st
from utils.parsers import parse_time_to_minutes

@st.cache_data
def load_data(username):
    """Lädt die Daten aus der SQLite-Datenbank für den ausgewählten User."""
    db_path = 'screentime.db'
    if not os.path.exists(db_path):
        return pd.DataFrame()
        
    try:
        conn = sqlite3.connect(db_path)
        query = "SELECT * FROM records WHERE username = ?"
        df = pd.read_sql_query(query, conn, params=(username,))
        conn.close()
        
        if df.empty:
            return df
            
        # Datum parsen
        df['Datum'] = pd.to_datetime(df['Datum'])
        
        # Strings in numerische Minuten und Stunden umwandeln
        df['Gesamtzeit_min'] = df['Gesamtzeit'].apply(parse_time_to_minutes)
        df['Gesamtzeit_h'] = df['Gesamtzeit_min'] / 60
        
        return df
    except Exception as e:
        return pd.DataFrame()
