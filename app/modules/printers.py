from __future__ import annotations

from typing import Any

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from app.services.database_service import DatabaseService


class PrinterDialog(QDialog):
    """Finestra per inserire o modificare una stampante."""

    printer_saved = Signal()

    def __init__(
        self,
        database: DatabaseService,
        printer_id: int | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.database = database
        self.printer_id = printer_id
        self.printer_data: dict[str, Any] | None = None

        if self.printer_id is not None:
            self.printer_data = self.database.get_printer(
                self.printer_id
            )

        self.setWindowTitle(
            "Modifica stampante"
            if self.printer_id is not None
            else "Nuova stampante"
        )
        self.resize(760, 720)
        self.setMinimumSize(680, 620)

        self.create_interface()

        if self.printer_data is not None:
            self.load_printer_data()

    def create_interface(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 22, 24, 22)
        main_layout.setSpacing(16)

        title = QLabel(
            "Modifica scheda stampante"
            if self.printer_id is not None
            else "Inserisci una nuova stampante"
        )
        title.setObjectName("dialogTitle")

        description = QLabel(
            "Compila i dati generali, tecnici e contrattuali "
            "della macchina."
        )
        description.setObjectName("dialogSubtitle")

        main_layout.addWidget(title)
        main_layout.addWidget(description)

        tabs = QTabWidget()
        tabs.setObjectName("printerTabs")

        tabs.addTab(
            self.create_general_tab(),
            "Generale",
        )
        tabs.addTab(
            self.create_technical_tab(),
            "Rete e software",
        )
        tabs.addTab(
            self.create_contract_tab(),
            "Cliente e contratto",
        )
        tabs.addTab(
            self.create_counters_tab(),
            "Contatori",
        )
        tabs.addTab(
            self.create_maintenance_tab(),
            "Manutenzione",
        )
        tabs.addTab(
            self.create_notes_tab(),
            "Note tecniche",
        )

        main_layout.addWidget(tabs, 1)

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

    def create_general_tab(self) -> QWidget:
        tab = QWidget()
        form = QFormLayout(tab)
        form.setContentsMargins(18, 20, 18, 20)
        form.setSpacing(14)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText(
            "Esempio: Bizhub C368 laboratorio"
        )

        self.brand_input = QLineEdit()
        self.brand_input.setPlaceholderText(
            "Esempio: Konica Minolta"
        )

        self.model_input = QLineEdit()
        self.model_input.setPlaceholderText(
            "Esempio: Bizhub C368"
        )

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

        self.serial_input = QLineEdit()
        self.serial_input.setPlaceholderText(
            "Numero di serie"
        )

        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText(
            "Esempio: Laboratorio"
        )

        self.status_input = QComboBox()
        self.status_input.addItems(
            [
                "Attiva",
                "Manutenzione",
                "Non disponibile",
                "Dismessa",
            ]
        )

        self.installation_date_input = QLineEdit()
        self.installation_date_input.setPlaceholderText(
            "GG/MM/AAAA"
        )

        form.addRow("Nome identificativo *", self.name_input)
        form.addRow("Marca", self.brand_input)
        form.addRow("Modello", self.model_input)
        form.addRow("Tecnologia", self.technology_input)
        form.addRow("Numero di serie", self.serial_input)
        form.addRow("Posizione interna", self.location_input)
        form.addRow("Stato", self.status_input)
        form.addRow(
            "Data installazione",
            self.installation_date_input,
        )

        return tab

    def create_technical_tab(self) -> QWidget:
        tab = QWidget()
        form = QFormLayout(tab)
        form.setContentsMargins(18, 20, 18, 20)
        form.setSpacing(14)

        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText(
            "Esempio: 192.168.1.100"
        )

        self.mac_input = QLineEdit()
        self.mac_input.setPlaceholderText(
            "Esempio: 00:11:22:33:44:55"
        )

        self.firmware_input = QLineEdit()
        self.firmware_input.setPlaceholderText(
            "Versione firmware installata"
        )

        self.driver_input = QLineEdit()
        self.driver_input.setPlaceholderText(
            "Driver utilizzato"
        )

        form.addRow("Indirizzo IP", self.ip_input)
        form.addRow("MAC Address", self.mac_input)
        form.addRow("Firmware", self.firmware_input)
        form.addRow("Driver", self.driver_input)

        return tab

    def create_contract_tab(self) -> QWidget:
        tab = QWidget()
        form = QFormLayout(tab)
        form.setContentsMargins(18, 20, 18, 20)
        form.setSpacing(14)

        self.customer_name_input = QLineEdit()
        self.customer_name_input.setPlaceholderText(
            "Nome cliente o azienda"
        )

        self.customer_location_input = QLineEdit()
        self.customer_location_input.setPlaceholderText(
            "Sede dove è installata la macchina"
        )

        self.contract_type_input = QComboBox()
        self.contract_type_input.addItems(
            [
                "",
                "Proprietà cliente",
                "Noleggio",
                "Costo copia",
                "Assistenza programmata",
                "Uso interno",
                "Altro",
            ]
        )

        self.contract_number_input = QLineEdit()
        self.contract_number_input.setPlaceholderText(
            "Numero contratto"
        )

        self.black_cost_input = QDoubleSpinBox()
        self.black_cost_input.setRange(0, 100)
        self.black_cost_input.setDecimals(5)
        self.black_cost_input.setSuffix(" €")
        self.black_cost_input.setSingleStep(0.001)

        self.color_cost_input = QDoubleSpinBox()
        self.color_cost_input.setRange(0, 100)
        self.color_cost_input.setDecimals(5)
        self.color_cost_input.setSuffix(" €")
        self.color_cost_input.setSingleStep(0.001)

        form.addRow("Cliente", self.customer_name_input)
        form.addRow(
            "Sede cliente",
            self.customer_location_input,
        )
        form.addRow(
            "Tipo contratto",
            self.contract_type_input,
        )
        form.addRow(
            "Numero contratto",
            self.contract_number_input,
        )
        form.addRow(
            "Costo copia B/N",
            self.black_cost_input,
        )
        form.addRow(
            "Costo copia colore",
            self.color_cost_input,
        )

        return tab

    def create_counters_tab(self) -> QWidget:
        tab = QWidget()
        form = QFormLayout(tab)
        form.setContentsMargins(18, 20, 18, 20)
        form.setSpacing(14)

        self.black_counter_input = QSpinBox()
        self.black_counter_input.setRange(
            0,
            2_000_000_000,
        )
        self.black_counter_input.setGroupSeparatorShown(True)

        self.color_counter_input = QSpinBox()
        self.color_counter_input.setRange(
            0,
            2_000_000_000,
        )
        self.color_counter_input.setGroupSeparatorShown(True)

        self.total_counter_input = QSpinBox()
        self.total_counter_input.setRange(
            0,
            2_000_000_000,
        )
        self.total_counter_input.setGroupSeparatorShown(True)

        calculate_button = QPushButton(
            "Calcola totale B/N + colore"
        )
        calculate_button.setObjectName("secondaryButton")
        calculate_button.clicked.connect(
            self.calculate_total_counter
        )

        form.addRow(
            "Contatore B/N",
            self.black_counter_input,
        )
        form.addRow(
            "Contatore colore",
            self.color_counter_input,
        )
        form.addRow(
            "Contatore totale",
            self.total_counter_input,
        )
        form.addRow("", calculate_button)

        return tab

    def create_maintenance_tab(self) -> QWidget:
        tab = QWidget()
        form = QFormLayout(tab)
        form.setContentsMargins(18, 20, 18, 20)
        form.setSpacing(14)

        self.last_maintenance_input = QLineEdit()
        self.last_maintenance_input.setPlaceholderText(
            "GG/MM/AAAA"
        )

        self.next_maintenance_input = QLineEdit()
        self.next_maintenance_input.setPlaceholderText(
            "GG/MM/AAAA"
        )

        form.addRow(
            "Ultima manutenzione",
            self.last_maintenance_input,
        )
        form.addRow(
            "Prossima manutenzione",
            self.next_maintenance_input,
        )

        return tab

    def create_notes_tab(self) -> QWidget:
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(18, 20, 18, 20)
        layout.setSpacing(14)

        notes_label = QLabel("Note generali")
        notes_label.setObjectName("formSectionTitle")

        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText(
            "Note tecniche, accessori, configurazioni, "
            "particolarità della macchina..."
        )

        knowledge_label = QLabel("Conoscenza tecnica")
        knowledge_label.setObjectName("formSectionTitle")

        self.technical_knowledge_input = QTextEdit()
        self.technical_knowledge_input.setPlaceholderText(
            "Guasti ricorrenti, codici errore, soluzioni, "
            "firmware consigliati, ricambi e procedure..."
        )

        layout.addWidget(notes_label)
        layout.addWidget(self.notes_input)
        layout.addWidget(knowledge_label)
        layout.addWidget(self.technical_knowledge_input)

        return tab

    def calculate_total_counter(self) -> None:
        total = (
            self.black_counter_input.value()
            + self.color_counter_input.value()
        )
        self.total_counter_input.setValue(total)

    def load_printer_data(self) -> None:
        if self.printer_data is None:
            return

        data = self.printer_data

        self.name_input.setText(
            str(data.get("name") or "")
        )
        self.brand_input.setText(
            str(data.get("brand") or "")
        )
        self.model_input.setText(
            str(data.get("model") or "")
        )

        self.set_combo_value(
            self.technology_input,
            str(data.get("technology") or ""),
        )

        self.serial_input.setText(
            str(data.get("serial_number") or "")
        )
        self.location_input.setText(
            str(data.get("location") or "")
        )

        self.set_combo_value(
            self.status_input,
            str(data.get("status") or "Attiva"),
        )

        self.installation_date_input.setText(
            str(data.get("installation_date") or "")
        )
        self.ip_input.setText(
            str(data.get("ip_address") or "")
        )
        self.mac_input.setText(
            str(data.get("mac_address") or "")
        )
        self.firmware_input.setText(
            str(data.get("firmware") or "")
        )
        self.driver_input.setText(
            str(data.get("driver") or "")
        )
        self.customer_name_input.setText(
            str(data.get("customer_name") or "")
        )
        self.customer_location_input.setText(
            str(data.get("customer_location") or "")
        )

        self.set_combo_value(
            self.contract_type_input,
            str(data.get("contract_type") or ""),
        )

        self.contract_number_input.setText(
            str(data.get("contract_number") or "")
        )
        self.black_cost_input.setValue(
            float(data.get("black_cost_per_copy") or 0)
        )
        self.color_cost_input.setValue(
            float(data.get("color_cost_per_copy") or 0)
        )
        self.black_counter_input.setValue(
            int(data.get("black_counter") or 0)
        )
        self.color_counter_input.setValue(
            int(data.get("color_counter") or 0)
        )
        self.total_counter_input.setValue(
            int(data.get("total_counter") or 0)
        )
        self.last_maintenance_input.setText(
            str(data.get("last_maintenance") or "")
        )
        self.next_maintenance_input.setText(
            str(data.get("next_maintenance") or "")
        )
        self.notes_input.setPlainText(
            str(data.get("notes") or "")
        )
        self.technical_knowledge_input.setPlainText(
            str(data.get("technical_knowledge") or "")
        )

    @staticmethod
    def set_combo_value(
        combo: QComboBox,
        value: str,
    ) -> None:
        index = combo.findText(value)

        if index >= 0:
            combo.setCurrentIndex(index)

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

        printer_data = {
            "name": name,
            "brand": self.brand_input.text().strip(),
            "model": self.model_input.text().strip(),
            "technology": self.technology_input.currentText(),
            "location": self.location_input.text().strip(),
            "ip_address": self.ip_input.text().strip(),
            "mac_address": self.mac_input.text().strip(),
            "serial_number": self.serial_input.text().strip(),
            "firmware": self.firmware_input.text().strip(),
            "driver": self.driver_input.text().strip(),
            "customer_name": (
                self.customer_name_input.text().strip()
            ),
            "customer_location": (
                self.customer_location_input.text().strip()
            ),
            "installation_date": (
                self.installation_date_input.text().strip()
            ),
            "contract_type": (
                self.contract_type_input.currentText()
            ),
            "contract_number": (
                self.contract_number_input.text().strip()
            ),
            "black_cost_per_copy": (
                self.black_cost_input.value()
            ),
            "color_cost_per_copy": (
                self.color_cost_input.value()
            ),
            "black_counter": (
                self.black_counter_input.value()
            ),
            "color_counter": (
                self.color_counter_input.value()
            ),
            "total_counter": (
                self.total_counter_input.value()
            ),
            "last_maintenance": (
                self.last_maintenance_input.text().strip()
            ),
            "next_maintenance": (
                self.next_maintenance_input.text().strip()
            ),
            "status": self.status_input.currentText(),
            "notes": self.notes_input.toPlainText().strip(),
            "technical_knowledge": (
                self.technical_knowledge_input
                .toPlainText()
                .strip()
            ),
        }

        if self.printer_id is None:
            self.database.add_printer(
                name=printer_data["name"],
                brand=printer_data["brand"],
                model=printer_data["model"],
                technology=printer_data["technology"],
                location=printer_data["location"],
                ip_address=printer_data["ip_address"],
                serial_number=printer_data["serial_number"],
                status=printer_data["status"],
                notes=printer_data["notes"],
                mac_address=printer_data["mac_address"],
                firmware=printer_data["firmware"],
                driver=printer_data["driver"],
                customer_name=printer_data["customer_name"],
                customer_location=(
                    printer_data["customer_location"]
                ),
                installation_date=(
                    printer_data["installation_date"]
                ),
                contract_type=printer_data["contract_type"],
                contract_number=(
                    printer_data["contract_number"]
                ),
                black_cost_per_copy=(
                    printer_data["black_cost_per_copy"]
                ),
                color_cost_per_copy=(
                    printer_data["color_cost_per_copy"]
                ),
            )

            QMessageBox.information(
                self,
                "Stampante salvata",
                "La nuova stampante è stata registrata.",
            )
        else:
            self.database.update_printer(
                self.printer_id,
                printer_data,
            )

            QMessageBox.information(
                self,
                "Modifiche salvate",
                "La scheda della stampante è stata aggiornata.",
            )

        self.printer_saved.emit()
        self.accept()


class PrintersWidget(QWidget):
    """Gestione professionale delle stampanti."""

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
        layout.setContentsMargins(30, 24, 30, 24)
        layout.setSpacing(18)

        layout.addLayout(self.create_header())
        layout.addLayout(self.create_summary_area())

        self.table = QTableWidget()
        self.configure_table()

        layout.addWidget(self.table, 1)
        layout.addLayout(self.create_bottom_buttons())

    def create_header(self) -> QHBoxLayout:
        header_layout = QHBoxLayout()

        title_layout = QVBoxLayout()
        title_layout.setSpacing(3)

        title = QLabel("Gestione Stampanti PRO")
        title.setObjectName("pageTitle")

        subtitle = QLabel(
            "Anagrafica tecnica, clienti, rete, contratti, "
            "contatori e manutenzioni"
        )
        subtitle.setObjectName("pageSubtitle")

        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)

        add_button = QPushButton("＋  Nuova stampante")
        add_button.setObjectName("primaryButton")
        add_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )
        add_button.clicked.connect(self.open_add_dialog)

        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        header_layout.addWidget(add_button)

        return header_layout

    def create_summary_area(self) -> QHBoxLayout:
        layout = QHBoxLayout()
        layout.setSpacing(12)

        self.total_label = self.create_summary_card(
            "Totale",
            "0",
        )
        self.active_label = self.create_summary_card(
            "Attive",
            "0",
        )
        self.maintenance_label = self.create_summary_card(
            "In manutenzione",
            "0",
        )
        self.unavailable_label = self.create_summary_card(
            "Non disponibili",
            "0",
        )

        layout.addWidget(self.total_label)
        layout.addWidget(self.active_label)
        layout.addWidget(self.maintenance_label)
        layout.addWidget(self.unavailable_label)

        return layout

    @staticmethod
    def create_summary_card(
        title: str,
        value: str,
    ) -> QLabel:
        label = QLabel(
            f"<b>{title}</b><br>"
            f"<span style='font-size:22px'>{value}</span>"
        )
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setMinimumHeight(72)
        label.setStyleSheet(
            """
            QLabel {
                background-color: white;
                border: 1px solid #e1e6ee;
                border-radius: 9px;
                color: #26344a;
                padding: 10px;
            }
            """
        )

        return label

    def configure_table(self) -> None:
        self.table.setColumnCount(11)
        self.table.setHorizontalHeaderLabels(
            [
                "ID",
                "Nome",
                "Marca",
                "Modello",
                "Cliente",
                "Posizione",
                "IP",
                "Firmware",
                "B/N",
                "Colore",
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
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.doubleClicked.connect(
            self.open_edit_dialog
        )

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

    def create_bottom_buttons(self) -> QHBoxLayout:
        layout = QHBoxLayout()

        edit_button = QPushButton(
            "Modifica stampante selezionata"
        )
        edit_button.setObjectName("secondaryButton")
        edit_button.clicked.connect(
            self.open_edit_dialog
        )

        delete_button = QPushButton(
            "Elimina stampante selezionata"
        )
        delete_button.clicked.connect(
            self.delete_selected_printer
        )

        refresh_button = QPushButton("Aggiorna elenco")
        refresh_button.clicked.connect(
            self.load_printers
        )

        layout.addWidget(edit_button)
        layout.addWidget(delete_button)
        layout.addStretch()
        layout.addWidget(refresh_button)

        return layout

    def get_selected_printer_id(self) -> int | None:
        selected_rows = (
            self.table.selectionModel().selectedRows()
        )

        if not selected_rows:
            return None

        selected_row = selected_rows[0].row()
        printer_id_item = self.table.item(
            selected_row,
            0,
        )

        if printer_id_item is None:
            return None

        return int(printer_id_item.text())

    def open_add_dialog(self) -> None:
        dialog = PrinterDialog(
            database=self.database,
            parent=self,
        )
        dialog.printer_saved.connect(
            self.handle_printers_changed
        )
        dialog.exec()

    def open_edit_dialog(self) -> None:
        printer_id = self.get_selected_printer_id()

        if printer_id is None:
            QMessageBox.warning(
                self,
                "Nessuna stampante selezionata",
                "Seleziona una stampante dall’elenco.",
            )
            return

        dialog = PrinterDialog(
            database=self.database,
            printer_id=printer_id,
            parent=self,
        )
        dialog.printer_saved.connect(
            self.handle_printers_changed
        )
        dialog.exec()

    def handle_printers_changed(self) -> None:
        self.load_printers()
        self.printers_changed.emit()

    def load_printers(self) -> None:
        printers = self.database.get_printers()

        self.table.setRowCount(len(printers))

        for row_index, printer in enumerate(printers):
            values = [
                printer.get("id"),
                printer.get("name"),
                printer.get("brand"),
                printer.get("model"),
                printer.get("customer_name"),
                printer.get("location"),
                printer.get("ip_address"),
                printer.get("firmware"),
                printer.get("black_counter"),
                printer.get("color_counter"),
                printer.get("status"),
            ]

            for column_index, value in enumerate(values):
                item = QTableWidgetItem(
                    str(value or "")
                )

                if column_index in (8, 9):
                    item.setTextAlignment(
                        Qt.AlignmentFlag.AlignRight
                        | Qt.AlignmentFlag.AlignVCenter
                    )

                self.table.setItem(
                    row_index,
                    column_index,
                    item,
                )

        status_counts = (
            self.database.count_printers_by_status()
        )

        self.total_label.setText(
            "<b>Totale</b><br>"
            f"<span style='font-size:22px'>"
            f"{len(printers)}</span>"
        )
        self.active_label.setText(
            "<b>Attive</b><br>"
            f"<span style='font-size:22px'>"
            f"{status_counts.get('Attiva', 0)}</span>"
        )
        self.maintenance_label.setText(
            "<b>In manutenzione</b><br>"
            f"<span style='font-size:22px'>"
            f"{status_counts.get('Manutenzione', 0)}</span>"
        )
        self.unavailable_label.setText(
            "<b>Non disponibili</b><br>"
            f"<span style='font-size:22px'>"
            f"{status_counts.get('Non disponibile', 0)}</span>"
        )

    def delete_selected_printer(self) -> None:
        printer_id = self.get_selected_printer_id()

        if printer_id is None:
            QMessageBox.warning(
                self,
                "Nessuna stampante selezionata",
                "Seleziona una stampante dall’elenco.",
            )
            return

        printer = self.database.get_printer(printer_id)

        if printer is None:
            return

        printer_name = str(
            printer.get("name") or "stampante selezionata"
        )

        response = QMessageBox.question(
            self,
            "Conferma eliminazione",
            f"Vuoi eliminare «{printer_name}»?\n\n"
            "Saranno eliminati anche contatori, interventi "
            "e documenti collegati.",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
        )

        if response != QMessageBox.StandardButton.Yes:
            return

        self.database.delete_printer(printer_id)
        self.handle_printers_changed()