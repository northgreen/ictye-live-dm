import asyncio
import os
import sys
import threading
import logging

from PyQt5 import QtWidgets

from ictye_live_dm.depends import configs
from . import main as server
from .GUI import Ui_MainWindow
from .depends import logger

__logger__ = logging.getLogger(__name__)


class MainWindow(QtWidgets.QWidget, Ui_MainWindow.Ui_Form):
    _instance = None
    _server = None
    _inited = False

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
        if self._inited:
            return
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self._server = ServerClass()
        self.startButtoen.clicked.connect(self.start_series)
        self.stopButton.clicked.connect(self.stop_series)

    def start_series(self):
        self._server.start()
        self.startButtoen.setEnabled(False)
        self.stopButton.setEnabled(True)

    def stop_series(self):
        self._server.stop()
        self.startButtoen.setEnabled(True)
        self.stopButton.setEnabled(False)


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
    form = MainWindow()
    form.show()

    # 讀取設定
    config = configs.ConfigManager()
    config.read_default(os.path.dirname(__file__) + "/config/system/config.yaml")

    # 設定logger
    logger.setup_logging(False, form)

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
