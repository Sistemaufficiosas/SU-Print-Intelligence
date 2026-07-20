from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from app.services.database_service import DatabaseService


class PrinterDialog(QDialog):
    """Finestra per inserire una nuova stampante."""

    printer_saved = Signal()

    def __init__(
        self,
        database: DatabaseService,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.database = database

        self.setWindowTitle("Nuova stampante")
        self.setMinimumWidth(520)

        self.create_interface()

    def create_interface(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 22, 24, 22)
        main_layout.setSpacing(16)

        title = QLabel("Inserisci una nuova stampante")
        title.setStyleSheet(
            "font-size: 20px; font-weight: 700; color: #18243a;"
        )

        description = QLabel(
            "Compila almeno il nome identificativo della stampante."
        )
        description.setStyleSheet("color: #748094;")

        main_layout.addWidget(title)
        main_layout.addWidget(description)

        form = QFormLayout()
        form.setSpacing(12)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText(
            "Esempio: Bizhub C368 laboratorio"
        )

        self.brand_input = QLineEdit()
        self.brand_input.setPlaceholderText("Esempio: Konica Minolta")

        self.model_input = QLineEdit()
        self.model_input.setPlaceholderText("Esempio: Bizhub C368")

        self.technology_input = QComboBox()
        self.technology_input.addItems(
            [
                "Laser colore",
                "Laser monocromatica",
                "Inkjet",
                "Plotter",
                "Sublimazione",
                "Etichette",
                "Stampa 3D",
                "Altro",
            ]
        )

        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText(
            "Esempio: Centro stampa"
        )

        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("Esempio: 192.168.1.100")

        self.serial_input = QLineEdit()
        self.serial_input.setPlaceholderText("Numero di serie")

        self.status_input = QComboBox()
        self.status_input.addItems(
            [
                "Attiva",
                "Manutenzione",
                "Non disponibile",
                "Dismessa",
            ]
        )

        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText(
            "Note tecniche, accessori, contatori o altre informazioni..."
        )
        self.notes_input.setMaximumHeight(90)

        form.addRow("Nome identificativo *", self.name_input)
        form.addRow("Marca", self.brand_input)
        form.addRow("Modello", self.model_input)
        form.addRow("Tecnologia", self.technology_input)
        form.addRow("Posizione", self.location_input)
        form.addRow("Indirizzo IP", self.ip_input)
        form.addRow("Numero di serie", self.serial_input)
        form.addRow("Stato", self.status_input)
        form.addRow("Note", self.notes_input)

        main_layout.addLayout(form)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )

        save_button = buttons.button(
            QDialogButtonBox.StandardButton.Save
        )
        save_button.setText("Salva stampante")

        cancel_button = buttons.button(
            QDialogButtonBox.StandardButton.Cancel
        )
        cancel_button.setText("Annulla")

        buttons.accepted.connect(self.save_printer)
        buttons.rejected.connect(self.reject)

        main_layout.addWidget(buttons)

    def save_printer(self) -> None:
        name = self.name_input.text().strip()

        if not name:
            QMessageBox.warning(
                self,
                "Dato obbligatorio",
                "Inserisci il nome identificativo della stampante.",
            )
            self.name_input.setFocus()
            return

        self.database.add_printer(
            name=name,
            brand=self.brand_input.text().strip(),
            model=self.model_input.text().strip(),
            technology=self.technology_input.currentText(),
            location=self.location_input.text().strip(),
            ip_address=self.ip_input.text().strip(),
            serial_number=self.serial_input.text().strip(),
            status=self.status_input.currentText(),
            notes=self.notes_input.toPlainText().strip(),
        )

        self.printer_saved.emit()
        self.accept()


