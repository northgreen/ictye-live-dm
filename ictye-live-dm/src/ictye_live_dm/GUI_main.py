import asyncio
import os
import sys
import threading

from PyQt5 import QtWidgets

from ictye_live_dm.depends import configs
from . import main as server
from .GUI import Ui_MainWindow
from .depends import logger


class MainWindow(QtWidgets.QWidget, Ui_MainWindow.Ui_Form):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

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

    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        self.setupUi(self)


class SeriverClass:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.loop = asyncio.new_event_loop()

    def start(self):
        thread = threading.Thread(target=server.run_server, args=(self.loop,))
        thread.start()

    def stop(self):
        self.loop.stop()


def main():
    """
    GUI主程式
    """
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    app = QtWidgets.QApplication(sys.argv)
    form = MainWindow()
    form.show()

    # 讀取設定
    config = configs.ConfigManager()
    config.read_default(os.path.dirname(__file__) + "/config/system/config.yaml")

    # 設定logger
    logger.setup_logging(False, form)

    # 啓動伺服器
    __server = SeriverClass()
    __server.start()
    # 啓動程式
    code = app.exec_()
    try:
        __server.stop()
    finally:
        sys.exit(code)


if __name__ == '__main__':
    main()
