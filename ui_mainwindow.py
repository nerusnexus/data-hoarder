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
    QTabWidget, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1126, 579)
        MainWindow.setStyleSheet(u"")
        MainWindow.setTabShape(QTabWidget.TabShape.Rounded)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_3 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.frame_main = QFrame(self.centralwidget)
        self.frame_main.setObjectName(u"frame_main")
        self.frame_main.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_main.setFrameShadow(QFrame.Shadow.Plain)
        self.frame_main.setLineWidth(0)
        self.verticalLayout_2 = QVBoxLayout(self.frame_main)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame_title_bar = QFrame(self.frame_main)
        self.frame_title_bar.setObjectName(u"frame_title_bar")
        self.frame_title_bar.setMaximumSize(QSize(16777215, 50))
        self.frame_title_bar.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_title_bar.setFrameShadow(QFrame.Shadow.Plain)
        self.frame_title_bar.setLineWidth(0)
        self.horizontalLayout = QHBoxLayout(self.frame_title_bar)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer = QSpacerItem(883, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.btn_minimize = QPushButton(self.frame_title_bar)
        self.btn_minimize.setObjectName(u"btn_minimize")
        self.btn_minimize.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout.addWidget(self.btn_minimize)

        self.btn_maximize = QPushButton(self.frame_title_bar)
        self.btn_maximize.setObjectName(u"btn_maximize")
        self.btn_maximize.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout.addWidget(self.btn_maximize)

        self.btn_close = QPushButton(self.frame_title_bar)
        self.btn_close.setObjectName(u"btn_close")
        self.btn_close.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout.addWidget(self.btn_close)


        self.verticalLayout_2.addWidget(self.frame_title_bar)

        self.frame_content = QFrame(self.frame_main)
        self.frame_content.setObjectName(u"frame_content")
        self.frame_content.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_content.setFrameShadow(QFrame.Shadow.Plain)
        self.frame_content.setLineWidth(0)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_content)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame_trigger = QFrame(self.frame_content)
        self.frame_trigger.setObjectName(u"frame_trigger")
        self.frame_trigger.setStyleSheet(u"border: none; background: transparent;")
        self.frame_trigger.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_trigger.setFrameShadow(QFrame.Shadow.Plain)
        self.frame_trigger.setLineWidth(0)

        self.horizontalLayout_2.addWidget(self.frame_trigger)

        self.frame_sidebar = QFrame(self.frame_content)
        self.frame_sidebar.setObjectName(u"frame_sidebar")
        self.frame_sidebar.setMinimumSize(QSize(150, 0))
        self.frame_sidebar.setMaximumSize(QSize(200, 16777215))
        self.frame_sidebar.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_sidebar.setFrameShadow(QFrame.Shadow.Plain)
        self.frame_sidebar.setLineWidth(0)
        self.verticalLayout = QVBoxLayout(self.frame_sidebar)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.btn_toggle = QPushButton(self.frame_sidebar)
        self.btn_toggle.setObjectName(u"btn_toggle")
        self.btn_toggle.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.verticalLayout.addWidget(self.btn_toggle)

        self.btn_home = QPushButton(self.frame_sidebar)
        self.btn_home.setObjectName(u"btn_home")
        self.btn_home.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.verticalLayout.addWidget(self.btn_home)

        self.btn_library = QPushButton(self.frame_sidebar)
        self.btn_library.setObjectName(u"btn_library")
        self.btn_library.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.verticalLayout.addWidget(self.btn_library)

        self.btn_database = QPushButton(self.frame_sidebar)
        self.btn_database.setObjectName(u"btn_database")
        self.btn_database.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.verticalLayout.addWidget(self.btn_database)

        self.btn_ytdlp = QPushButton(self.frame_sidebar)
        self.btn_ytdlp.setObjectName(u"btn_ytdlp")
        self.btn_ytdlp.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.verticalLayout.addWidget(self.btn_ytdlp)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.btn_settings = QPushButton(self.frame_sidebar)
        self.btn_settings.setObjectName(u"btn_settings")
        self.btn_settings.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.verticalLayout.addWidget(self.btn_settings)

        self.btn_info = QPushButton(self.frame_sidebar)
        self.btn_info.setObjectName(u"btn_info")

        self.verticalLayout.addWidget(self.btn_info)

        self.btn_closeSideTab = QPushButton(self.frame_sidebar)
        self.btn_closeSideTab.setObjectName(u"btn_closeSideTab")
        self.btn_closeSideTab.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.verticalLayout.addWidget(self.btn_closeSideTab)


        self.horizontalLayout_2.addWidget(self.frame_sidebar)

        self.stacked_pages = QStackedWidget(self.frame_content)
        self.stacked_pages.setObjectName(u"stacked_pages")
        self.stacked_pages.setLineWidth(0)
        self.page_home = QWidget()
        self.page_home.setObjectName(u"page_home")
        self.stacked_pages.addWidget(self.page_home)
        self.page_library = QWidget()
        self.page_library.setObjectName(u"page_library")
        self.stacked_pages.addWidget(self.page_library)
        self.page_ytdlp = QWidget()
        self.page_ytdlp.setObjectName(u"page_ytdlp")
        self.stacked_pages.addWidget(self.page_ytdlp)
        self.page_database = QWidget()
        self.page_database.setObjectName(u"page_database")
        self.stacked_pages.addWidget(self.page_database)
        self.page_settings = QWidget()
        self.page_settings.setObjectName(u"page_settings")
        self.stacked_pages.addWidget(self.page_settings)

        self.horizontalLayout_2.addWidget(self.stacked_pages)


        self.verticalLayout_2.addWidget(self.frame_content)


        self.horizontalLayout_3.addWidget(self.frame_main)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stacked_pages.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.btn_minimize.setText(QCoreApplication.translate("MainWindow", u"minimize", None))
        self.btn_maximize.setText(QCoreApplication.translate("MainWindow", u"maximize", None))
        self.btn_close.setText(QCoreApplication.translate("MainWindow", u"close", None))
        self.btn_toggle.setText(QCoreApplication.translate("MainWindow", u"Toggle", None))
        self.btn_home.setText(QCoreApplication.translate("MainWindow", u"Home", None))
        self.btn_library.setText(QCoreApplication.translate("MainWindow", u"Library", None))
        self.btn_database.setText(QCoreApplication.translate("MainWindow", u"Database", None))
        self.btn_ytdlp.setText(QCoreApplication.translate("MainWindow", u"YT-DLP", None))
        self.btn_settings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.btn_info.setText(QCoreApplication.translate("MainWindow", u"Info", None))
        self.btn_closeSideTab.setText(QCoreApplication.translate("MainWindow", u"Close Side Tab", None))
    # retranslateUi

