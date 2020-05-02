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
        self.btnBrowse.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnBrowse.setObjectName("btnBrowse")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(330, 50, 161, 101))
        self.listWidget.setObjectName("listWidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 90, 111, 31))
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 130, 111, 31))
        self.pushButton_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(10, 170, 111, 31))
        self.pushButton_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(10, 210, 111, 31))
        self.pushButton_4.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(10, 250, 111, 31))
        self.pushButton_5.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(10, 370, 111, 31))
        self.pushButton_6.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_6.setObjectName("pushButton_6")
        self.text_edit = QtWidgets.QTextEdit(self.centralwidget)
        self.text_edit.setGeometry(QtCore.QRect(150, 210, 341, 151))
        self.text_edit.setObjectName("text_edit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 291, 41))
        font = QtGui.QFont()
        font.setFamily("ObelixPro")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label.setTextFormat(QtCore.Qt.PlainText)
        self.label.setObjectName("label")
        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setGeometry(QtCore.QRect(10, 290, 111, 31))
        self.pushButton_7.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_8 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_8.setGeometry(QtCore.QRect(10, 330, 111, 31))
        self.pushButton_8.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_9 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_9.setGeometry(QtCore.QRect(0, 40, 251, 31))
        self.pushButton_9.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_9.setObjectName("pushButton_9")
        Encryptor.setCentralWidget(self.centralwidget)

        self.retranslateUi(Encryptor)
        QtCore.QMetaObject.connectSlotsByName(Encryptor)

    def retranslateUi(self, Encryptor):
        _translate = QtCore.QCoreApplication.translate
        Encryptor.setWindowTitle(_translate("Encryptor", "Encryptor 1.910"))
        self.btnBrowse.setText(_translate("Encryptor", "CHOOSE FOLDER"))
        self.pushButton.setText(_translate("Encryptor", "Write data"))
        self.pushButton_2.setText(_translate("Encryptor", "Generate keys"))
        self.pushButton_3.setText(_translate("Encryptor", "Erase keys"))
        self.pushButton_4.setText(_translate("Encryptor", "Encrypt"))
        self.pushButton_5.setText(_translate("Encryptor", "Decrypt"))
        self.pushButton_6.setText(_translate("Encryptor", "EXIT"))
        self.label.setText(_translate("Encryptor", "What do you want to do?"))
        self.pushButton_7.setText(_translate("Encryptor", "Twofish Encrypt"))
        self.pushButton_8.setText(_translate("Encryptor", "Twofish Decrypt"))
        self.pushButton_9.setText(_translate("Encryptor", "Check update"))
