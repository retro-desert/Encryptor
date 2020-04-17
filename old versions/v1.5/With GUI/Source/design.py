# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Encryptor(object):
    def setupUi(self, Encryptor):
        Encryptor.setObjectName("Encryptor")
        Encryptor.resize(553, 411)
        self.centralwidget = QtWidgets.QWidget(Encryptor)
        self.centralwidget.setObjectName("centralwidget")
        self.btnBrowse = QtWidgets.QPushButton(self.centralwidget)
        self.btnBrowse.setGeometry(QtCore.QRect(330, 0, 161, 41))
        self.btnBrowse.setObjectName("btnBrowse")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(330, 50, 161, 101))
        self.listWidget.setObjectName("listWidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 52, 111, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 90, 111, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(10, 130, 111, 31))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(10, 170, 111, 31))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(10, 210, 111, 31))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(10, 250, 111, 31))
        self.pushButton_6.setObjectName("pushButton_6")
        self.text_edit = QtWidgets.QTextEdit(self.centralwidget)
        self.text_edit.setGeometry(QtCore.QRect(150, 210, 361, 161))
        self.text_edit.setObjectName("text_edit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 291, 41))
        font = QtGui.QFont()
        font.setFamily("ObelixPro")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label.setTextFormat(QtCore.Qt.PlainText)
        self.label.setObjectName("label")
        Encryptor.setCentralWidget(self.centralwidget)

        self.retranslateUi(Encryptor)
        QtCore.QMetaObject.connectSlotsByName(Encryptor)

    def retranslateUi(self, Encryptor):
        _translate = QtCore.QCoreApplication.translate
        Encryptor.setWindowTitle(_translate("Encryptor", "Encryptor 1.5"))
        self.btnBrowse.setText(_translate("Encryptor", "CHOOSE FOLDER"))
        self.pushButton.setText(_translate("Encryptor", "Write data"))
        self.pushButton_2.setText(_translate("Encryptor", "Generate keys"))
        self.pushButton_3.setText(_translate("Encryptor", "Erase keys"))
        self.pushButton_4.setText(_translate("Encryptor", "Encrypt"))
        self.pushButton_5.setText(_translate("Encryptor", "Decrypt"))
        self.pushButton_6.setText(_translate("Encryptor", "EXIT"))
        self.label.setText(_translate("Encryptor", "What do you want to do?"))
