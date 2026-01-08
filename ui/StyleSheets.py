MAIN_STYLE_SHEET = """
    QWidget#centralwidget {
        background-color: #1a1a1a;
        border-radius: 10px;
    }
    QFrame#frame_sidebar {
        background-color: #1a1a1a;
        border-bottom-left-radius: 10px;
        padding-bottom: 10px;
    }
    QFrame#frame_content, QStackedWidget, QWidget#page, QWidget#page_2 {
        background-color: transparent;
    }

    /* Botões da Sidebar */
    QFrame#frame_sidebar QPushButton {
        background-color: transparent;
        border: none;
        border-radius: 5px;
        color: #FFFFFF;
        text-align: left;
        padding: 5px;
        max-height: 50px;
        font-size: 16px;
        font-family: 'Segoe UI', sans-serif;
    }
    QFrame#frame_sidebar QPushButton:hover { background-color: #333333; color: white; }
    QFrame#frame_sidebar QPushButton:checked { background-color: #444444; color: white; }

    /* Botões de Janela */
    QPushButton#btn_close, QPushButton#btn_minimize, QPushButton#btn_maximize {
        background-color: transparent; border: none; border-radius: 10px; color: #cccccc; padding: 5px;
    }
    QPushButton#btn_close:hover { background-color: #ff5555; color: white; }
    QPushButton#btn_minimize:hover { background-color: #333333; color: white; }
    QPushButton#btn_maximize:hover { background-color: #333333; color: white; }

    QLabel#lbl_app_title {
        color: #FFFFFF; font-family: 'Segoe UI'; font-weight: bold; font-size: 14px; padding-left: 10px;
    }
"""

FLOATING_OPEN_BUTTON = """
QPushButton { background-color: #252525; border-left: none; border-top-right-radius: 5px; border-bottom-right-radius: 5px; }
QPushButton:hover { background-color: #0078d4; }
"""

YtDlp_PAGE = """
QTabWidget::pane {
    background: #121212;
    border-top-right-radius: 5px;
    border-bottom-right-radius: 5px;
    border-bottom-left-radius: 5px;
}
QTabBar::tab {
    background: #252525;
    color: #cccccc;
    padding: 5px 5px;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
    margin-right: 0px;
}
QTabBar::tab:selected {
    background: #333333;
    color: white;
}
QTabBar::tab:hover {
    background: #333333;
}
"""

SIDEBAR_BUTTON_MARGIN = "margin-top: {}px;"
