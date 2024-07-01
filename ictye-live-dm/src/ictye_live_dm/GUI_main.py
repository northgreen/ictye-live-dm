import asyncio
import logging
import os
import sys
import threading

from PyQt5 import QtWidgets
from PyQt5.QtCore import QTranslator, Qt
from PyQt5.QtWidgets import QTreeWidgetItem, QStyledItemDelegate, QComboBox

from ictye_live_dm.depends import configs
from . import main as server
from . import pluginsystem
from .GUI import Ui_MainWindow
from .depends import logger

__all__ = ["main", "MainWindow"]
__logger__ = logging.getLogger(__name__)


class NonEditableDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        return None


def value_set(value):
    def __set(v):
        nonlocal value
        value = v

    return __set


class SettingTreeWidgetItem(QTreeWidgetItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class SettingTreeBuilder:
    def __init__(self, tree_widget):
        self.tree_widget = tree_widget

    def build_tree(self, key, value, value_manager, edit_function):
        display = [key, str(value)]
        editable = True
        if isinstance(value, dict):
            display[1] = "[Dict]"
            editable = False
        elif isinstance(value, list):
            display[1] = "[List]"
            editable = False
        parent = QTreeWidgetItem(self.tree_widget, display)

        if value_manager and value_manager.is_option():
            combo_box = QComboBox()
            combo_box.addItems([str(item) for item in value_manager.get_option()])
            self.tree_widget.setItemWidget(parent, 1, combo_box)
        elif type(value) is bool:
            combo_box = QComboBox()
            combo_box.addItems(["True", "False"])
            self.tree_widget.setItemWidget(parent, 1, combo_box)

        if editable:
            parent.setFlags(parent.flags() | Qt.ItemIsEditable)  # 设置父节点为可编辑

        if isinstance(value, dict):
            for k, v in value.items():
                SettingTreeBuilder(parent).build_tree(str(k), v, None, value_set(v))  # 递归处理子节点
        elif isinstance(value, list):
            for i, v in enumerate(value):
                SettingTreeBuilder(parent).build_tree(str(i), v, None, value_set(v))  # 递归处理子节点


class MainWindow(QtWidgets.QWidget, Ui_MainWindow.Ui_Form):
    _instance = None
    _server = None
    _inited = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, parent=None):
        if self._inited:
            return
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.tabWidget.setCurrentIndex(0)
        self.init_setting_tab()
        self.retranslateUi(self)
        self._server = ServerClass()
        self.startButtoen.clicked.connect(self.start_series)
        self.stopButton.clicked.connect(self.stop_series)
        self.settingTreeWidget.expandAll()

    def init_setting_tab(self):
        config = configs.ConfigManager()
        tree_builder = SettingTreeBuilder(self.settingTreeWidget)
        self.settingTreeWidget.setItemDelegateForColumn(0, NonEditableDelegate(self))

        for key, value in config.items():
            tree_builder.build_tree(key, value.get(), value, value.set)

    def submit_log(self, time, log_level, log_text):
        """
        寫入日志
        @param time: 時間
        @param log_level: 日誌等級
        @param log_text: 日志内容
        """
        try:
            row = self.logTable.rowCount()
            self.logTable.insertRow(row)
            self.logTable.setItem(row, 0, QtWidgets.QTableWidgetItem(time))
            self.logTable.setItem(row, 1, QtWidgets.QTableWidgetItem(log_level))
            self.logTable.setItem(row, 2, QtWidgets.QTableWidgetItem(log_text))
        except RuntimeError:
            pass
        finally:
            self.table_follow()

    def start_series(self):
        self._server.start()
        self.startButtoen.setEnabled(False)
        self.stopButton.setEnabled(True)

    def stop_series(self):
        self._server.stop()
        self.startButtoen.setEnabled(True)
        self.stopButton.setEnabled(False)

    def table_follow(self):
        if self.followCheckBox.isChecked():
            self.logTable.scrollToBottom()

    def show_plugin_list(self):
        plugins = pluginsystem.Plugin().list_plugin()
        for i in plugins:
            row = self.pluginListTable.rowCount()
            self.pluginListTable.insertRow(row)
            self.pluginListTable.setItem(row, 0, QtWidgets.QTableWidgetItem(i[0]))
            self.pluginListTable.setItem(row, 1, QtWidgets.QTableWidgetItem(i[1]))


class ServerClass:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=server.run_server, args=(self.loop,))

    def start(self):
        __logger__.info("Server start")
        self.thread = threading.Thread(target=server.run_server, args=(self.loop,))
        self.thread.start()

    def stop(self):
        __logger__.info("Server stoping")
        self.loop.stop()

    def get_status(self):
        return self.loop.is_running() and self.thread.is_alive()


def main():
    """
    GUI主程式
    """
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    app = QtWidgets.QApplication(sys.argv)

    # 讀取設定
    config = configs.ConfigManager()
    config.read_default(os.path.dirname(__file__) + "/config/system/config.yaml")

    translater = QTranslator()
    translater.load(os.path.dirname(__file__) + "/translate/zh-ch_MainUI.qm")
    app.installTranslator(translater)

    with open(os.path.normpath(os.path.dirname(__file__) + f'/GUI/StyleSheets/{config["style"]}.qss'), 'r',
              encoding='utf-8') as f:
        style = f.read()
        app.setStyleSheet(style)

    form = MainWindow()
    form.show_plugin_list()
    form.show()

    # 設定logger
    logger.setup_logging(window=form)

    # 啓動伺服器
    __server = ServerClass()
    form.startButtoen.setEnabled(not __server.get_status())
    form.stopButton.setEnabled(__server.get_status())
    # 啓動程式
    code = app.exec_()
    try:
        __server.stop()
    finally:
        sys.exit(code)


if __name__ == '__main__':
    main()
