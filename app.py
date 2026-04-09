import streamlit as st

# Konfiguration der Seite MUSS immer oben stehen
st.set_page_config(page_title="Screen Time Dashboard", layout="wide")

# Eigene Importe
from data.database import load_data
from utils.parsers import prepare_app_dataframe
from components.layout import apply_custom_css, render_sidebar
from components.kpis import render_kpis
from components.charts import render_timeline_chart, render_apps_stacked_bar, render_small_charts

def main():
    apply_custom_css()
    
    st.title("Screen Time Dashboard")
    
    # 1. User Auswählen
    st.sidebar.header("Benutzer-Auswahl")
    users = ["Jon", "Anna (Test)", "Max (Test)"]
    selected_user = st.sidebar.selectbox("Gruppenmitglied wählen", users)
    
    # 2. Daten laden
    df = load_data(selected_user)
    
    if df.empty:
        st.warning(f"Keine Daten für '{selected_user}' in der Datenbank (screentime.db) gefunden.")
        return
        
    # 3. Zeitraum Filtern
    selected_dates = render_sidebar(df)
    mask = (df['Datum'].dt.date >= selected_dates[0]) & (df['Datum'].dt.date <= selected_dates[1])
    filtered_df = df.loc[mask].copy()
    
    if filtered_df.empty:
        st.info("Im ausgewählten Zeitraum liegen keine Daten vor.")
        return
        
    st.markdown("---")
    
    # 4. Rohdaten transformieren
    app_df = prepare_app_dataframe(filtered_df)
    top_apps = app_df.groupby('App_Name')['App_Zeit_h'].sum().reset_index()
    
    # 5. UI Elemente Rendern
    render_kpis(filtered_df, top_apps)
    st.markdown("---")
    render_timeline_chart(filtered_df)
    render_apps_stacked_bar(app_df)
    render_small_charts(filtered_df, app_df)

if __name__ == "__main__":
    main()
