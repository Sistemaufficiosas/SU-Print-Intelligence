import sys

from app.core.application import Application
from app.core.main_window import MainWindow


def main() -> None:
    app = Application(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()