"""Layout components and styling for the Screen Time Dashboard."""
import streamlit as st

def apply_custom_css():
    """Inject custom CSS styles into the Streamlit application for better typography and visual styling."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600&display=swap');
    html, body, [class*="css"] { font-family: 'Fredoka', sans-serif !important; }
    h1, h2, h3, h4, h5, h6 { font-family: 'Fredoka', cursive !important; color: #5c6b73 !important; }
    </style>
    """, unsafe_allow_html=True)

def render_sidebar(df):
    """Render the sidebar filter controls and return the selected date range.

    Args:
        df (pd.DataFrame): The dataset used to determine the minimum and maximum dates available.

    Returns:
        tuple: A tuple containing the selected start and end dates.
    """
    st.sidebar.markdown("---")
    st.sidebar.header("Zeitraum filtern")
    min_date = df['Datum'].min().date()
    max_date = df['Datum'].max().date()
    
    if min_date == max_date:
        selected_dates = (min_date, max_date)
        st.sidebar.info("Aktuell ist nur ein einziger Tag verfügbar.")
    else:
        selected_dates = st.sidebar.slider(
            "Wähle den Zeitraum:",
            min_value=min_date,
            max_value=max_date,
            value=(min_date, max_date),
            format="DD.MM.YYYY"
        )
    return selected_dates
