import asyncio
import logging
import os
import sys
import threading
from typing import Union

from PyQt5 import QtWidgets
from PyQt5.QtCore import QTranslator, Qt
from PyQt5.QtWidgets import QTreeWidgetItem, QStyledItemDelegate, QComboBox

from ictye_live_dm.depends import configs, config_registrar
from . import main as server
from . import pluginsystem
from .GUI import Ui_MainWindow
from .depends import logger

__all__ = ["main", "MainWindow"]
__logger__ = logging.getLogger(__name__)


class NonEditableDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        return None


class SettingTreeWidgetItem(QTreeWidgetItem):
    def __init__(self, parent, key, values: Union[config_registrar.ConfigTree, config_registrar.ConfigKey]):
        print(repr(values))  # TODO： 臨時代碼
        self.__value = values
        keys = [str(key), str("" if isinstance(values, config_registrar.ConfigTree) else values.get())]
        super().__init__(parent, keys)

        if isinstance(values, config_registrar.ConfigKey) and values.has_option():
            combo_box = QComboBox()
            combo_box.addItems([str(item) for item in values.get_options()])
            self.treeWidget().setItemWidget(self, 1, combo_box)

    def setData(self, column, role, value):
        print(value)  # TODO： 臨時代碼
        if isinstance(self.__value, config_registrar.ConfigKey):
            self.__value.set(value)
        super().setData(column, role, value)


class SettingTreeBuilder:
    def __init__(self, tree_widget):
        self.tree_widget = tree_widget

    def build_tree(self, config_tree: config_registrar.ConfigTree):
        parent: QTreeWidgetItem
        if config_tree.is_list():
            for i, v in enumerate(config_tree.values()):
                parent = SettingTreeWidgetItem(self.tree_widget, i, v)
                if isinstance(v, config_registrar.ConfigKey):
                    parent.setFlags(parent.flags() | Qt.ItemIsEditable)

                if isinstance(v, config_registrar.ConfigTree):
                    SettingTreeBuilder(parent).build_tree(v)

        elif config_tree.is_dict():
            for k, v in config_tree.items():
                parent = SettingTreeWidgetItem(self.tree_widget, k, v)
                if isinstance(v, config_registrar.ConfigKey):
                    parent.setFlags(parent.flags() | Qt.ItemIsEditable)

                if isinstance(v, config_registrar.ConfigTree):
                    SettingTreeBuilder(parent).build_tree(v)


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
        config_tree = config.get_config_tree()
        tree_builder.build_tree(config_tree)

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
