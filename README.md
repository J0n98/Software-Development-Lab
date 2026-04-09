# Screen Time Dashboard

A modular, Streamlit-based web application to analyze and visualize smartphone usage data.

## Features
- **Clean Architecture:** Separated data logic, components, and utilities in alignment with software engineering standards.
- **Data Persistence:** Fully powered by an SQLite database.
- **Interactive UI:** Dynamic timeline charts, stacked app breakdown, and summary KPIs built with Plotly.

## Project Structure
```text
screentime_project/
├── app.py                  # Main Streamlit application
├── components/             # UI elements (Charts, KPIs, Sidebar)
├── data/                   # Database logic and loading functions
├── utils/                  # Mathematical and string parsers
├── scripts/                # Standalone CLI tools (Tracker)
└── requirements.txt        # Python dependencies
```

## How to Run

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Launch the Dashboard:**
   ```bash
   streamlit run app.py
   ```
3. **Track new data:**
   ```bash
   python scripts/tracker.py
   ```
