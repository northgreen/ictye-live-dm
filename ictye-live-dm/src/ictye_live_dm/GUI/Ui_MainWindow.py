# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ictye-live-dm\src\QT-GUI\main.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(971, 638)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setMinimumSize(QtCore.QSize(223, 28))
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.startButtoen = QtWidgets.QPushButton(Form)
        self.startButtoen.setMaximumSize(QtCore.QSize(317, 28))
        self.startButtoen.setObjectName("startButtoen")
        self.horizontalLayout.addWidget(self.startButtoen)
        self.stopButton = QtWidgets.QPushButton(Form)
        self.stopButton.setMaximumSize(QtCore.QSize(316, 28))
        self.stopButton.setObjectName("stopButton")
        self.horizontalLayout.addWidget(self.stopButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setObjectName("tabWidget")
        self.log_Tab = QtWidgets.QWidget()
        self.log_Tab.setObjectName("log_Tab")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.log_Tab)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.logTable = QtWidgets.QTableWidget(self.log_Tab)
        self.logTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.logTable.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.logTable.setObjectName("logTable")
        self.logTable.setColumnCount(3)
        self.logTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.logTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.logTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.logTable.setHorizontalHeaderItem(2, item)
        self.logTable.horizontalHeader().setCascadingSectionResizes(False)
        self.logTable.horizontalHeader().setSortIndicatorShown(False)
        self.logTable.horizontalHeader().setStretchLastSection(True)
        self.logTable.verticalHeader().setCascadingSectionResizes(False)
        self.horizontalLayout_2.addWidget(self.logTable)
        self.tabWidget.addTab(self.log_Tab, "")
        self.setting_Tab = QtWidgets.QWidget()
        self.setting_Tab.setObjectName("setting_Tab")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.setting_Tab)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.settingScrollArea = QtWidgets.QScrollArea(self.setting_Tab)
        self.settingScrollArea.setWidgetResizable(True)
        self.settingScrollArea.setObjectName("settingScrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 919, 527))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.settingScrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout_3.addWidget(self.settingScrollArea)
        self.tabWidget.addTab(self.setting_Tab, "")
        self.verticalLayout.addWidget(self.tabWidget)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Ictye Live Danmmku"))
        self.label.setText(_translate("Form", "本項目由美國聖地亞哥（American Sangdiyagou）獨家贊助研發(x)"))
        self.startButtoen.setText(_translate("Form", "Start"))
        self.stopButton.setText(_translate("Form", "Stop"))
        item = self.logTable.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Time"))
        item = self.logTable.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Level"))
        item = self.logTable.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Contents"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.log_Tab), _translate("Form", "Log"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.setting_Tab), _translate("Form", "Setting"))