class PrintersWidget(QWidget):
    """Schermata principale per la gestione delle stampanti."""

    printers_changed = Signal()

    def __init__(
        self,
        database: DatabaseService,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.database = database
        self.create_interface()
        self.load_printers()

    def create_interface(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 26, 32, 26)
        layout.setSpacing(18)

        header_layout = QHBoxLayout()

        title_layout = QVBoxLayout()
        title_layout.setSpacing(3)

        title = QLabel("Stampanti")
        title.setStyleSheet(
            "font-size: 28px; font-weight: 700; color: #172238;"
        )

        subtitle = QLabel(
            "Gestione delle stampanti, dei plotter e dei dispositivi di produzione"
        )
        subtitle.setStyleSheet("color: #748094;")

        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)

        add_button = QPushButton("＋  Nuova stampante")
        add_button.setCursor(Qt.CursorShape.PointingHandCursor)
        add_button.setStyleSheet(
            """
            QPushButton {
                background-color: #2f7de1;
                color: white;
                border: none;
                border-radius: 7px;
                padding: 12px 18px;
                font-weight: 600;
            }

            QPushButton:hover {
                background-color: #216bc9;
            }
            """
        )
        add_button.clicked.connect(self.open_add_dialog)

        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        header_layout.addWidget(add_button)

        layout.addLayout(header_layout)

        self.summary_label = QLabel()
        self.summary_label.setStyleSheet(
            """
            background-color: white;
            border: 1px solid #e1e6ee;
            border-radius: 8px;
            padding: 12px;
            color: #26344a;
            font-weight: 600;
            """
        )

        layout.addWidget(self.summary_label)

        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(
            [
                "ID",
                "Nome",
                "Marca",
                "Modello",
                "Tecnologia",
                "Posizione",
                "Indirizzo IP",
                "Stato",
            ]
        )

        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.table.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )
        self.table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        header.setSectionResizeMode(
            1,
            QHeaderView.ResizeMode.Stretch,
        )

        self.table.setStyleSheet(
            """
            QTableWidget {
                background-color: white;
                alternate-background-color: #f8fafc;
                border: 1px solid #e1e6ee;
                border-radius: 8px;
                gridline-color: #edf0f4;
                selection-background-color: #dceafe;
                selection-color: #172238;
            }

            QHeaderView::section {
                background-color: #edf2f8;
                color: #536176;
                border: none;
                border-bottom: 1px solid #d9e0e9;
                padding: 10px;
                font-weight: 600;
            }

            QTableWidget::item {
                padding: 8px;
            }
            """
        )

        layout.addWidget(self.table, 1)

        bottom_layout = QHBoxLayout()

        delete_button = QPushButton("Elimina stampante selezionata")
        delete_button.setCursor(Qt.CursorShape.PointingHandCursor)
        delete_button.clicked.connect(self.delete_selected_printer)

        refresh_button = QPushButton("Aggiorna elenco")
        refresh_button.setCursor(Qt.CursorShape.PointingHandCursor)
        refresh_button.clicked.connect(self.load_printers)

        bottom_layout.addWidget(delete_button)
        bottom_layout.addStretch()
        bottom_layout.addWidget(refresh_button)

        layout.addLayout(bottom_layout)

    def open_add_dialog(self) -> None:
        dialog = PrinterDialog(self.database, self)
        dialog.printer_saved.connect(self.load_printers)
        dialog.printer_saved.connect(self.printers_changed.emit)
        dialog.exec()

    def load_printers(self) -> None:
        printers = self.database.get_printers()

        self.table.setRowCount(len(printers))

        for row_index, printer in enumerate(printers):
            values = [
                printer["id"],
                printer["name"],
                printer["brand"],
                printer["model"],
                printer["technology"],
                printer["location"],
                printer["ip_address"],
                printer["status"],
            ]

            for column_index, value in enumerate(values):
                item = QTableWidgetItem(str(value or ""))
                self.table.setItem(
                    row_index,
                    column_index,
                    item,
                )

        active_count = self.database.count_active_printers()

        self.summary_label.setText(
            f"Stampanti registrate: {len(printers)}"
            f"     •     Stampanti attive: {active_count}"
        )

    def delete_selected_printer(self) -> None:
        selected_rows = self.table.selectionModel().selectedRows()

        if not selected_rows:
            QMessageBox.warning(
                self,
                "Nessuna stampante selezionata",
                "Seleziona una stampante dall’elenco.",
            )
            return

        selected_row = selected_rows[0].row()

        printer_id_item = self.table.item(selected_row, 0)
        printer_name_item = self.table.item(selected_row, 1)

        if printer_id_item is None:
            return

        printer_id = int(printer_id_item.text())
        printer_name = (
            printer_name_item.text()
            if printer_name_item is not None
            else "stampante selezionata"
        )

        response = QMessageBox.question(
            self,
            "Conferma eliminazione",
            f"Vuoi eliminare «{printer_name}»?",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
        )

        if response != QMessageBox.StandardButton.Yes:
            return

        self.database.delete_printer(printer_id)
        self.load_printers()
        self.printers_changed.emit()