import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)


class KpiCard(QFrame):
    """Scheda utilizzata per mostrare un indicatore principale."""

    def __init__(
        self,
        title: str,
        value: str,
        description: str,
        accent: str = "#2f7de1",
    ) -> None:
        super().__init__()

        self.setObjectName("kpiCard")
        self.setMinimumHeight(145)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        accent_bar = QFrame()
        accent_bar.setFixedWidth(5)
        accent_bar.setStyleSheet(
            f"""
            background-color: {accent};
            border-top-left-radius: 10px;
            border-bottom-left-radius: 10px;
            """
        )

        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(20, 17, 20, 17)
        content_layout.setSpacing(6)

        title_label = QLabel(title)
        title_label.setObjectName("kpiTitle")

        value_label = QLabel(value)
        value_label.setObjectName("kpiValue")

        description_label = QLabel(description)
        description_label.setObjectName("kpiDescription")
        description_label.setWordWrap(True)

        content_layout.addWidget(title_label)
        content_layout.addWidget(value_label)
        content_layout.addWidget(description_label)
        content_layout.addStretch()

        main_layout.addWidget(accent_bar)
        main_layout.addLayout(content_layout, 1)


class ActivityItem(QFrame):
    """Riga della cronologia operativa."""

    def __init__(
        self,
        time_text: str,
        title: str,
        description: str,
        symbol: str = "✓",
    ) -> None:
        super().__init__()

        self.setObjectName("activityItem")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 9, 10, 9)
        layout.setSpacing(12)

        icon = QLabel(symbol)
        icon.setObjectName("activityIcon")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon.setFixedSize(30, 30)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)

        title_label = QLabel(title)
        title_label.setObjectName("activityTitle")

        description_label = QLabel(description)
        description_label.setObjectName("activityDescription")
        description_label.setWordWrap(True)

        time_label = QLabel(time_text)
        time_label.setObjectName("activityTime")
        time_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop
        )
        time_label.setFixedWidth(48)

        text_layout.addWidget(title_label)
        text_layout.addWidget(description_label)

        layout.addWidget(icon)
        layout.addLayout(text_layout, 1)
        layout.addWidget(time_label)


class PrinterItem(QFrame):
    """Stato sintetico di una stampante."""

    def __init__(
        self,
        printer_name: str,
        location: str,
        status: str,
        percentage: int,
    ) -> None:
        super().__init__()

        self.setObjectName("printerItem")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(7)

        top_layout = QHBoxLayout()

        name_label = QLabel(printer_name)
        name_label.setObjectName("printerName")

        status_label = QLabel(status)
        status_label.setObjectName("printerStatus")

        top_layout.addWidget(name_label)
        top_layout.addStretch()
        top_layout.addWidget(status_label)

        location_label = QLabel(location)
        location_label.setObjectName("printerLocation")

        progress = QProgressBar()
        progress.setRange(0, 100)
        progress.setValue(percentage)
        progress.setTextVisible(True)
        progress.setFormat(f"Disponibilità consumabili: {percentage}%")
        progress.setFixedHeight(18)

        layout.addLayout(top_layout)
        layout.addWidget(location_label)
        layout.addWidget(progress)


