"""Main entry point for the Streamlit Screen Time Dashboard application."""
import streamlit as st

st.set_page_config(page_title="Screen Time Dashboard", layout="wide")  # Configuration must be the first command to avoid Streamlit errors.

from data.database import load_data
from utils.parsers import prepare_app_dataframe
from components.layout import apply_custom_css, render_sidebar
from components.kpis import render_kpis
from components.charts import render_timeline_chart, render_apps_stacked_bar, render_small_charts

def main():
    """Execute the core application logic to render the Streamlit dashboard."""
    apply_custom_css()
    
    st.title("Screen Time Dashboard")
    
    st.sidebar.header("Benutzer-Auswahl")
    users = ["Jon", "Alban", "Daniel"]
    selected_user = st.sidebar.selectbox("Gruppenmitglied wählen", users)  # Allow team members to switch between their usage data.
    
    df = load_data(selected_user)
    
    if df.empty:
        st.warning(f"Keine Daten für '{selected_user}' in der Datenbank (screentime.db) gefunden.")
        return
        
    selected_dates = render_sidebar(df)
    mask = (df['Datum'].dt.date >= selected_dates[0]) & (df['Datum'].dt.date <= selected_dates[1])
    filtered_df = df.loc[mask].copy()
    
    if filtered_df.empty:
        st.info("Im ausgewählten Zeitraum liegen keine Daten vor.")
        return
        
    st.markdown("---")
    
    app_df = prepare_app_dataframe(filtered_df)
    top_apps = app_df.groupby('App_Name')['App_Zeit_h'].sum().reset_index()
    
    render_kpis(filtered_df, top_apps)
    st.markdown("---")
    render_timeline_chart(filtered_df)
    render_apps_stacked_bar(app_df)
    render_small_charts(filtered_df, app_df)

if __name__ == "__main__":
    main()
