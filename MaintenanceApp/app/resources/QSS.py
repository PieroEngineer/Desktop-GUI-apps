QSS = """
/* =========================
   Modern Light Theme (PyQt6)
   Palette: #0099FF (primary), #003087 (secondary), #FE5000 (accent)
   ========================= */

/* ---- Base / Typography ---- */
* {
    color: #0B1220;                 /* text */
    font-size: 13px;
}
QWidget {
    background: #FFFFFF;            /* app background */
    selection-background-color: #0099FF;
    selection-color: #ffffff;
}

/* ---- Panels / Cards ---- */
QFrame, QGroupBox, QStackedWidget, QTabWidget {
    background: #F7F9FC;
    border: 1px solid #E3E8F2;
    border-radius: 10px;
}

/* GroupBox header label */
QGroupBox {
    margin-top: 18px;
    padding: 0px;   /*12px*/
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    color: #5B667A;
    padding: 0 0px; /*0 6px*/
}

/* ---- Labels ---- */
QLabel {
    color: #0B1220;
}
QLabel#caption, QLabel#muted {
    color: #5B667A;
}
QLabel#driver_ads {
    color: green;
}

/* ---- Buttons ---- */
QPushButton {
    background: #EFF3F8;
    color: #0B1220;
    border: 1px solid #D6DEEA;
    border-radius: 10px;
    padding: 4px 6px;  /*8px 12px*/
}
QPushButton:hover {
    border-color: #0099FF;
}
QPushButton:pressed {
    background: #E6F2FF;
}
QPushButton:disabled {
    color: #8A93A3;
    background: #F2F4F8;
    border-color: #E3E8F2;
}

/* Primary CTA (set objectName 'primary') */
QPushButton#primary {
    background: #0099FF;
    color: #ffffff;
    border: 1px solid #0099FF;
}
QPushButton#primary:hover {
    background: #0089E6;           /* subtle darken on hover */
    border-color: #0089E6;
}
QPushButton#primary:pressed {
    background: #003087;           /* secondary on press */
    border-color: #003087;
}

/* Accent button (objectName 'accent') */
QPushButton#accent {
    background: #FE5000;
    color: #ffffff;
    border: 1px solid #FE5000;
}
QPushButton#accent:hover {
    background: #e44700;
    border-color: #e44700;
}
QPushButton#accent:pressed {
    background: #c83d00;
    border-color: #c83d00;
}

/* ---- Inputs (PlainText) ---- */
QPlainTextEdit {
    background: #EFF3F8;
    color: #0B1220;
    border: 1px solid #D6DEEA;
    border-radius: 10px;
    padding: 4px;   /*8px*/
    selection-background-color: #DCEEFF;   /* light selection inside input */
    selection-color: #0B1220;
}
QPlainTextEdit:focus {
    border-color: #0099FF;
}

/* ---- Tabs ---- */
QTabWidget::pane {
    border: 1px solid #E3E8F2;
    border-radius: 10px;
    top: 8px;                       /* little gap between tabs and pane */
    background: #F7F9FC;
}
QTabBar::tab {
    background: transparent;
    color: #5B667A;
    border: none;
    padding: 4px 7px;  /*8px 14px*/
    margin-right: 6px;
    border-bottom: 2px solid transparent;
}
QTabBar::tab:selected {
    color: #0B1220;
    border-bottom: 2px solid #0099FF;  /* underline style */
}
QTabBar::tab:hover {
    color: #0B1220;
}
QTabBar::tab:!selected {
    background: transparent;
}

/* ---- Table (QTableWidget) ---- */
QTableView, QTableWidget {
    background: #FFFFFF;
    border: 1px solid #E3E8F2;
    border-radius: 10px;
    gridline-color: #D6DEEA;
    selection-background-color: #E6F2FF;   /* primary tint */
    selection-color: #0B1220;
    alternate-background-color: #FAFCFF;
}
QHeaderView::section {
    background: #EFF3F8;
    color: #5B667A;
    padding: 3px 5px; /*6px 10px*/
    border: 0;
    border-right: 1px solid #E3E8F2;
}
QHeaderView::section:horizontal:first {
    border-top-left-radius: 8px;
}
QHeaderView::section:horizontal:last {
    border-top-right-radius: 8px;
}
QTableCornerButton::section {
    background: #EFF3F8;
    border: 0;
    border-right: 1px solid #E3E8F2;
    border-bottom: 1px solid #E3E8F2;
}

/* ---- Progress Bar ---- */
QProgressBar {
    background: #EFF3F8;
    color: #0B1220;
    border: 1px solid #D6DEEA;
    border-radius: 10px;
    text-align: center;
    padding: 1px;   /*2px*/
}
QProgressBar::chunk {
    border-radius: 10px;
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #0099FF, stop:1 #003087
    );
}

/* ---- Menus (if used) ---- */
QMenuBar {
    background: #F7F9FC;
    border-bottom: 1px solid #E3E8F2;
}
QMenuBar::item {
    padding: 3px 5px;  /*6px 10px*/
    color: #5B667A;
}
QMenuBar::item:selected { background: #EFF3F8; color: #0B1220; }
QMenu {
    background: #FFFFFF;
    border: 1px solid #E3E8F2;
    border-radius: 10px;
    padding: 3px 0;  /*6px 0*/
}
QMenu::item {
    padding: 3px 6px;  /*6px 12px*/
}
QMenu::item:selected {
    background: #E6F2FF;
}

/* ---- Slim Scrollbars (affect tables/edits) ---- */
QScrollBar:horizontal, QScrollBar:vertical {
    background: transparent;
    margin: 6px;
}
QScrollBar::handle:horizontal, QScrollBar::handle:vertical {
    background: #D6DEEA;
    border-radius: 8px;
}
QScrollBar::handle:hover {
    background: #0099FF;
}
QScrollBar::add-line, QScrollBar::sub-line {
    width: 0; height: 0; border: none; background: none;
}

/* ---- Subtle error helper (optional) ---- */
/* Add property error='true' to highlight any widget */
*[error="true"] {
    border: 1px solid #FE5000;
    background: rgba(254,80,0,0.07);
}

/* ---- Status tips / tooltips (optional polish) ---- */
QToolTip {
    background: #003087;
    color: #ffffff;
    border: 1px solid #003087;
    border-radius: 6px;
    padding: 3px 4px;   /*6px 8px*/
}

QCheckBox {
    spacing: 5px; /* Space between box and text */
}

QCheckBox::indicator {
    width: 16px;
    height: 16px;
}

QCheckBox::indicator:unchecked {
    border: 1px solid #D6DEEA;
    background: #FFFFFF;
    border-radius: 4px;
}

QCheckBox::indicator:checked {
    border: 1px solid #0099FF;
    background: #0099FF;
    image: none; /* Ensures no default checkmark image conflicts */
}

QCheckBox::indicator:checked::hover {
    background: #0089E6; /* Slight hover effect for checked state */
}
"""


