# -- coding: utf-8 --
import time
import datetime
import traceback
from PyQt5.QtCore import *


# 定时线程
class TimeThread(QThread):
    active = True
    # 触发器
    zero_trigger = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    def stop(self):
        self.terminate()

    def run(self):
        while self.active:
            try:
                time.sleep(0.1)
                second = datetime.datetime.now().second
                if int(second) == 0:
                    self.zero_trigger.emit("xxx")
                    time.sleep(2)
            except Exception:
                traceback.print_exc()
