import sqlite3
from pathlib import Path
from typing import Any


class DatabaseService:
    """Gestisce il database locale di SU Print Intelligence."""

    def __init__(self) -> None:
        project_root = Path(__file__).resolve().parents[2]
        data_directory = project_root / "data"
        data_directory.mkdir(parents=True, exist_ok=True)

        self.database_path = (
            data_directory / "su_print_intelligence.db"
        )

        self.create_tables()
        self.update_database_structure()

    def connect(self) -> sqlite3.Connection:
        """Apre una connessione al database SQLite."""

        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")

        return connection

    def create_tables(self) -> None:
        """Crea le tabelle principali quando non esistono."""

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

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS printer_counters (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    printer_id INTEGER NOT NULL,
                    counter_date TEXT NOT NULL DEFAULT CURRENT_DATE,
                    black_counter INTEGER NOT NULL DEFAULT 0,
                    color_counter INTEGER NOT NULL DEFAULT 0,
                    total_counter INTEGER NOT NULL DEFAULT 0,
                    notes TEXT,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (printer_id)
                        REFERENCES printers(id)
                        ON DELETE CASCADE
                )
                """
            )

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS printer_interventions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    printer_id INTEGER NOT NULL,
                    intervention_date TEXT NOT NULL DEFAULT CURRENT_DATE,
                    intervention_type TEXT,
                    error_code TEXT,
                    description TEXT NOT NULL,
                    solution TEXT,
                    replaced_parts TEXT,
                    technician TEXT,
                    counter_value INTEGER NOT NULL DEFAULT 0,
                    cost REAL NOT NULL DEFAULT 0,
                    notes TEXT,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (printer_id)
                        REFERENCES printers(id)
                        ON DELETE CASCADE
                )
                """
            )

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS printer_documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    printer_id INTEGER NOT NULL,
                    document_type TEXT NOT NULL,
                    title TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    notes TEXT,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (printer_id)
                        REFERENCES printers(id)
                        ON DELETE CASCADE
                )
                """
            )

            connection.commit()

    def update_database_structure(self) -> None:
        """
        Aggiunge in sicurezza i nuovi campi alle installazioni
        esistenti, senza cancellare le stampanti già registrate.
        """

        new_columns = {
            "mac_address": "TEXT",
            "firmware": "TEXT",
            "driver": "TEXT",
            "customer_name": "TEXT",
            "customer_location": "TEXT",
            "installation_date": "TEXT",
            "contract_type": "TEXT",
            "contract_number": "TEXT",
            "black_cost_per_copy": "REAL NOT NULL DEFAULT 0",
            "color_cost_per_copy": "REAL NOT NULL DEFAULT 0",
            "black_counter": "INTEGER NOT NULL DEFAULT 0",
            "color_counter": "INTEGER NOT NULL DEFAULT 0",
            "total_counter": "INTEGER NOT NULL DEFAULT 0",
            "last_maintenance": "TEXT",
            "next_maintenance": "TEXT",
            "photo_path": "TEXT",
            "technical_knowledge": "TEXT",
            "updated_at": "TEXT",
        }

        with self.connect() as connection:
            existing_columns = {
                row["name"]
                for row in connection.execute(
                    "PRAGMA table_info(printers)"
                ).fetchall()
            }

            for column_name, column_definition in (
                new_columns.items()
            ):
                if column_name in existing_columns:
                    continue

                connection.execute(
                    f"""
                    ALTER TABLE printers
                    ADD COLUMN {column_name} {column_definition}
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
        mac_address: str = "",
        firmware: str = "",
        driver: str = "",
        customer_name: str = "",
        customer_location: str = "",
        installation_date: str = "",
        contract_type: str = "",
        contract_number: str = "",
        black_cost_per_copy: float = 0,
        color_cost_per_copy: float = 0,
    ) -> int:
        """Inserisce una nuova stampante nel database."""

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
                    notes,
                    mac_address,
                    firmware,
                    driver,
                    customer_name,
                    customer_location,
                    installation_date,
                    contract_type,
                    contract_number,
                    black_cost_per_copy,
                    color_cost_per_copy,
                    updated_at
                )
                VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?, ?, ?, ?,
                    CURRENT_TIMESTAMP
                )
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
                    mac_address,
                    firmware,
                    driver,
                    customer_name,
                    customer_location,
                    installation_date,
                    contract_type,
                    contract_number,
                    black_cost_per_copy,
                    color_cost_per_copy,
                ),
            )

            connection.commit()

            if cursor.lastrowid is None:
                raise RuntimeError(
                    "Impossibile recuperare l'ID della stampante."
                )

            return int(cursor.lastrowid)

    def get_printers(self) -> list[dict[str, Any]]:
        """Restituisce tutte le stampanti registrate."""

        with self.connect() as connection:
            rows = connection.execute(
                """
                SELECT *
                FROM printers
                ORDER BY name COLLATE NOCASE
                """
            ).fetchall()

        return [dict(row) for row in rows]

    def get_printer(
        self,
        printer_id: int,
    ) -> dict[str, Any] | None:
        """Restituisce una singola stampante tramite il suo ID."""

        with self.connect() as connection:
            row = connection.execute(
                """
                SELECT *
                FROM printers
                WHERE id = ?
                """,
                (printer_id,),
            ).fetchone()

        if row is None:
            return None

        return dict(row)

    def update_printer(
        self,
        printer_id: int,
        printer_data: dict[str, Any],
    ) -> None:
        """Aggiorna la scheda generale di una stampante."""

        allowed_fields = {
            "name",
            "brand",
            "model",
            "technology",
            "location",
            "ip_address",
            "mac_address",
            "serial_number",
            "firmware",
            "driver",
            "customer_name",
            "customer_location",
            "installation_date",
            "contract_type",
            "contract_number",
            "black_cost_per_copy",
            "color_cost_per_copy",
            "black_counter",
            "color_counter",
            "total_counter",
            "last_maintenance",
            "next_maintenance",
            "photo_path",
            "status",
            "notes",
            "technical_knowledge",
        }

        fields_to_update = {
            key: value
            for key, value in printer_data.items()
            if key in allowed_fields
        }

        if not fields_to_update:
            return

        assignments = [
            f"{field_name} = ?"
            for field_name in fields_to_update
        ]

        assignments.append("updated_at = CURRENT_TIMESTAMP")

        values = list(fields_to_update.values())
        values.append(printer_id)

        with self.connect() as connection:
            connection.execute(
                f"""
                UPDATE printers
                SET {", ".join(assignments)}
                WHERE id = ?
                """,
                values,
            )

            connection.commit()

    def delete_printer(self, printer_id: int) -> None:
        """Elimina una stampante e i suoi dati collegati."""

        with self.connect() as connection:
            connection.execute(
                """
                DELETE FROM printers
                WHERE id = ?
                """,
                (printer_id,),
            )

            connection.commit()

    def count_active_printers(self) -> int:
        """Conta le stampanti con stato Attiva."""

        with self.connect() as connection:
            row = connection.execute(
                """
                SELECT COUNT(*) AS total
                FROM printers
                WHERE status = 'Attiva'
                """
            ).fetchone()

        return int(row["total"]) if row is not None else 0

    def count_printers_by_status(self) -> dict[str, int]:
        """Restituisce il numero di stampanti per ciascuno stato."""

        result = {
            "Attiva": 0,
            "Manutenzione": 0,
            "Non disponibile": 0,
            "Dismessa": 0,
        }

        with self.connect() as connection:
            rows = connection.execute(
                """
                SELECT status, COUNT(*) AS total
                FROM printers
                GROUP BY status
                """
            ).fetchall()

        for row in rows:
            status = str(row["status"])
            result[status] = int(row["total"])

        return result

    def add_counter_reading(
        self,
        printer_id: int,
        counter_date: str,
        black_counter: int,
        color_counter: int,
        total_counter: int,
        notes: str = "",
    ) -> int:
        """Registra una lettura dei contatori."""

        with self.connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO printer_counters (
                    printer_id,
                    counter_date,
                    black_counter,
                    color_counter,
                    total_counter,
                    notes
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    printer_id,
                    counter_date,
                    black_counter,
                    color_counter,
                    total_counter,
                    notes,
                ),
            )

            connection.execute(
                """
                UPDATE printers
                SET
                    black_counter = ?,
                    color_counter = ?,
                    total_counter = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (
                    black_counter,
                    color_counter,
                    total_counter,
                    printer_id,
                ),
            )

            connection.commit()

            if cursor.lastrowid is None:
                raise RuntimeError(
                    "Impossibile salvare la lettura dei contatori."
                )

            return int(cursor.lastrowid)

    def get_counter_history(
        self,
        printer_id: int,
    ) -> list[dict[str, Any]]:
        """Restituisce lo storico dei contatori."""

        with self.connect() as connection:
            rows = connection.execute(
                """
                SELECT *
                FROM printer_counters
                WHERE printer_id = ?
                ORDER BY counter_date DESC, id DESC
                """,
                (printer_id,),
            ).fetchall()

        return [dict(row) for row in rows]

    def add_intervention(
        self,
        printer_id: int,
        intervention_date: str,
        intervention_type: str,
        error_code: str,
        description: str,
        solution: str,
        replaced_parts: str,
        technician: str,
        counter_value: int,
        cost: float,
        notes: str = "",
    ) -> int:
        """Registra un intervento tecnico."""

        with self.connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO printer_interventions (
                    printer_id,
                    intervention_date,
                    intervention_type,
                    error_code,
                    description,
                    solution,
                    replaced_parts,
                    technician,
                    counter_value,
                    cost,
                    notes
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    printer_id,
                    intervention_date,
                    intervention_type,
                    error_code,
                    description,
                    solution,
                    replaced_parts,
                    technician,
                    counter_value,
                    cost,
                    notes,
                ),
            )

            connection.commit()

            if cursor.lastrowid is None:
                raise RuntimeError(
                    "Impossibile salvare l'intervento tecnico."
                )

            return int(cursor.lastrowid)

    def get_interventions(
        self,
        printer_id: int,
    ) -> list[dict[str, Any]]:
        """Restituisce lo storico degli interventi tecnici."""

        with self.connect() as connection:
            rows = connection.execute(
                """
                SELECT *
                FROM printer_interventions
                WHERE printer_id = ?
                ORDER BY intervention_date DESC, id DESC
                """,
                (printer_id,),
            ).fetchall()

        return [dict(row) for row in rows]