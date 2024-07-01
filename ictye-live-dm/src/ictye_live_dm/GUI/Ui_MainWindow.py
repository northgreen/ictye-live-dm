# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\main.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setWindowModality(QtCore.Qt.NonModal)
        Form.resize(765, 681)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(".\\../ictye_live_dm/icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        Form.setStyleSheet("")
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
        self.stopButton.setEnabled(True)
        self.stopButton.setMaximumSize(QtCore.QSize(316, 28))
        self.stopButton.setObjectName("stopButton")
        self.horizontalLayout.addWidget(self.stopButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.West)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setElideMode(QtCore.Qt.ElideNone)
        self.tabWidget.setMovable(False)
        self.tabWidget.setTabBarAutoHide(False)
        self.tabWidget.setObjectName("tabWidget")
        self.log_Tab = QtWidgets.QWidget()
        self.log_Tab.setObjectName("log_Tab")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.log_Tab)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.totalLogLable = QtWidgets.QLabel(self.log_Tab)
        self.totalLogLable.setObjectName("totalLogLable")
        self.horizontalLayout_2.addWidget(self.totalLogLable)
        self.followCheckBox = QtWidgets.QCheckBox(self.log_Tab)
        self.followCheckBox.setEnabled(True)
        self.followCheckBox.setMaximumSize(QtCore.QSize(194, 16777215))
        self.followCheckBox.setTabletTracking(False)
        self.followCheckBox.setChecked(True)
        self.followCheckBox.setTristate(False)
        self.followCheckBox.setObjectName("followCheckBox")
        self.horizontalLayout_2.addWidget(self.followCheckBox)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.logTable = QtWidgets.QTableWidget(self.log_Tab)
        self.logTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.logTable.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.logTable.setShowGrid(True)
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
        self.verticalLayout_4.addWidget(self.logTable)
        self.tabWidget.addTab(self.log_Tab, "")
        self.pluginListPage = QtWidgets.QWidget()
        self.pluginListPage.setObjectName("pluginListPage")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.pluginListPage)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pluginTotalLable = QtWidgets.QLabel(self.pluginListPage)
        self.pluginTotalLable.setObjectName("pluginTotalLable")
        self.verticalLayout_2.addWidget(self.pluginTotalLable)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.lineEdit = QtWidgets.QLineEdit(self.pluginListPage)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_4.addWidget(self.lineEdit)
        self.pushButton = QtWidgets.QPushButton(self.pluginListPage)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_4.addWidget(self.pushButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.pluginListTable = QtWidgets.QTableWidget(self.pluginListPage)
        self.pluginListTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.pluginListTable.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.pluginListTable.setObjectName("pluginListTable")
        self.pluginListTable.setColumnCount(2)
        self.pluginListTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.pluginListTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.pluginListTable.setHorizontalHeaderItem(1, item)
        self.pluginListTable.horizontalHeader().setCascadingSectionResizes(False)
        self.pluginListTable.horizontalHeader().setSortIndicatorShown(False)
        self.pluginListTable.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout_2.addWidget(self.pluginListTable)
        self.tabWidget.addTab(self.pluginListPage, "")
        self.setting_Tab = QtWidgets.QWidget()
        self.setting_Tab.setObjectName("setting_Tab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.setting_Tab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.settingScrollArea = QtWidgets.QScrollArea(self.setting_Tab)
        self.settingScrollArea.setLineWidth(3)
        self.settingScrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.settingScrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.settingScrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.settingScrollArea.setWidgetResizable(True)
        self.settingScrollArea.setAlignment(QtCore.Qt.AlignCenter)
        self.settingScrollArea.setObjectName("settingScrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 732, 592))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.settingTreeWidget = QtWidgets.QTreeWidget(self.scrollAreaWidgetContents)
        self.settingTreeWidget.setMinimumSize(QtCore.QSize(710, 117))
        self.settingTreeWidget.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.settingTreeWidget.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked|QtWidgets.QAbstractItemView.EditKeyPressed|QtWidgets.QAbstractItemView.SelectedClicked)
        self.settingTreeWidget.setObjectName("settingTreeWidget")
        self.verticalLayout_5.addWidget(self.settingTreeWidget)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(90, 20, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.applyButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.applyButton.setObjectName("applyButton")
        self.horizontalLayout_3.addWidget(self.applyButton)
        spacerItem1 = QtWidgets.QSpacerItem(90, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout_5.addLayout(self.horizontalLayout_3)
        self.settingScrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_3.addWidget(self.settingScrollArea)
        self.tabWidget.addTab(self.setting_Tab, "")
        self.verticalLayout.addWidget(self.tabWidget)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Ictye Live Danmmku"))
        self.label.setText(_translate("Form", "本項目由美國聖地亞哥（American Sangdiyagou）獨家贊助研發(x)"))
        self.startButtoen.setText(_translate("Form", "Start"))
        self.stopButton.setText(_translate("Form", "Stop"))
        self.totalLogLable.setText(_translate("Form", "Total"))
        self.followCheckBox.setText(_translate("Form", "Follow newest log"))
        self.logTable.setSortingEnabled(False)
        item = self.logTable.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Time"))
        item = self.logTable.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Level"))
        item = self.logTable.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Contents"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.log_Tab), _translate("Form", "Log"))
        self.pluginTotalLable.setText(_translate("Form", "Total:"))
        self.pushButton.setText(_translate("Form", "Submit"))
        item = self.pluginListTable.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Plugin name"))
        item = self.pluginListTable.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Description"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.pluginListPage), _translate("Form", "Plugins"))
        self.settingTreeWidget.headerItem().setText(0, _translate("Form", "Item"))
        self.settingTreeWidget.headerItem().setText(1, _translate("Form", "Value"))
        self.applyButton.setText(_translate("Form", "Apply"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.setting_Tab), _translate("Form", "Setting"))
