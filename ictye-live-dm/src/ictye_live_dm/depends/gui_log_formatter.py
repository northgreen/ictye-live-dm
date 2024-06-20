import logging
from PyQt5 import QtCore, QtGui, QtWidgets


class GuiLogFormatter(logging.Formatter):
    """
    Custom log formatter for the GUI.
    """

    def __init__(self, gui, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mainwindow = gui

    def format(self, record):
        record.message = record.getMessage()
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)
        log_text = self.formatMessage(record)
        log_level = record.levelname
        time_str = self.formatTime(record, self.datefmt)
        self.mainwindow.submit_log(time_str, log_level, log_text)
        return ""
