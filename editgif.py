# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'editgif.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                                QLineEdit, QComboBox ,QHBoxLayout, QVBoxLayout,QMainWindow)
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap,QImage
from PIL import Image
from PIL.ImageQt import ImageQt
import math

class Ui_EditWindow(object):
    def setupUi(self, EditWindow):
        EditWindow.setObjectName("EditWindow")
        EditWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(EditWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.topTextLabel = QtWidgets.QLabel(self.centralwidget)
        self.topTextLabel.setGeometry(QtCore.QRect(140, 380, 67, 17))
        self.topTextLabel.setObjectName("topTextLabel")
        self.bottomTextLabel = QtWidgets.QLabel(self.centralwidget)
        self.bottomTextLabel.setGeometry(QtCore.QRect(140, 420, 91, 17))
        self.bottomTextLabel.setObjectName("bottomTextLabel")
        self.topLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.topLineEdit.setGeometry(QtCore.QRect(260, 380, 113, 25))
        self.topLineEdit.setObjectName("topLineEdit")
        self.bottomLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.bottomLineEdit.setGeometry(QtCore.QRect(260, 420, 113, 25))
        self.bottomLineEdit.setObjectName("bottomLineEdit")
        self.filterTextLabel = QtWidgets.QLabel(self.centralwidget)
        self.filterTextLabel.setGeometry(QtCore.QRect(140, 460, 91, 17))
        self.filterTextLabel.setObjectName("filterTextLabel")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(260, 460, 111, 25))
        self.comboBox.setObjectName("comboBox")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(150, 30, 461, 311))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("Escritorio/205/finalProject/source.gif"))
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(650, 520, 89, 25))
        self.pushButton.setObjectName("pushButton")
        EditWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(EditWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        EditWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(EditWindow)
        self.statusbar.setObjectName("statusbar")
        EditWindow.setStatusBar(self.statusbar)

        self.retranslateUi(EditWindow)
        QtCore.QMetaObject.connectSlotsByName(EditWindow)
        EditWindow.show()

    def retranslateUi(self, EditWindow):
        _translate = QtCore.QCoreApplication.translate
        EditWindow.setWindowTitle(_translate("EditWindow", "MainWindow"))
        self.topTextLabel.setText(_translate("EditWindow", "Top Text"))
        self.bottomTextLabel.setText(_translate("EditWindow", "Bottom Text"))
        self.filterTextLabel.setText(_translate("EditWindow", "Filter"))
        self.pushButton.setText(_translate("EditWindow", "Create"))

app = QApplication(sys.argv)
main = Ui_EditWindow()
w = QMainWindow()
main.setupUi(w)
sys.exit(app.exec_())