"""Plotly chart rendering components for the Screen Time Dashboard."""

import streamlit as st
import plotly.express as px
import pandas as pd


def render_timeline_chart(filtered_df: pd.DataFrame) -> None:
    """Render a line chart showing the total screen time over the selected period.

    Args:
        filtered_df (pd.DataFrame): The filtered dataset containing full daily records.
    """
    st.subheader("Entwicklung der Gesamten Bildschirmzeit")
    df_timeline = filtered_df.sort_values(by="Datum")
    fig_timeline = px.line(
        df_timeline,
        x="Datum",
        y="Gesamtzeit_h",
        markers=True,
        labels={"Gesamtzeit_h": "Bildschirmzeit (Stunden)"},
        line_shape="spline",
        color_discrete_sequence=["#829eb9"],
    )
    fig_timeline.update_layout(
        yaxis_range=[0, max(filtered_df["Gesamtzeit_h"].max() * 1.2, 1)],
        template="simple_white",
        font=dict(family="Fredoka, sans-serif"),
    )
    st.plotly_chart(fig_timeline, width="stretch")


def render_apps_stacked_bar(app_df: pd.DataFrame) -> None:
    """Render a stacked bar chart displaying time spent per app category over time.

    Args:
        app_df (pd.DataFrame): The long-format DataFrame with individual app usage records.
    """
    st.subheader("Aufteilung der Kategorien pro Tag")

    cat_df = (
        app_df.groupby(["Datum", "Kategorie"])["App_Zeit_h"].sum().reset_index()
    )  # Aggregate data by category to create clean stacked blocks per day.
    cat_df_timeline = cat_df.sort_values(by="Datum")

    fig_apps = px.bar(
        cat_df_timeline,
        x="Datum",
        y="App_Zeit_h",
        color="Kategorie",
        labels={
            "App_Zeit_h": "Zeit (Stunden)",
            "Kategorie": "Kategorie",
            "Datum": "Datum",
        },
        title="Tagesverlauf der Kategorien-Nutzung",
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )
    fig_apps.update_layout(
        template="simple_white",
        barmode="stack",
        font=dict(family="Fredoka, sans-serif"),
    )
    fig_apps.update_traces(marker_cornerradius=10)
    st.plotly_chart(fig_apps, width="stretch")


def render_small_charts(filtered_df: pd.DataFrame, app_df: pd.DataFrame) -> None:
    """Render side-by-side charts for average weekday usage and category distribution.

    Args:
        filtered_df (pd.DataFrame): The filtered dataset containing full daily records.
        app_df (pd.DataFrame): The long-format DataFrame with individual app usage records.
    """
    st.markdown("---")
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.subheader("Ø Zeit je Wochentag")
        weekday_grouped = (
            filtered_df.groupby("Wochentag")["Gesamtzeit_h"].mean().reset_index()
        )
        week_order = [
            "Montag",
            "Dienstag",
            "Mittwoch",
            "Donnerstag",
            "Freitag",
            "Samstag",
            "Sonntag",
        ]
        existing_days = [
            d for d in week_order if d in weekday_grouped["Wochentag"].values
        ]

        if not weekday_grouped.empty:
            fig_weekdays = px.bar(
                weekday_grouped,
                x="Wochentag",
                y="Gesamtzeit_h",
                category_orders={"Wochentag": existing_days},
                labels={"Gesamtzeit_h": "Ø Zeit (Stunden)", "Wochentag": "Tag"},
                color_discrete_sequence=["#a3b8cc"],
            )
            fig_weekdays.update_layout(
                template="simple_white", font=dict(family="Fredoka, sans-serif")
            )
            fig_weekdays.update_traces(marker_cornerradius=10)
            st.plotly_chart(fig_weekdays, width="stretch")

    with col_chart2:
        st.subheader("Anteil der Kategorien am Gesamtverbrauch")
        if not app_df.empty:
            cat_grouped = app_df.groupby("Kategorie")["App_Zeit_h"].sum().reset_index()
            cat_sorted = cat_grouped.sort_values("App_Zeit_h", ascending=False)
            fig_pie = px.pie(
                cat_sorted,
                values="App_Zeit_h",
                names="Kategorie",
                hole=0.5,
                color_discrete_sequence=px.colors.qualitative.Pastel,
            )
            fig_pie.update_traces(textposition="inside", textinfo="percent+label")
            fig_pie.update_layout(
                template="simple_white",
                showlegend=False,
                font=dict(family="Fredoka, sans-serif"),
            )
            st.plotly_chart(fig_pie, width="stretch")
