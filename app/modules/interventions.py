from __future__ import annotations

from PySide6.QtCore import QDate, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QDateEdit,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QSpinBox,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from app.services.database_service import DatabaseService


class InterventionDialog(QDialog):
    """Finestra per registrare un nuovo intervento tecnico."""

    intervention_saved = Signal()

    def __init__(
        self,
        database: DatabaseService,
        printer_id: int,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.database = database
        self.printer_id = printer_id
        self.printer = self.database.get_printer(printer_id)

        self.setWindowTitle(
            "Nuovo intervento tecnico - SU Print Intelligence"
        )
        self.resize(720, 720)
        self.setMinimumSize(650, 620)

        self.create_interface()

    def create_interface(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 22, 24, 22)
        main_layout.setSpacing(16)

        printer_name = "Stampante"

        if self.printer is not None:
            printer_name = str(
                self.printer.get("name") or "Stampante"
            )

        title = QLabel("Nuovo intervento tecnico")
        title.setStyleSheet(
            "font-size: 24px; font-weight: 700; color: #172238;"
        )

        subtitle = QLabel(
            f"Macchina: {printer_name}"
        )
        subtitle.setStyleSheet(
            "font-size: 14px; color: #748094;"
        )

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        form = QFormLayout()
        form.setSpacing(13)

        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setDisplayFormat("dd/MM/yyyy")

        self.type_input = QComboBox()
        self.type_input.addItems(
            [
                "Riparazione",
                "Manutenzione ordinaria",
                "Manutenzione straordinaria",
                "Installazione",
                "Configurazione",
                "Aggiornamento firmware",
                "Sostituzione consumabili",
                "Controllo tecnico",
                "Intervento remoto",
                "Altro",
            ]
        )

        self.error_code_input = QLineEdit()
        self.error_code_input.setPlaceholderText(
            "Esempio: P-28, 9310, 3205"
        )

        self.problem_input = QTextEdit()
        self.problem_input.setPlaceholderText(
            "Descrivi il problema segnalato dal cliente..."
        )
        self.problem_input.setMaximumHeight(95)

        self.work_input = QTextEdit()
        self.work_input.setPlaceholderText(
            "Descrivi i controlli e le operazioni eseguite..."
        )
        self.work_input.setMaximumHeight(110)

        self.solution_input = QTextEdit()
        self.solution_input.setPlaceholderText(
            "Descrivi la soluzione adottata e il risultato finale..."
        )
        self.solution_input.setMaximumHeight(100)

        self.replaced_parts_input = QTextEdit()
        self.replaced_parts_input.setPlaceholderText(
            "Esempio: Developer nero DV-621, fusore, "
            "rullo presa carta, scheda madre..."
        )
        self.replaced_parts_input.setMaximumHeight(90)

        self.counter_input = QSpinBox()
        self.counter_input.setRange(0, 2_000_000_000)
        self.counter_input.setGroupSeparatorShown(True)

        if self.printer is not None:
            current_counter = int(
                self.printer.get("total_counter") or 0
            )
            self.counter_input.setValue(current_counter)

        self.technician_input = QLineEdit()
        self.technician_input.setText("Francesco Matrone")

        self.cost_input = QDoubleSpinBox()
        self.cost_input.setRange(0, 1_000_000)
        self.cost_input.setDecimals(2)
        self.cost_input.setSuffix(" €")

        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText(
            "Altre note, indicazioni per il prossimo intervento, "
            "materiale da ordinare..."
        )
        self.notes_input.setMaximumHeight(90)

        form.addRow("Data intervento", self.date_input)
        form.addRow("Tipo intervento", self.type_input)
        form.addRow("Codice errore", self.error_code_input)
        form.addRow("Problema segnalato *", self.problem_input)
        form.addRow("Lavoro eseguito", self.work_input)
        form.addRow("Soluzione", self.solution_input)
        form.addRow(
            "Ricambi e componenti sostituiti",
            self.replaced_parts_input,
        )
        form.addRow("Contatore macchina", self.counter_input)
        form.addRow("Tecnico", self.technician_input)
        form.addRow("Costo intervento", self.cost_input)
        form.addRow("Note finali", self.notes_input)

        main_layout.addLayout(form)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )

        save_button = buttons.button(
            QDialogButtonBox.StandardButton.Save
        )
        save_button.setText("Archivia intervento")

        cancel_button = buttons.button(
            QDialogButtonBox.StandardButton.Cancel
        )
        cancel_button.setText("Annulla")

        buttons.accepted.connect(self.save_intervention)
        buttons.rejected.connect(self.reject)

        main_layout.addWidget(buttons)

    def save_intervention(self) -> None:
        problem = self.problem_input.toPlainText().strip()

        if not problem:
            QMessageBox.warning(
                self,
                "Dato obbligatorio",
                "Descrivi il problema segnalato o il motivo "
                "dell’intervento.",
            )
            self.problem_input.setFocus()
            return

        work_done = self.work_input.toPlainText().strip()

        description = problem

        if work_done:
            description = (
                f"Problema segnalato:\n{problem}\n\n"
                f"Lavoro eseguito:\n{work_done}"
            )

        intervention_date = self.date_input.date().toString(
            "yyyy-MM-dd"
        )

        self.database.add_intervention(
            printer_id=self.printer_id,
            intervention_date=intervention_date,
            intervention_type=self.type_input.currentText(),
            error_code=self.error_code_input.text().strip(),
            description=description,
            solution=self.solution_input.toPlainText().strip(),
            replaced_parts=(
                self.replaced_parts_input.toPlainText().strip()
            ),
            technician=self.technician_input.text().strip(),
            counter_value=self.counter_input.value(),
            cost=self.cost_input.value(),
            notes=self.notes_input.toPlainText().strip(),
        )

        QMessageBox.information(
            self,
            "Intervento archiviato",
            "L’intervento tecnico è stato salvato "
            "nella cronologia della macchina.",
        )

        self.intervention_saved.emit()
        self.accept()