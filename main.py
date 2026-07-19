import sys

from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
)
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("SU Print Intelligence - Genesis Alpha 0.1")
        self.resize(1200, 700)

        label = QLabel("SU Print Intelligence\n\nGenesis Alpha 0.1")
        label.setAlignment(Qt.AlignCenter)

        label.setStyleSheet("""
            font-size:30px;
            font-family:Segoe UI;
            font-weight:bold;
        """)

        self.setCentralWidget(label)


def main():

    app = QApplication(sys.argv)

    window = MainWindow()

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
    