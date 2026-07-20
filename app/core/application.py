from PySide6.QtWidgets import QApplication

from app.ui.styles import APP_STYLE


class Application(QApplication):
    """Applicazione principale di SU Print Intelligence."""

    def __init__(self, argv):
        super().__init__(argv)

        self.setApplicationName("SU Print Intelligence")
        self.setStyleSheet(APP_STYLE)