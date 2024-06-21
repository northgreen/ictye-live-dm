import logging
import time


# noinspection PyPep8Naming
class GUI_Handler(logging.Handler):
    def __init__(self, gui, *args, **b):
        super().__init__(*args, **b)
        self.main_window = gui

    def emit(self, record: logging.LogRecord):
        record.message = record.getMessage()
        log_text = record.message
        log_level = record.levelname
        time_str = time.strftime("%Y-%m-%d %H: %M: %S", time.localtime(record.created))
        self.main_window.submit_log(time_str, log_level, log_text)
