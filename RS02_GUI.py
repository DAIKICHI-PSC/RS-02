# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'RS02_GUI.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
    QGroupBox, QLabel, QLineEdit, QMainWindow,
    QMenuBar, QPlainTextEdit, QPushButton, QRadioButton,
    QSizePolicy, QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(686, 520)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(7)
        MainWindow.setFont(font)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox_6 = QGroupBox(self.centralwidget)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.groupBox_6.setEnabled(False)
        self.groupBox_6.setMinimumSize(QSize(171, 81))
        self.groupBox_6.setMaximumSize(QSize(171, 16777215))
        font1 = QFont()
        font1.setPointSize(9)
        self.groupBox_6.setFont(font1)
        self.comboBox_1 = QComboBox(self.groupBox_6)
        self.comboBox_1.setObjectName(u"comboBox_1")
        self.comboBox_1.setEnabled(False)
        self.comboBox_1.setGeometry(QRect(10, 20, 69, 22))
        self.comboBox_1.setFont(font1)
        self.comboBox_1.setEditable(False)
        self.pushButton_12 = QPushButton(self.groupBox_6)
        self.pushButton_12.setObjectName(u"pushButton_12")
        self.pushButton_12.setEnabled(False)
        self.pushButton_12.setGeometry(QRect(90, 20, 71, 23))
        self.pushButton_12.setFont(font1)
        self.pushButton_13 = QPushButton(self.groupBox_6)
        self.pushButton_13.setObjectName(u"pushButton_13")
        self.pushButton_13.setEnabled(False)
        self.pushButton_13.setGeometry(QRect(10, 50, 71, 23))
        self.pushButton_13.setFont(font1)
        self.pushButton_14 = QPushButton(self.groupBox_6)
        self.pushButton_14.setObjectName(u"pushButton_14")
        self.pushButton_14.setEnabled(False)
        self.pushButton_14.setGeometry(QRect(90, 50, 71, 23))
        self.pushButton_14.setFont(font1)

        self.gridLayout.addWidget(self.groupBox_6, 2, 6, 2, 2)

        self.lineEdit_1 = QLineEdit(self.centralwidget)
        self.lineEdit_1.setObjectName(u"lineEdit_1")
        self.lineEdit_1.setMaximumSize(QSize(59, 22))
        font2 = QFont()
        font2.setPointSize(12)
        self.lineEdit_1.setFont(font2)
        self.lineEdit_1.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEdit_1, 5, 5, 1, 1)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setEnabled(False)
        self.groupBox_2.setMinimumSize(QSize(121, 111))
        self.groupBox_2.setFont(font1)
        self.checkBox_1 = QCheckBox(self.groupBox_2)
        self.checkBox_1.setObjectName(u"checkBox_1")
        self.checkBox_1.setGeometry(QRect(10, 20, 91, 16))
        self.checkBox_2 = QCheckBox(self.groupBox_2)
        self.checkBox_2.setObjectName(u"checkBox_2")
        self.checkBox_2.setGeometry(QRect(10, 40, 101, 16))
        self.comboBox_2 = QComboBox(self.groupBox_2)
        self.comboBox_2.setObjectName(u"comboBox_2")
        self.comboBox_2.setEnabled(False)
        self.comboBox_2.setGeometry(QRect(10, 80, 101, 22))
        self.comboBox_2.setFont(font1)
        self.comboBox_2.setEditable(False)
        self.checkBox_3 = QCheckBox(self.groupBox_2)
        self.checkBox_3.setObjectName(u"checkBox_3")
        self.checkBox_3.setGeometry(QRect(10, 60, 101, 16))

        self.gridLayout.addWidget(self.groupBox_2, 5, 1, 3, 1)

        self.pushButton_1 = QPushButton(self.centralwidget)
        self.pushButton_1.setObjectName(u"pushButton_1")
        self.pushButton_1.setEnabled(False)
        self.pushButton_1.setMaximumSize(QSize(83, 23))
        self.pushButton_1.setFont(font1)

        self.gridLayout.addWidget(self.pushButton_1, 0, 6, 1, 1)

        self.groupBox_4 = QGroupBox(self.centralwidget)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setEnabled(False)
        self.groupBox_4.setMinimumSize(QSize(61, 111))
        self.groupBox_4.setFont(font1)
        self.radioButton_10 = QRadioButton(self.groupBox_4)
        self.radioButton_10.setObjectName(u"radioButton_10")
        self.radioButton_10.setGeometry(QRect(10, 20, 61, 16))
        self.radioButton_10.setChecked(True)
        self.radioButton_11 = QRadioButton(self.groupBox_4)
        self.radioButton_11.setObjectName(u"radioButton_11")
        self.radioButton_11.setGeometry(QRect(10, 40, 61, 16))
        self.radioButton_12 = QRadioButton(self.groupBox_4)
        self.radioButton_12.setObjectName(u"radioButton_12")
        self.radioButton_12.setGeometry(QRect(10, 60, 61, 16))

        self.gridLayout.addWidget(self.groupBox_4, 5, 3, 3, 1)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMaximumSize(QSize(18, 38))
        self.label_2.setFont(font2)

        self.gridLayout.addWidget(self.label_2, 6, 4, 1, 1)

        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setEnabled(False)
        self.pushButton_2.setMaximumSize(QSize(83, 23))
        self.pushButton_2.setFont(font1)

        self.gridLayout.addWidget(self.pushButton_2, 0, 7, 1, 1)

        self.groupBox_5 = QGroupBox(self.centralwidget)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.groupBox_5.setEnabled(False)
        sizePolicy.setHeightForWidth(self.groupBox_5.sizePolicy().hasHeightForWidth())
        self.groupBox_5.setSizePolicy(sizePolicy)
        self.groupBox_5.setMinimumSize(QSize(171, 171))
        self.groupBox_5.setMaximumSize(QSize(171, 16777215))
        self.groupBox_5.setFont(font1)
        self.pushButton_9 = QPushButton(self.groupBox_5)
        self.pushButton_9.setObjectName(u"pushButton_9")
        self.pushButton_9.setEnabled(False)
        self.pushButton_9.setGeometry(QRect(90, 80, 71, 23))
        self.pushButton_9.setFont(font1)
        self.pushButton_4 = QPushButton(self.groupBox_5)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setEnabled(False)
        self.pushButton_4.setGeometry(QRect(10, 20, 71, 23))
        self.pushButton_4.setFont(font1)
        self.pushButton_6 = QPushButton(self.groupBox_5)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.pushButton_6.setEnabled(False)
        self.pushButton_6.setGeometry(QRect(10, 50, 71, 23))
        self.pushButton_6.setFont(font1)
        self.pushButton_7 = QPushButton(self.groupBox_5)
        self.pushButton_7.setObjectName(u"pushButton_7")
        self.pushButton_7.setEnabled(False)
        self.pushButton_7.setGeometry(QRect(90, 50, 71, 23))
        self.pushButton_7.setFont(font1)
        self.pushButton_5 = QPushButton(self.groupBox_5)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setEnabled(False)
        self.pushButton_5.setGeometry(QRect(90, 20, 71, 23))
        self.pushButton_5.setFont(font1)
        self.pushButton_8 = QPushButton(self.groupBox_5)
        self.pushButton_8.setObjectName(u"pushButton_8")
        self.pushButton_8.setEnabled(False)
        self.pushButton_8.setGeometry(QRect(10, 80, 71, 23))
        self.pushButton_8.setFont(font1)
        self.pushButton_11 = QPushButton(self.groupBox_5)
        self.pushButton_11.setObjectName(u"pushButton_11")
        self.pushButton_11.setEnabled(False)
        self.pushButton_11.setGeometry(QRect(10, 140, 71, 23))
        self.pushButton_11.setFont(font1)
        self.pushButton_3 = QPushButton(self.groupBox_5)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setEnabled(False)
        self.pushButton_3.setGeometry(QRect(10, 110, 71, 23))
        self.pushButton_3.setFont(font1)
        self.pushButton_10 = QPushButton(self.groupBox_5)
        self.pushButton_10.setObjectName(u"pushButton_10")
        self.pushButton_10.setEnabled(False)
        self.pushButton_10.setGeometry(QRect(90, 110, 71, 23))
        self.pushButton_10.setFont(font1)

        self.gridLayout.addWidget(self.groupBox_5, 1, 6, 1, 2)

        self.label_1 = QLabel(self.centralwidget)
        self.label_1.setObjectName(u"label_1")
        self.label_1.setMaximumSize(QSize(18, 38))
        self.label_1.setFont(font2)

        self.gridLayout.addWidget(self.label_1, 5, 4, 1, 1)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMaximumSize(QSize(18, 38))
        self.label_3.setFont(font2)

        self.gridLayout.addWidget(self.label_3, 7, 4, 1, 1)

        self.groupBox_1 = QGroupBox(self.centralwidget)
        self.groupBox_1.setObjectName(u"groupBox_1")
        self.groupBox_1.setMinimumSize(QSize(71, 111))
        self.groupBox_1.setFont(font1)
        self.radioButton_1 = QRadioButton(self.groupBox_1)
        self.radioButton_1.setObjectName(u"radioButton_1")
        self.radioButton_1.setGeometry(QRect(10, 20, 86, 16))
        self.radioButton_1.setChecked(True)
        self.radioButton_2 = QRadioButton(self.groupBox_1)
        self.radioButton_2.setObjectName(u"radioButton_2")
        self.radioButton_2.setGeometry(QRect(10, 40, 86, 16))
        self.radioButton_3 = QRadioButton(self.groupBox_1)
        self.radioButton_3.setObjectName(u"radioButton_3")
        self.radioButton_3.setGeometry(QRect(10, 60, 86, 16))

        self.gridLayout.addWidget(self.groupBox_1, 5, 0, 3, 1)

        self.lineEdit_3 = QLineEdit(self.centralwidget)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setMaximumSize(QSize(59, 22))
        self.lineEdit_3.setFont(font2)
        self.lineEdit_3.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEdit_3, 7, 5, 1, 1)

        self.groupBox_7 = QGroupBox(self.centralwidget)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.groupBox_7.setEnabled(True)
        self.groupBox_7.setMinimumSize(QSize(171, 51))
        self.groupBox_7.setMaximumSize(QSize(171, 16777215))
        self.groupBox_7.setFont(font1)
        self.pushButton_15 = QPushButton(self.groupBox_7)
        self.pushButton_15.setObjectName(u"pushButton_15")
        self.pushButton_15.setEnabled(True)
        self.pushButton_15.setGeometry(QRect(10, 20, 71, 23))
        self.pushButton_15.setFont(font1)
        self.pushButton_16 = QPushButton(self.groupBox_7)
        self.pushButton_16.setObjectName(u"pushButton_16")
        self.pushButton_16.setEnabled(True)
        self.pushButton_16.setGeometry(QRect(90, 20, 71, 23))
        self.pushButton_16.setFont(font1)

        self.gridLayout.addWidget(self.groupBox_7, 4, 6, 1, 2)

        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setEnabled(False)
        self.groupBox_3.setMinimumSize(QSize(131, 111))
        self.groupBox_3.setFont(font1)
        self.radioButton_4 = QRadioButton(self.groupBox_3)
        self.radioButton_4.setObjectName(u"radioButton_4")
        self.radioButton_4.setGeometry(QRect(10, 20, 86, 16))
        self.radioButton_4.setChecked(True)
        self.radioButton_5 = QRadioButton(self.groupBox_3)
        self.radioButton_5.setObjectName(u"radioButton_5")
        self.radioButton_5.setGeometry(QRect(10, 40, 86, 16))
        self.radioButton_6 = QRadioButton(self.groupBox_3)
        self.radioButton_6.setObjectName(u"radioButton_6")
        self.radioButton_6.setGeometry(QRect(10, 60, 86, 16))
        self.radioButton_7 = QRadioButton(self.groupBox_3)
        self.radioButton_7.setObjectName(u"radioButton_7")
        self.radioButton_7.setGeometry(QRect(70, 20, 61, 16))
        self.radioButton_8 = QRadioButton(self.groupBox_3)
        self.radioButton_8.setObjectName(u"radioButton_8")
        self.radioButton_8.setGeometry(QRect(70, 40, 61, 16))
        self.radioButton_9 = QRadioButton(self.groupBox_3)
        self.radioButton_9.setObjectName(u"radioButton_9")
        self.radioButton_9.setGeometry(QRect(70, 60, 61, 16))

        self.gridLayout.addWidget(self.groupBox_3, 5, 2, 3, 1)

        self.lineEdit_2 = QLineEdit(self.centralwidget)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setMaximumSize(QSize(59, 22))
        self.lineEdit_2.setFont(font2)
        self.lineEdit_2.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEdit_2, 6, 5, 1, 1)

        self.groupBox_8 = QGroupBox(self.centralwidget)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.groupBox_8.setEnabled(True)
        self.groupBox_8.setMinimumSize(QSize(171, 101))
        self.groupBox_8.setMaximumSize(QSize(171, 16777215))
        self.groupBox_8.setFont(font1)
        self.pushButton_17 = QPushButton(self.groupBox_8)
        self.pushButton_17.setObjectName(u"pushButton_17")
        self.pushButton_17.setEnabled(True)
        self.pushButton_17.setGeometry(QRect(80, 70, 71, 23))
        self.pushButton_17.setFont(font1)
        self.lineEdit_4 = QLineEdit(self.groupBox_8)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        self.lineEdit_4.setGeometry(QRect(70, 20, 81, 20))
        self.lineEdit_4.setFont(font2)
        self.lineEdit_4.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.lineEdit_4.setReadOnly(True)
        self.lineEdit_5 = QLineEdit(self.groupBox_8)
        self.lineEdit_5.setObjectName(u"lineEdit_5")
        self.lineEdit_5.setGeometry(QRect(70, 40, 81, 20))
        self.lineEdit_5.setFont(font2)
        self.lineEdit_5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.lineEdit_5.setReadOnly(True)
        self.label_4 = QLabel(self.groupBox_8)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(10, 20, 51, 16))
        self.label_4.setFont(font2)
        self.label_5 = QLabel(self.groupBox_8)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(10, 40, 51, 16))
        self.label_5.setFont(font2)

        self.gridLayout.addWidget(self.groupBox_8, 5, 6, 3, 2)

        self.plainTextEdit_1 = QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_1.setObjectName(u"plainTextEdit_1")
        self.plainTextEdit_1.setMinimumSize(QSize(0, 0))
        font3 = QFont()
        font3.setPointSize(18)
        font3.setBold(True)
        self.plainTextEdit_1.setFont(font3)
        self.plainTextEdit_1.setAutoFillBackground(False)
        self.plainTextEdit_1.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.plainTextEdit_1.setReadOnly(False)

        self.gridLayout.addWidget(self.plainTextEdit_1, 0, 0, 3, 6)

        self.plainTextEdit_2 = QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_2.setObjectName(u"plainTextEdit_2")
        self.plainTextEdit_2.setEnabled(True)
        self.plainTextEdit_2.setFont(font2)
        self.plainTextEdit_2.setAutoFillBackground(False)
        self.plainTextEdit_2.setReadOnly(True)
        self.plainTextEdit_2.setBackgroundVisible(False)

        self.gridLayout.addWidget(self.plainTextEdit_2, 3, 0, 2, 6)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 686, 18))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"RS-02 V1.0", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("MainWindow", u"SERIAL", None))
        self.pushButton_12.setText(QCoreApplication.translate("MainWindow", u"PORTS", None))
        self.pushButton_13.setText(QCoreApplication.translate("MainWindow", u"D CON", None))
        self.pushButton_14.setText(QCoreApplication.translate("MainWindow", u"D DIS", None))
        self.lineEdit_1.setText("")
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"SWITCH", None))
        self.checkBox_1.setText(QCoreApplication.translate("MainWindow", u"ONE CYCLE", None))
        self.checkBox_2.setText(QCoreApplication.translate("MainWindow", u"SINGLE BLOCK", None))
        self.checkBox_3.setText(QCoreApplication.translate("MainWindow", u"DEBUG", None))
        self.pushButton_1.setText(QCoreApplication.translate("MainWindow", u"RUN", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"RAPID", None))
        self.radioButton_10.setText(QCoreApplication.translate("MainWindow", u"25", None))
        self.radioButton_11.setText(QCoreApplication.translate("MainWindow", u"50", None))
        self.radioButton_12.setText(QCoreApplication.translate("MainWindow", u"100", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Y :", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"STOP", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"DOBOT", None))
        self.pushButton_9.setText(QCoreApplication.translate("MainWindow", u"Z-", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"X+", None))
        self.pushButton_6.setText(QCoreApplication.translate("MainWindow", u"Y+", None))
        self.pushButton_7.setText(QCoreApplication.translate("MainWindow", u"Y-", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"X-", None))
        self.pushButton_8.setText(QCoreApplication.translate("MainWindow", u"Z+", None))
        self.pushButton_11.setText(QCoreApplication.translate("MainWindow", u"POSITION", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"HOME", None))
        self.pushButton_10.setText(QCoreApplication.translate("MainWindow", u"WRITE", None))
        self.label_1.setText(QCoreApplication.translate("MainWindow", u"X :", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Z :", None))
        self.groupBox_1.setTitle(QCoreApplication.translate("MainWindow", u"MODE", None))
        self.radioButton_1.setText(QCoreApplication.translate("MainWindow", u"EDIT", None))
        self.radioButton_2.setText(QCoreApplication.translate("MainWindow", u"AUTO", None))
        self.radioButton_3.setText(QCoreApplication.translate("MainWindow", u"JOG", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("MainWindow", u"FILE", None))
        self.pushButton_15.setText(QCoreApplication.translate("MainWindow", u"OPEN", None))
        self.pushButton_16.setText(QCoreApplication.translate("MainWindow", u"SAVE", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"OVERRIDE", None))
        self.radioButton_4.setText(QCoreApplication.translate("MainWindow", u"0.1mm", None))
        self.radioButton_5.setText(QCoreApplication.translate("MainWindow", u"1mm", None))
        self.radioButton_6.setText(QCoreApplication.translate("MainWindow", u"5mm", None))
        self.radioButton_7.setText(QCoreApplication.translate("MainWindow", u"10mm", None))
        self.radioButton_8.setText(QCoreApplication.translate("MainWindow", u"20mm", None))
        self.radioButton_9.setText(QCoreApplication.translate("MainWindow", u"30mm", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("MainWindow", u"COUNTER", None))
        self.pushButton_17.setText(QCoreApplication.translate("MainWindow", u"RESET", None))
        self.lineEdit_4.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.lineEdit_5.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"COUNT", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"NG", None))
    # retranslateUi

