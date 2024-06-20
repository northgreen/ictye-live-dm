import logging


class GUI_Handler(logging.Handler):
    def __init__(self, gui, *args, **b):
        super().__init__(*args, **b)
        self.mainwindow = gui

    def emit(self, record):
        record.message = record.getMessage()
        log_text = record.message
        log_level = record.levelname
        time_str = record
        self.mainwindow.submit_log(time_str, log_level, log_text)
