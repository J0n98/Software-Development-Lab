"""Database operations for the Screen Time Dashboard."""
import sqlite3
import pandas as pd
import os
import streamlit as st
from utils.parsers import parse_time_to_minutes

@st.cache_data
def load_data(username):
    """Load screen time data from SQLite database for a specific user.

    Args:
        username (str): The name of the user to load data for.

    Returns:
        pd.DataFrame: A DataFrame containing the user's screen time data, or an empty DataFrame on failure.
    """
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
            
        df['Datum'] = pd.to_datetime(df['Datum'])  # Parse dates to enable time-series filtering and plotting.
        
        df['Gesamtzeit_min'] = df['Gesamtzeit'].apply(parse_time_to_minutes)
        df['Gesamtzeit_h'] = df['Gesamtzeit_min'] / 60  # Convert duration strings to numeric values for aggregations.
        
        return df
    except Exception:
        return pd.DataFrame()
