from PySide6.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    """Finestra principale di SU Print Intelligence."""

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("SU Print Intelligence - Genesis Alpha 0.4")
        self.resize(1400, 850)
        self.setMinimumSize(1150, 700)