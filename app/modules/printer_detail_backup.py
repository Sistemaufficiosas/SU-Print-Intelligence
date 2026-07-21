from __future__ import annotations

from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QPushButton,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from app.services.database_service import DatabaseService


class InfoCard(QFrame):
    """Riquadro riepilogativo della scheda macchina."""

    def __init__(
        self,
        title: str,
        value: str,
        description: str = "",
    ) -> None:
        super().__init__()

        self.setObjectName("detailCard")
        self.setMinimumHeight(105)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 15, 18, 15)
        layout.setSpacing(5)

        title_label = QLabel(title)
        title_label.setObjectName("detailCardTitle")

        value_label = QLabel(value or "—")
        value_label.setObjectName("detailCardValue")
        value_label.setWordWrap(True)

        description_label = QLabel(description)
        description_label.setObjectName("detailCardDescription")
        description_label.setWordWrap(True)

        layout.addWidget(title_label)
        layout.addWidget(value_label)

        if description:
            layout.addWidget(description_label)

        layout.addStretch()


class PrinterDetailDialog(QDialog):
    """Cartella tecnica completa di una stampante."""

    def __init__(
        self,
        database: DatabaseService,
        printer_id: int,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.database = database
        self.printer_id = printer_id
        self.printer: dict[str, Any] | None = (
            self.database.get_printer(printer_id)
        )

        self.setWindowTitle(
            "Cartella tecnica - SU Print Intelligence"
        )
        self.resize(1180, 760)
        self.setMinimumSize(950, 650)

        self.create_interface()
        self.apply_style()

    def create_interface(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(26, 22, 26, 22)
        main_layout.setSpacing(18)

        if self.printer is None:
            error_label = QLabel(
                "La stampante richiesta non è stata trovata."
            )
            error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            main_layout.addWidget(error_label)
            return

        main_layout.addLayout(self.create_header())

        tabs = QTabWidget()
        tabs.setObjectName("detailTabs")

        tabs.addTab(
            self.create_overview_tab(),
            "Panoramica",
        )
        tabs.addTab(
            self.create_counters_tab(),
            "Contatori",
        )
        tabs.addTab(
            self.create_consumables_tab(),
            "Consumabili",
        )
        tabs.addTab(
            self.create_interventions_tab(),
            "Interventi",
        )
        tabs.addTab(
            self.create_documents_tab(),
            "Documenti",
        )
        tabs.addTab(
            self.create_knowledge_tab(),
            "Conoscenza tecnica",
        )

        main_layout.addWidget(tabs, 1)

        close_layout = QHBoxLayout()
        close_layout.addStretch()

        close_button = QPushButton("Chiudi")
        close_button.setObjectName("secondaryButton")
        close_button.clicked.connect(self.accept)

        close_layout.addWidget(close_button)
        main_layout.addLayout(close_layout)

    def create_header(self) -> QHBoxLayout:
        layout = QHBoxLayout()

        title_layout = QVBoxLayout()
        title_layout.setSpacing(3)

        printer_name = str(
            self.printer.get("name") or "Stampante"
        )
        brand = str(self.printer.get("brand") or "")
        model = str(self.printer.get("model") or "")

        title = QLabel(printer_name)
        title.setObjectName("detailTitle")

        subtitle_text = " ".join(
            value for value in (brand, model) if value
        )

        subtitle = QLabel(
            subtitle_text or "Scheda tecnica della macchina"
        )
        subtitle.setObjectName("detailSubtitle")

        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)

        status = QLabel(
            str(self.printer.get("status") or "Non definito")
        )
        status.setObjectName("detailStatus")
        status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status.setMinimumWidth(130)

        layout.addLayout(title_layout)
        layout.addStretch()
        layout.addWidget(status)

        return layout

    def create_overview_tab(self) -> QWidget:
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(18, 20, 18, 20)
        layout.setSpacing(16)

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(12)

        cards_layout.addWidget(
            InfoCard(
                "CLIENTE",
                str(
                    self.printer.get("customer_name")
                    or "Non associato"
                ),
                str(
                    self.printer.get("customer_location")
                    or ""
                ),
            )
        )

        cards_layout.addWidget(
            InfoCard(
                "INDIRIZZO IP",
                str(
                    self.printer.get("ip_address")
                    or "Non configurato"
                ),
                str(
                    self.printer.get("mac_address")
                    or ""
                ),
            )
        )

        cards_layout.addWidget(
            InfoCard(
                "FIRMWARE",
                str(
                    self.printer.get("firmware")
                    or "Non indicato"
                ),
                str(
                    self.printer.get("driver")
                    or ""
                ),
            )
        )

        cards_layout.addWidget(
            InfoCard(
                "CONTATORE TOTALE",
                self.format_number(
                    self.printer.get("total_counter")
                ),
                "Copie registrate",
            )
        )

        layout.addLayout(cards_layout)

        data_panel = QFrame()
        data_panel.setObjectName("detailPanel")

        form = QFormLayout(data_panel)
        form.setContentsMargins(22, 20, 22, 20)
        form.setSpacing(12)

        form.addRow(
            "Marca:",
            self.value_label("brand"),
        )
        form.addRow(
            "Modello:",
            self.value_label("model"),
        )
        form.addRow(
            "Numero di serie:",
            self.value_label("serial_number"),
        )
        form.addRow(
            "Tecnologia:",
            self.value_label("technology"),
        )
        form.addRow(
            "Posizione interna:",
            self.value_label("location"),
        )
        form.addRow(
            "Data installazione:",
            self.value_label("installation_date"),
        )
        form.addRow(
            "Tipo contratto:",
            self.value_label("contract_type"),
        )
        form.addRow(
            "Numero contratto:",
            self.value_label("contract_number"),
        )
        form.addRow(
            "Ultima manutenzione:",
            self.value_label("last_maintenance"),
        )
        form.addRow(
            "Prossima manutenzione:",
            self.value_label("next_maintenance"),
        )

        layout.addWidget(data_panel)
        layout.addStretch()

        return tab

    def create_counters_tab(self) -> QWidget:
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(18, 20, 18, 20)
        layout.setSpacing(16)

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(12)

        cards_layout.addWidget(
            InfoCard(
                "BIANCO E NERO",
                self.format_number(
                    self.printer.get("black_counter")
                ),
            )
        )
        cards_layout.addWidget(
            InfoCard(
                "COLORE",
                self.format_number(
                    self.printer.get("color_counter")
                ),
            )
        )
        cards_layout.addWidget(
            InfoCard(
                "TOTALE",
                self.format_number(
                    self.printer.get("total_counter")
                ),
            )
        )

        layout.addLayout(cards_layout)

        title = QLabel("Storico letture")
        title.setObjectName("sectionTitle")
        layout.addWidget(title)

        history = self.database.get_counter_history(
            self.printer_id
        )

        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(
            [
                "Data",
                "B/N",
                "Colore",
                "Totale",
                "Note",
            ]
        )
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        header = table.horizontalHeader()
        header.setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        header.setSectionResizeMode(
            4,
            QHeaderView.ResizeMode.Stretch,
        )

        table.setRowCount(len(history))

        for row_index, reading in enumerate(history):
            values = [
                reading.get("counter_date"),
                reading.get("black_counter"),
                reading.get("color_counter"),
                reading.get("total_counter"),
                reading.get("notes"),
            ]

            for column_index, value in enumerate(values):
                table.setItem(
                    row_index,
                    column_index,
                    QTableWidgetItem(str(value or "")),
                )

        layout.addWidget(table, 1)

        return tab

    def create_consumables_tab(self) -> QWidget:
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(18, 20, 18, 20)
        layout.setSpacing(14)

        title = QLabel("Consumabili e componenti")
        title.setObjectName("sectionTitle")

        description = QLabel(
            "Questa sezione ospiterà toner, drum, developer, "
            "fusore, cinghia di trasferimento, rulli e altri "
            "componenti della macchina."
        )
        description.setWordWrap(True)
        description.setObjectName("placeholderText")

        components = QLabel(
            "• Toner K, C, M, Y\n"
            "• Drum K, C, M, Y\n"
            "• Developer K, C, M, Y\n"
            "• Fusore\n"
            "• Transfer Belt\n"
            "• Rulli di alimentazione\n"
            "• Componenti ADF"
        )
        components.setObjectName("componentList")

        layout.addWidget(title)
        layout.addWidget(description)
        layout.addSpacing(10)
        layout.addWidget(components)
        layout.addStretch()

        return tab

    def create_interventions_tab(self) -> QWidget:
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(18, 20, 18, 20)
        layout.setSpacing(14)

        title = QLabel("Storico interventi tecnici")
        title.setObjectName("sectionTitle")
        layout.addWidget(title)

        interventions = self.database.get_interventions(
            self.printer_id
        )

        table = QTableWidget()
        table.setColumnCount(8)
        table.setHorizontalHeaderLabels(
            [
                "Data",
                "Tipo",
                "Errore",
                "Descrizione",
                "Soluzione",
                "Ricambi",
                "Tecnico",
                "Costo",
            ]
        )
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        header = table.horizontalHeader()
        header.setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        header.setSectionResizeMode(
            3,
            QHeaderView.ResizeMode.Stretch,
        )
        header.setSectionResizeMode(
            4,
            QHeaderView.ResizeMode.Stretch,
        )

        table.setRowCount(len(interventions))

        for row_index, intervention in enumerate(
            interventions
        ):
            values = [
                intervention.get("intervention_date"),
                intervention.get("intervention_type"),
                intervention.get("error_code"),
                intervention.get("description"),
                intervention.get("solution"),
                intervention.get("replaced_parts"),
                intervention.get("technician"),
                intervention.get("cost"),
            ]

            for column_index, value in enumerate(values):
                table.setItem(
                    row_index,
                    column_index,
                    QTableWidgetItem(str(value or "")),
                )

        layout.addWidget(table, 1)

        return tab

    def create_documents_tab(self) -> QWidget:
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(18, 20, 18, 20)
        layout.setSpacing(14)

        title = QLabel("Documentazione tecnica")
        title.setObjectName("sectionTitle")

        description = QLabel(
            "In questa sezione collegheremo manuali tecnici, "
            "Part List, firmware, fotografie, video e backup "
            "delle impostazioni."
        )
        description.setWordWrap(True)
        description.setObjectName("placeholderText")

        document_types = QLabel(
            "📄 Manuale tecnico\n"
            "📄 Part List\n"
            "💾 Firmware\n"
            "💾 Backup configurazione\n"
            "📷 Fotografie\n"
            "🎥 Video tecnici"
        )
        document_types.setObjectName("componentList")

        layout.addWidget(title)
        layout.addWidget(description)
        layout.addSpacing(10)
        layout.addWidget(document_types)
        layout.addStretch()

        return tab

    def create_knowledge_tab(self) -> QWidget:
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(18, 20, 18, 20)
        layout.setSpacing(14)

        notes_title = QLabel("Note generali")
        notes_title.setObjectName("sectionTitle")

        notes = QTextEdit()
        notes.setReadOnly(True)
        notes.setPlainText(
            str(self.printer.get("notes") or "")
        )

        knowledge_title = QLabel("Conoscenza tecnica")
        knowledge_title.setObjectName("sectionTitle")

        knowledge = QTextEdit()
        knowledge.setReadOnly(True)
        knowledge.setPlainText(
            str(
                self.printer.get("technical_knowledge")
                or ""
            )
        )

        layout.addWidget(notes_title)
        layout.addWidget(notes)
        layout.addWidget(knowledge_title)
        layout.addWidget(knowledge)

        return tab

    def value_label(self, field_name: str) -> QLabel:
        value = str(
            self.printer.get(field_name) or "—"
        )

        label = QLabel(value)
        label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        label.setWordWrap(True)

        return label

    @staticmethod
    def format_number(value: Any) -> str:
        try:
            number = int(value or 0)
        except (TypeError, ValueError):
            number = 0

        return f"{number:,}".replace(",", ".")

    def apply_style(self) -> None:
        self.setStyleSheet(
            """
            #detailTitle {
                color: #172238;
                font-size: 28px;
                font-weight: 700;
            }

            #detailSubtitle {
                color: #748094;
                font-size: 14px;
            }

            #detailStatus {
                background-color: #e4f6ec;
                color: #168449;
                border-radius: 8px;
                padding: 10px 14px;
                font-weight: 700;
            }

            #detailCard {
                background-color: white;
                border: 1px solid #e1e6ee;
                border-radius: 9px;
            }

            #detailCardTitle {
                color: #7b8798;
                font-size: 11px;
                font-weight: 700;
            }

            #detailCardValue {
                color: #18243a;
                font-size: 20px;
                font-weight: 700;
            }

            #detailCardDescription {
                color: #8b96a6;
                font-size: 11px;
            }

            #detailPanel {
                background-color: white;
                border: 1px solid #e1e6ee;
                border-radius: 9px;
            }

            #sectionTitle {
                color: #18243a;
                font-size: 18px;
                font-weight: 700;
            }

            #placeholderText {
                color: #687589;
                font-size: 14px;
            }

            #componentList {
                background-color: #f7f9fc;
                border: 1px solid #e1e6ee;
                border-radius: 8px;
                color: #344258;
                padding: 18px;
                font-size: 14px;
            }

            QTabWidget::pane {
                background-color: #f4f6f9;
                border: 1px solid #dfe5ed;
                border-radius: 7px;
            }

            QTabBar::tab {
                background-color: #e9edf3;
                color: #5c687b;
                padding: 10px 16px;
                margin-right: 2px;
            }

            QTabBar::tab:selected {
                background-color: #2f7de1;
                color: white;
                font-weight: 600;
            }

            QTableWidget {
                background-color: white;
                alternate-background-color: #f8fafc;
                border: 1px solid #e1e6ee;
                gridline-color: #edf0f4;
            }

            QHeaderView::section {
                background-color: #edf2f8;
                color: #536176;
                border: none;
                border-bottom: 1px solid #d9e0e9;
                padding: 9px;
                font-weight: 600;
            }
            """
        )