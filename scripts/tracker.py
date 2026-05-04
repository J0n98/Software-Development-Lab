"""CLI tool for manually inserting screen time daily records into the SQLite database."""

import os
import sqlite3


def main():
    """Run the interactive tracker application to collect and save screen time data."""
    print("📱 --- Tages-Screen-Time Tracker --- 📱")
    username = input(
        "Für welchen Nutzer möchtest du Daten eintragen? (z.B. Daniel): "
    ).strip()
    if not username:
        username = "Test"
    print(
        f"INFO: Jeder eingegebene Tag wird an die 'screentime.db' (User: {username}) angehängt.\n"
    )

    while True:
        try:
            num_days = int(
                input(
                    "Wie viele Tage möchtest du dieses Mal eintragen? (z.B. 1 oder 7): "
                ).strip()
            )
            if num_days > 0:
                break
        except ValueError:
            print("Bitte eine Zahl eingeben.")

    records = []

    for d in range(num_days):
        print(f"\n--- TAG {d + 1} VON {num_days} ---")
        datum = input("Datum (z.B. 2026-04-01): ").strip()
        wochentag = input("Wochentag (z.B. Montag): ").strip()
        total_time = input(
            f"Gesamte Bildschirmzeit am {wochentag} (z.B. 4h 30m): "
        ).strip()

        print(f"\nBitte die 5 meistgenutzten Apps am {wochentag} eingeben:")
        row_data = {"Datum": datum, "Wochentag": wochentag, "Gesamtzeit": total_time}

        for i in range(1, 6):
            app_name = input(f"  App {i} Name: ").strip()
            app_time = input(f"  App {i} Zeit (z.B. 45m): ").strip()
            row_data[f"App{i}_Name"] = app_name
            row_data[f"App{i}_Zeit"] = app_time

        records.append(row_data)

    # Fix relative path issue to consistently use the database in the project root.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    db_path = os.path.join(project_root, "screentime.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create the table if missing to prevent SQL errors when running on fresh setups.
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        Datum TEXT,
        Wochentag TEXT,
        Gesamtzeit TEXT,
        App1_Name TEXT, App1_Zeit TEXT,
        App2_Name TEXT, App2_Zeit TEXT,
        App3_Name TEXT, App3_Zeit TEXT,
        App4_Name TEXT, App4_Zeit TEXT,
        App5_Name TEXT, App5_Zeit TEXT
    )
    """)

    for row in records:
        cursor.execute(
            """
        INSERT INTO records (
            username, Datum, Wochentag, Gesamtzeit,
            App1_Name, App1_Zeit, App2_Name, App2_Zeit,
            App3_Name, App3_Zeit, App4_Name, App4_Zeit,
            App5_Name, App5_Zeit
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                username,
                row["Datum"],
                row["Wochentag"],
                row["Gesamtzeit"],
                row.get("App1_Name", ""),
                row.get("App1_Zeit", ""),
                row.get("App2_Name", ""),
                row.get("App2_Zeit", ""),
                row.get("App3_Name", ""),
                row.get("App3_Zeit", ""),
                row.get("App4_Name", ""),
                row.get("App4_Zeit", ""),
                row.get("App5_Name", ""),
                row.get("App5_Zeit", ""),
            ),
        )

    conn.commit()
    conn.close()

    print(
        f"\n✅ Erfolgreich! {num_days} Tag(e) wurden als neue Zeilen in '{db_path}' angefügt."
    )


if __name__ == "__main__":
    main()
