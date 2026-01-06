# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QMainWindow,
    QPushButton, QSizePolicy, QSpacerItem, QStackedWidget,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1106, 618)
        MainWindow.setStyleSheet(u"/* Fundo geral do App */\n"
"QMainWindow {\n"
"    background-color: #1a1a1a;\n"
"}\n"
"\n"
"/* Estilo da Barra Lateral */\n"
"QFrame#frame_sidebar {\n"
"    background-color: #252525;\n"
"    border: none;\n"
"    border-right: 1px solid #333;\n"
"}\n"
"\n"
"/* Bot\u00f5es da Barra Lateral */\n"
"QPushButton {\n"
"    background-color: transparent;\n"
"    color: #cccccc;\n"
"    border: none;\n"
"    border-radius: 5px;\n"
"    text-align: left;\n"
"    padding: 10px;\n"
"    font-size: 13px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #333333;\n"
"    color: white;\n"
"}\n"
"\n"
"/* Destaque para o bot\u00e3o ativo (precisaremos de l\u00f3gica Python depois) */\n"
"QPushButton:checked {\n"
"    background-color: #444444;\n"
"    border-left: 3px solid #0078d4;\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.frame_trigger = QFrame(self.centralwidget)
        self.frame_trigger.setObjectName(u"frame_trigger")
        self.frame_trigger.setMinimumSize(QSize(5, 0))
        self.frame_trigger.setMaximumSize(QSize(10, 16777215))
        self.frame_trigger.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_trigger.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout.addWidget(self.frame_trigger)

        self.frame_sidebar = QFrame(self.centralwidget)
        self.frame_sidebar.setObjectName(u"frame_sidebar")
        self.frame_sidebar.setMinimumSize(QSize(150, 0))
        self.frame_sidebar.setMaximumSize(QSize(200, 16777215))
        self.frame_sidebar.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_sidebar.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_sidebar)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.btn_toggle = QPushButton(self.frame_sidebar)
        self.btn_toggle.setObjectName(u"btn_toggle")

        self.verticalLayout.addWidget(self.btn_toggle)

        self.btn_home = QPushButton(self.frame_sidebar)
        self.btn_home.setObjectName(u"btn_home")

        self.verticalLayout.addWidget(self.btn_home)

        self.btn_library = QPushButton(self.frame_sidebar)
        self.btn_library.setObjectName(u"btn_library")

        self.verticalLayout.addWidget(self.btn_library)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.btn_settings = QPushButton(self.frame_sidebar)
        self.btn_settings.setObjectName(u"btn_settings")

        self.verticalLayout.addWidget(self.btn_settings)


        self.horizontalLayout.addWidget(self.frame_sidebar)

        self.stacked_pages = QStackedWidget(self.centralwidget)
        self.stacked_pages.setObjectName(u"stacked_pages")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.stacked_pages.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.stacked_pages.addWidget(self.page_2)

        self.horizontalLayout.addWidget(self.stacked_pages)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stacked_pages.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.btn_toggle.setText(QCoreApplication.translate("MainWindow", u"Toggle", None))
        self.btn_home.setText(QCoreApplication.translate("MainWindow", u"Home", None))
        self.btn_library.setText(QCoreApplication.translate("MainWindow", u"Library", None))
        self.btn_settings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
    # retranslateUi

