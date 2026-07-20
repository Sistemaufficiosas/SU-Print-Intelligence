import sqlite3
from pathlib import Path
from typing import Any


class DatabaseService:
    """Gestisce il database locale di SU Print Intelligence."""

    def __init__(self) -> None:
        project_root = Path(__file__).resolve().parents[2]
        data_directory = project_root / "data"
        data_directory.mkdir(parents=True, exist_ok=True)

        self.database_path = data_directory / "su_print_intelligence.db"
        self.create_tables()

    def connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def create_tables(self) -> None:
        with self.connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS printers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    brand TEXT,
                    model TEXT,
                    technology TEXT,
                    location TEXT,
                    ip_address TEXT,
                    serial_number TEXT,
                    status TEXT NOT NULL DEFAULT 'Attiva',
                    notes TEXT,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            connection.commit()

    def add_printer(
        self,
        name: str,
        brand: str,
        model: str,
        technology: str,
        location: str,
        ip_address: str,
        serial_number: str,
        status: str,
        notes: str,
    ) -> int:
        with self.connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO printers (
                    name,
                    brand,
                    model,
                    technology,
                    location,
                    ip_address,
                    serial_number,
                    status,
                    notes
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    name,
                    brand,
                    model,
                    technology,
                    location,
                    ip_address,
                    serial_number,
                    status,
                    notes,
                ),
            )
            connection.commit()
            return int(cursor.lastrowid)

    def get_printers(self) -> list[dict[str, Any]]:
        with self.connect() as connection:
            rows = connection.execute(
                """
                SELECT *
                FROM printers
                ORDER BY name COLLATE NOCASE
                """
            ).fetchall()

        return [dict(row) for row in rows]

    def delete_printer(self, printer_id: int) -> None:
        with self.connect() as connection:
            connection.execute(
                "DELETE FROM printers WHERE id = ?",
                (printer_id,),
            )
            connection.commit()

    def count_active_printers(self) -> int:
        with self.connect() as connection:
            row = connection.execute(
                """
                SELECT COUNT(*) AS total
                FROM printers
                WHERE status = 'Attiva'
                """
            ).fetchone()

        return int(row["total"])