class AgendaItem(QFrame):
    """Appuntamento sintetico della giornata."""

    def __init__(
        self,
        time_text: str,
        title: str,
        description: str,
    ) -> None:
        super().__init__()

        self.setObjectName("agendaItem")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 9, 10, 9)
        layout.setSpacing(12)

        time_label = QLabel(time_text)
        time_label.setObjectName("agendaTime")
        time_label.setFixedWidth(48)
        time_label.setAlignment(Qt.AlignmentFlag.AlignTop)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)

        title_label = QLabel(title)
        title_label.setObjectName("agendaTitle")

        description_label = QLabel(description)
        description_label.setObjectName("agendaDescription")
        description_label.setWordWrap(True)

        text_layout.addWidget(title_label)
        text_layout.addWidget(description_label)

        layout.addWidget(time_label)
        layout.addLayout(text_layout, 1)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("SU Print Intelligence - Genesis Alpha 0.4")
        self.resize(1400, 850)
        self.setMinimumSize(1150, 700)

        self.menu_buttons: list[QPushButton] = []
        self.menu_group = QButtonGroup(self)
        self.menu_group.setExclusive(True)

        self.create_interface()
        self.apply_style()

    def create_interface(self) -> None:
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        main_layout.addWidget(self.create_sidebar())
        main_layout.addWidget(self.create_content(), 1)

    def create_sidebar(self) -> QFrame:
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(245)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(18, 24, 18, 20)
        layout.setSpacing(7)

        logo = QLabel("SU")
        logo.setObjectName("logo")

        software_name = QLabel("PRINT INTELLIGENCE")
        software_name.setObjectName("softwareName")

        version = QLabel("Genesis Alpha 0.4")
        version.setObjectName("versionLabel")

        layout.addWidget(logo)
        layout.addWidget(software_name)
        layout.addWidget(version)
        layout.addSpacing(25)

        menu_items = [
            "⌂   Centro Operativo",
            "▣   Preventivi",
            "◫   Lavori",
            "♙   Clienti",
            "▤   Stampanti",
            "▧   Carta e materiali",
            "◉   Inchiostri",
            "▦   Agenda",
            "⇄   Importa / Esporta",
            "⚙   Impostazioni",
        ]

        for index, text in enumerate(menu_items):
            button = QPushButton(text)
            button.setObjectName("menuButton")
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setCheckable(True)

            self.menu_group.addButton(button)
            self.menu_buttons.append(button)

            if index == 0:
                button.setChecked(True)

            button.clicked.connect(
                lambda checked=False, name=text: self.menu_clicked(name)
            )

            layout.addWidget(button)

        layout.addStretch()

        user_box = QFrame()
        user_box.setObjectName("userBox")

        user_layout = QVBoxLayout(user_box)
        user_layout.setContentsMargins(12, 10, 12, 10)

        user_name = QLabel("Francesco Matrone")
        user_name.setObjectName("userName")

        user_role = QLabel("Amministratore")
        user_role.setObjectName("userRole")

        user_layout.addWidget(user_name)
        user_layout.addWidget(user_role)

        layout.addWidget(user_box)

        return sidebar

    def create_content(self) -> QWidget:
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setObjectName("mainScrollArea")

        content = QWidget()
        content.setObjectName("contentArea")

        layout = QVBoxLayout(content)
        layout.setContentsMargins(32, 25, 32, 24)
        layout.setSpacing(20)

        layout.addLayout(self.create_top_bar())
        layout.addLayout(self.create_kpi_area())
        layout.addLayout(self.create_dashboard_area(), 1)

        footer = QLabel(
            "SU Print Intelligence  •  Genesis Alpha 0.4  •  Centro Operativo"
        )
        footer.setObjectName("footer")
        footer.setAlignment(Qt.AlignmentFlag.AlignRight)

        layout.addWidget(footer)

        scroll_area.setWidget(content)
        return scroll_area

    def create_top_bar(self) -> QHBoxLayout:
        top_bar = QHBoxLayout()

        title_box = QVBoxLayout()
        title_box.setSpacing(2)

        self.page_title = QLabel("Centro Operativo")
        self.page_title.setObjectName("pageTitle")

        self.page_subtitle = QLabel(
            "Controllo generale di lavori, costi, stampanti e attività"
        )
        self.page_subtitle.setObjectName("pageSubtitle")

        title_box.addWidget(self.page_title)
        title_box.addWidget(self.page_subtitle)

        status_box = QFrame()
        status_box.setObjectName("statusBox")

        status_layout = QHBoxLayout(status_box)
        status_layout.setContentsMargins(14, 8, 14, 8)

        status = QLabel("●  Sistema operativo")
        status.setObjectName("systemStatus")

        notification_button = QPushButton("🔔  2")
        notification_button.setObjectName("notificationButton")
        notification_button.setCursor(Qt.CursorShape.PointingHandCursor)
        notification_button.clicked.connect(self.show_notifications)

        status_layout.addWidget(status)
        status_layout.addWidget(notification_button)

        top_bar.addLayout(title_box)
        top_bar.addStretch()
        top_bar.addWidget(status_box)

        return top_bar

    def create_kpi_area(self) -> QHBoxLayout:
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(15)

        cards_layout.addWidget(
            KpiCard(
                "LAVORI ANALIZZATI",
                "0",
                "Analisi effettuate nella sessione corrente.",
                "#2f7de1",
            )
        )

        cards_layout.addWidget(
            KpiCard(
                "COSTI STIMATI",
                "€ 0,00",
                "Totale dei costi previsti dal motore.",
                "#7c5ce7",
            )
        )

        cards_layout.addWidget(
            KpiCard(
                "PRECISIONE PREVISIONE",
                "—",
                "Disponibile dopo i primi confronti reali.",
                "#e29b2d",
            )
        )

        cards_layout.addWidget(
            KpiCard(
                "STAMPANTI ATTIVE",
                "0",
                "Dispositivi configurati e disponibili.",
                "#35a56f",
            )
        )

        return cards_layout

    def create_dashboard_area(self) -> QGridLayout:
        dashboard_layout = QGridLayout()
        dashboard_layout.setSpacing(17)

        dashboard_layout.addWidget(
            self.create_activity_panel(),
            0,
            0,
            2,
            2,
        )

        dashboard_layout.addWidget(
            self.create_ai_panel(),
            0,
            2,
            1,
            1,
        )

        dashboard_layout.addWidget(
            self.create_printers_panel(),
            2,
            0,
            1,
            2,
        )

        dashboard_layout.addWidget(
            self.create_agenda_panel(),
            1,
            2,
            2,
            1,
        )

        dashboard_layout.setColumnStretch(0, 1)
        dashboard_layout.setColumnStretch(1, 1)
        dashboard_layout.setColumnStretch(2, 1)

        dashboard_layout.setRowStretch(0, 1)
        dashboard_layout.setRowStretch(1, 1)
        dashboard_layout.setRowStretch(2, 1)

        return dashboard_layout

    def create_activity_panel(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("panel")

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(22, 19, 22, 19)
        layout.setSpacing(8)

        header = QHBoxLayout()

        title = QLabel("Attività recenti")
        title.setObjectName("panelTitle")

        live_label = QLabel("● AGGIORNAMENTO ATTIVO")
        live_label.setObjectName("liveLabel")

        header.addWidget(title)
        header.addStretch()
        header.addWidget(live_label)

        layout.addLayout(header)

        layout.addWidget(
            ActivityItem(
                "09:35",
                "Centro Operativo avviato",
                "SU Print Intelligence è pronto per iniziare il lavoro.",
                "✓",
            )
        )

        layout.addWidget(
            ActivityItem(
                "09:36",
                "Motore intelligente in preparazione",
                "In attesa dei primi dati reali per la calibrazione.",
                "AI",
            )
        )

        layout.addWidget(
            ActivityItem(
                "09:37",
                "Archivio controllato",
                "La struttura del progetto risulta correttamente inizializzata.",
                "✓",
            )
        )

        layout.addStretch()

        return panel

    def create_ai_panel(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("panel")

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(22, 19, 22, 19)
        layout.setSpacing(12)

        title = QLabel("Motore intelligente")
        title.setObjectName("panelTitle")

        state = QLabel("STATO: IN PREPARAZIONE")
        state.setObjectName("aiState")

        description = QLabel(
            "Il motore confronterà consumi previsti e dati reali per "
            "migliorare progressivamente la precisione dei preventivi."
        )
        description.setObjectName("panelText")
        description.setWordWrap(True)

        learning_label = QLabel("Apprendimento disponibile")
        learning_label.setObjectName("smallLabel")

        learning_progress = QProgressBar()
        learning_progress.setRange(0, 100)
        learning_progress.setValue(0)
        learning_progress.setFormat("0%")
        learning_progress.setFixedHeight(20)

        start_button = QPushButton("＋  Nuova analisi")
        start_button.setObjectName("primaryButton")
        start_button.setCursor(Qt.CursorShape.PointingHandCursor)
        start_button.clicked.connect(self.start_new_analysis)

        layout.addWidget(title)
        layout.addWidget(state)
        layout.addWidget(description)
        layout.addWidget(learning_label)
        layout.addWidget(learning_progress)
        layout.addStretch()
        layout.addWidget(start_button)

        return panel

    def create_printers_panel(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("panel")

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(22, 19, 22, 19)
        layout.setSpacing(9)

        header = QHBoxLayout()

        title = QLabel("Stato stampanti")
        title.setObjectName("panelTitle")

        configure_button = QPushButton("Configura dispositivi")
        configure_button.setObjectName("textButton")
        configure_button.setCursor(Qt.CursorShape.PointingHandCursor)
        configure_button.clicked.connect(self.configure_printers)

        header.addWidget(title)
        header.addStretch()
        header.addWidget(configure_button)

        layout.addLayout(header)

        layout.addWidget(
            PrinterItem(
                "Nessuna stampante configurata",
                "Apri il modulo Stampanti per inserire il primo dispositivo.",
                "DA CONFIGURARE",
                0,
            )
        )

        return panel

    def create_agenda_panel(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("panel")

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(22, 19, 22, 19)
        layout.setSpacing(9)

        header = QHBoxLayout()

        title = QLabel("Agenda di oggi")
        title.setObjectName("panelTitle")

        count_label = QLabel("2 attività")
        count_label.setObjectName("countLabel")

        header.addWidget(title)
        header.addStretch()
        header.addWidget(count_label)

        layout.addLayout(header)

        layout.addWidget(
            AgendaItem(
                "10:00",
                "Sviluppo Dashboard",
                "Completamento della Genesis Alpha 0.4.",
            )
        )

        layout.addWidget(
            AgendaItem(
                "15:30",
                "Controllo progetto",
                "Verifica del funzionamento e salvataggio su GitHub.",
            )
        )

        layout.addStretch()

        agenda_button = QPushButton("Apri agenda completa")
        agenda_button.setObjectName("secondaryButton")
        agenda_button.setCursor(Qt.CursorShape.PointingHandCursor)
        agenda_button.clicked.connect(self.open_agenda)

        layout.addWidget(agenda_button)

        return panel

    def menu_clicked(self, menu_name: str) -> None:
        clean_name = menu_name.strip()

        if "Centro Operativo" in clean_name:
            self.page_title.setText("Centro Operativo")
            self.page_subtitle.setText(
                "Controllo generale di lavori, costi, stampanti e attività"
            )
            return

        section_name = clean_name[3:].strip()

        QMessageBox.information(
            self,
            section_name,
            f"Il modulo «{section_name}» sarà sviluppato "
            "nelle prossime fasi del progetto.",
        )

        self.menu_buttons[0].setChecked(True)

    def start_new_analysis(self) -> None:
        QMessageBox.information(
            self,
            "Nuova analisi",
            "Il pulsante funziona correttamente.\n\n"
            "Nel prossimo sviluppo aprirà il modulo di analisi preventiva "
            "di immagini e documenti.",
        )

    def show_notifications(self) -> None:
        QMessageBox.information(
            self,
            "Notifiche operative",
            "1. Configurare almeno una stampante.\n\n"
            "2. Importare i primi dati reali per avviare "
            "l'apprendimento del motore.",
        )

    def configure_printers(self) -> None:
        QMessageBox.information(
            self,
            "Configurazione stampanti",
            "Il modulo Stampanti sarà il prossimo componente operativo "
            "collegato alla Dashboard.",
        )

    def open_agenda(self) -> None:
        QMessageBox.information(
            self,
            "Agenda",
            "Il collegamento funziona.\n\n"
            "Successivamente verrà collegato all'Agenda completa "
            "e alla sincronizzazione Nextcloud.",
        )

    def apply_style(self) -> None:
        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #f4f6f9;
            }

            QWidget {
                font-family: "Segoe UI";
                font-size: 14px;
            }

            QScrollArea {
                border: none;
                background-color: #f4f6f9;
            }

            QScrollBar:vertical {
                background: #edf0f5;
                width: 10px;
                margin: 0;
            }

            QScrollBar::handle:vertical {
                background: #b6c0ce;
                border-radius: 5px;
                min-height: 40px;
            }

            #sidebar {
                background-color: #182235;
                border: none;
            }

            #logo {
                color: white;
                font-size: 31px;
                font-weight: 800;
            }

            #softwareName {
                color: #dce7f6;
                font-size: 15px;
                font-weight: 700;
                letter-spacing: 1px;
            }

            #versionLabel {
                color: #8293aa;
                font-size: 12px;
            }

            #menuButton {
                background-color: transparent;
                color: #c7d1df;
                border: none;
                border-radius: 7px;
                text-align: left;
                padding: 11px 13px;
                font-size: 14px;
            }

            #menuButton:hover {
                background-color: #24344e;
                color: white;
            }

            #menuButton:checked {
                background-color: #2f7de1;
                color: white;
                font-weight: 600;
            }

            #userBox {
                background-color: #202e45;
                border-radius: 8px;
            }

            #userName {
                color: white;
                font-weight: 600;
            }

            #userRole {
                color: #8fa1b9;
                font-size: 12px;
            }

            #contentArea {
                background-color: #f4f6f9;
            }

            #pageTitle {
                color: #172238;
                font-size: 28px;
                font-weight: 700;
            }

            #pageSubtitle {
                color: #748094;
                font-size: 14px;
            }

            #statusBox {
                background-color: white;
                border: 1px solid #e1e6ee;
                border-radius: 10px;
            }

            #systemStatus {
                color: #168449;
                font-weight: 600;
            }

            #notificationButton {
                background-color: #eef4fc;
                color: #2767b7;
                border: none;
                border-radius: 7px;
                padding: 7px 11px;
                font-weight: 600;
            }

            #notificationButton:hover {
                background-color: #ddeafb;
            }

            #kpiCard {
                background-color: white;
                border: 1px solid #e1e6ee;
                border-radius: 10px;
            }

            #kpiCard:hover {
                border: 1px solid #b7c9e3;
            }

            #kpiTitle {
                color: #778397;
                font-size: 12px;
                font-weight: 700;
            }

            #kpiValue {
                color: #162239;
                font-size: 27px;
                font-weight: 700;
            }

            #kpiDescription {
                color: #8a95a6;
                font-size: 12px;
            }

            #panel {
                background-color: white;
                border: 1px solid #e1e6ee;
                border-radius: 10px;
            }

            #panelTitle {
                color: #18243a;
                font-size: 18px;
                font-weight: 700;
            }

            #liveLabel {
                color: #209760;
                font-size: 10px;
                font-weight: 700;
            }

            #activityItem {
                background-color: #f8fafc;
                border-radius: 7px;
            }

            #activityIcon {
                background-color: #e5f2ff;
                color: #2773cf;
                border-radius: 15px;
                font-size: 11px;
                font-weight: 700;
            }

            #activityTitle {
                color: #26344a;
                font-weight: 600;
            }

            #activityDescription {
                color: #7d899a;
                font-size: 12px;
            }

            #activityTime {
                color: #9aa5b3;
                font-size: 11px;
            }

            #panelText {
                color: #657185;
            }

            #smallLabel {
                color: #778397;
                font-size: 12px;
                font-weight: 600;
            }

            #aiState {
                background-color: #fff3d8;
                color: #9b6a00;
                border-radius: 6px;
                padding: 8px 10px;
                font-size: 12px;
                font-weight: 700;
            }

            QProgressBar {
                background-color: #e8edf4;
                border: none;
                border-radius: 8px;
                color: #4e5b6d;
                font-size: 10px;
                text-align: center;
            }

            QProgressBar::chunk {
                background-color: #2f7de1;
                border-radius: 8px;
            }

            #primaryButton {
                background-color: #2f7de1;
                color: white;
                border: none;
                border-radius: 7px;
                padding: 12px 18px;
                font-weight: 600;
            }

            #primaryButton:hover {
                background-color: #216bc9;
            }

            #secondaryButton {
                background-color: #edf4fd;
                color: #276bc2;
                border: 1px solid #d4e3f7;
                border-radius: 7px;
                padding: 10px 15px;
                font-weight: 600;
            }

            #secondaryButton:hover {
                background-color: #deebfb;
            }

            #textButton {
                background-color: transparent;
                color: #2f75cc;
                border: none;
                font-size: 12px;
                font-weight: 600;
            }

            #textButton:hover {
                text-decoration: underline;
            }

            #printerItem {
                background-color: #f8fafc;
                border-radius: 7px;
            }

            #printerName {
                color: #26344a;
                font-weight: 600;
            }

            #printerStatus {
                color: #a46f00;
                background-color: #fff1d2;
                border-radius: 5px;
                padding: 4px 7px;
                font-size: 10px;
                font-weight: 700;
            }

            #printerLocation {
                color: #7d899a;
                font-size: 12px;
            }

            #agendaItem {
                background-color: #f8fafc;
                border-radius: 7px;
            }

            #agendaTime {
                color: #2f75cc;
                font-weight: 700;
            }

            #agendaTitle {
                color: #26344a;
                font-weight: 600;
            }

            #agendaDescription {
                color: #7d899a;
                font-size: 12px;
            }

            #countLabel {
                background-color: #edf4fd;
                color: #2f75cc;
                border-radius: 6px;
                padding: 5px 8px;
                font-size: 11px;
                font-weight: 600;
            }

            #footer {
                color: #9aa4b3;
                font-size: 11px;
            }
            """
        )


def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationName("SU Print Intelligence")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()