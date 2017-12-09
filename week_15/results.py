# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'results.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(767, 462)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.srch_label = QtWidgets.QLabel(Form)
        self.srch_label.setObjectName("srch_label")
        self.horizontalLayout.addWidget(self.srch_label)
        self.searchbar = QtWidgets.QLineEdit(Form)
        self.searchbar.setObjectName("searchbar")
        self.horizontalLayout.addWidget(self.searchbar)
        self.srch_btn = QtWidgets.QPushButton(Form)
        self.srch_btn.setObjectName("srch_btn")
        self.horizontalLayout.addWidget(self.srch_btn)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.columnView = QtWidgets.QColumnView(Form)
        self.columnView.setAlternatingRowColors(True)
        self.columnView.setObjectName("columnView")
        self.verticalLayout_4.addWidget(self.columnView)
        self.verticalLayout_3.addLayout(self.verticalLayout_4)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.srch_label.setText(_translate("Form", "Search Again:"))
        self.srch_btn.setText(_translate("Form", "Search"))

