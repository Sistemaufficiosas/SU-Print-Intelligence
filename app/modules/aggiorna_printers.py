from pathlib import Path


file_path = Path("app/modules/printers.py")

text = file_path.read_text(encoding="utf-8")


# Aggiunge l'import della Cartella tecnica
old_import = (
    "from app.services.database_service "
    "import DatabaseService"
)

new_import = (
    "from app.modules.printer_detail "
    "import PrinterDetailDialog\n"
    "from app.services.database_service "
    "import DatabaseService"
)

if "PrinterDetailDialog" not in text:
    text = text.replace(
        old_import,
        new_import,
        1,
    )


# Collega il doppio clic alla Cartella tecnica
text = text.replace(
    """self.table.doubleClicked.connect(
            self.open_edit_dialog
        )""",
    """self.table.doubleClicked.connect(
            self.open_detail_dialog
        )""",
    1,
)


# Aggiunge il nuovo metodo automaticamente
new_method = '''    def open_detail_dialog(self) -> None:
        """Apre la cartella tecnica della stampante selezionata."""

        printer_id = self.get_selected_printer_id()

        if printer_id is None:
            QMessageBox.warning(
                self,
                "Nessuna stampante selezionata",
                "Seleziona una stampante dall’elenco.",
            )
            return

        dialog = PrinterDetailDialog(
            database=self.database,
            printer_id=printer_id,
            parent=self,
        )
        dialog.exec()

'''

marker = "    def open_edit_dialog(self) -> None:\n"

if "def open_detail_dialog(self)" not in text:
    text = text.replace(
        marker,
        new_method + marker,
        1,
    )


file_path.write_text(
    text,
    encoding="utf-8",
)

print("MODIFICA COMPLETATA CORRETTAMENTE")