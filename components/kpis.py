"""KPI rendering components for the Screen Time Dashboard."""
import streamlit as st
import pandas as pd

def render_kpis(filtered_df: pd.DataFrame, top_apps: pd.DataFrame) -> None:
    """Render the main Key Performance Indicator (KPI) metric cards.

    Args:
        filtered_df (pd.DataFrame): The filtered dataset for calculating overall metrics.
        top_apps (pd.DataFrame): The dataset aggregated by app to find the most used app.
    """
    st.subheader("Statistische Kennzahlen")
    col1, col2, col3, col4 = st.columns(4)
    
    avg_screen_time_h = filtered_df['Gesamtzeit_h'].mean()
    total_screen_time_h = filtered_df['Gesamtzeit_h'].sum()
    
    weekday_grouped = filtered_df.groupby('Wochentag')['Gesamtzeit_h'].mean().reset_index()
    most_used_weekday = weekday_grouped.loc[weekday_grouped['Gesamtzeit_h'].idxmax()]['Wochentag'] if not weekday_grouped.empty else "-"
    most_used_app = top_apps.loc[top_apps['App_Zeit_h'].idxmax()]['App_Name'] if not top_apps.empty else "-"
    
    col1.metric("Ø Bildschirmzeit / Tag", f"{avg_screen_time_h:.1f} Std")
    col2.metric("Gesamte Bildschirmzeit", f"{total_screen_time_h:.1f} Std")
    col3.metric("Meistgenutzter Wochentag", f"{most_used_weekday}")
    col4.metric("Nummer #1 App", f"{most_used_app}")
