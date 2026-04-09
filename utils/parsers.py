import pandas as pd
import re

APP_CATEGORIES = {
    'Instagram': 'Social Media',
    'TikTok': 'Social Media',
    'Reddit': 'Social Media',
    'Snapchat': 'Social Media',
    'Spotify': 'Medien & Unterhaltung',
    'YouTube': 'Medien & Unterhaltung',
    'Twitch': 'Medien & Unterhaltung',
    'Video_Lite': 'Medien & Unterhaltung',
    'IMDb': 'Medien & Unterhaltung',
    'WhatsApp': 'Kommunikation',
    'Safari': 'Produktivität & Tools',
    'Mail': 'Produktivität & Tools',
    'Perplexity': 'Produktivität & Tools',
    'DB_Navigator': 'Produktivität & Tools',
    'Google_Maps': 'Produktivität & Tools',
    'Clash_of_Clans': 'Spiele'
}

def parse_time_to_minutes(time_str):
    """Konvertiert Zeiten-Strings wie '1h 20m', '45m' in Minuten"""
    if pd.isna(time_str):
        return 0
    time_str = str(time_str).lower().strip()
    
    h_match = re.search(r'(\d+)h', time_str)
    m_match = re.search(r'(\d+)m', time_str)
    
    hours = int(h_match.group(1)) if h_match else 0
    minutes = int(m_match.group(1)) if m_match else 0
        
    return hours * 60 + minutes

def prepare_app_dataframe(filtered_df):
    """Extrahiert die 5 App-Spalten in ein langes DataFrame und berechnet Zeiten."""
    app_data = []
    for i in range(1, 6):
        temp_df = filtered_df[['Datum', f'App{i}_Name', f'App{i}_Zeit']].copy()
        temp_df.columns = ['Datum', 'App_Name', 'App_Zeit']
        app_data.append(temp_df)
    
    app_df = pd.concat(app_data, ignore_index=True)
    # Leere App-Einträge entfernen
    app_df = app_df.dropna(subset=['App_Name'])
    app_df = app_df[app_df['App_Name'] != '']
    
    app_df['Kategorie'] = app_df['App_Name'].map(APP_CATEGORIES).fillna('Sonstiges')
    
    app_df['App_Zeit_min'] = app_df['App_Zeit'].apply(parse_time_to_minutes)
    app_df['App_Zeit_h'] = app_df['App_Zeit_min'] / 60
    return app_df
