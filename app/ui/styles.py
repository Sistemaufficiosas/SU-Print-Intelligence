APP_STYLE = """
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