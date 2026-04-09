import streamlit as st

def apply_custom_css():
    """Injiziert benutzerdefinierte CSS Stile (Google Fonts etc.)."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600&display=swap');
    html, body, [class*="css"] { font-family: 'Fredoka', sans-serif !important; }
    h1, h2, h3, h4, h5, h6 { font-family: 'Fredoka', cursive !important; color: #5c6b73 !important; }
    </style>
    """, unsafe_allow_html=True)

def render_sidebar(df):
    """Rendert die Sidebar-Filter und gibt das gewählte Datum zurück."""
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
