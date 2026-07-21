from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QVBoxLayout,
)

from app.modules.dashboard import MainWindow as DashboardWindow
from app.modules.printers import PrintersWidget
from app.services.database_service import DatabaseService


class MainWindow(DashboardWindow):
    """Finestra principale della Genesis Alpha 0.4."""

    def __init__(self) -> None:
        self.database = DatabaseService()

        super().__init__()

        self.setWindowTitle(
            "SU Print Intelligence - Genesis Alpha 0.4"
        )

        self.update_printers_kpi()

    def menu_clicked(self, menu_name: str) -> None:
        """Apre il modulo selezionato dal menu laterale."""

        if "Stampanti" in menu_name:
            self.open_printers_module()
            return

        super().menu_clicked(menu_name)

    def configure_printers(self) -> None:
        """Apre il modulo Stampanti dalla Dashboard."""

        self.open_printers_module()

    def open_printers_module(self) -> None:
        """Mostra la gestione delle stampanti."""

        dialog = QDialog(self)
        dialog.setWindowTitle(
            "Gestione Stampanti - SU Print Intelligence"
        )
        dialog.resize(1150, 700)
        dialog.setMinimumSize(900, 550)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(0, 0, 0, 0)

        printers_widget = PrintersWidget(
            database=self.database,
            parent=dialog,
        )

        layout.addWidget(printers_widget)

        dialog.exec()

        self.update_printers_kpi()
        self.menu_buttons[0].setChecked(True)

    def update_printers_kpi(self) -> None:
        """Aggiorna il numero delle stampanti attive nella Dashboard."""

        active_count = self.database.count_active_printers()

        title_labels = self.findChildren(QLabel, "kpiTitle")

        for title_label in title_labels:
            if title_label.text().strip().upper() != "STAMPANTI ATTIVE":
                continue

            card = title_label.parentWidget()

            if card is None:
                continue

            value_label = card.findChild(QLabel, "kpiValue")

            if value_label is not None:
                value_label.setText(str(active_count))

            return