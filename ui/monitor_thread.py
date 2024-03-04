from PyQt5.QtCore import Qt, pyqtSignal, QObject, QTimer
import logging
import time
import threading

from utils import check_internet_connection
import sys

sys.path.append('../')  # 添加上一级目录到 sys.path
from authentication_utils import login, logout

# 要登录的URL
login_url = "http://10.0.1.5:801/eportal/portal/login"
logout_url = "http://10.0.1.5:801/eportal/portal/mac/unbind"


class MonitorThread(QObject):
    message_emitted = pyqtSignal(str)

    def __init__(self, username, password, operator_code):
        super().__init__()
        self.username = username
        self.password = password
        self.operator_code = operator_code
        self._stop_event = threading.Event()

    def run(self):
        while not self._stop_event.is_set():
            if not check_internet_connection():
                message = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 无法访问网络，正在重新登录校园网..."
                self.message_emitted.emit(message)
                logging.info("无法访问网络，正在重新登录校园网...")
                login_result = login(login_url, self.username, self.password, self.operator_code)
                if login_result == 1 or login_result == 2:
                    message = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 重新登陆成功"
                    self.message_emitted.emit(message)
                    logging.info("重新登陆成功")
                else:
                    message = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {login_result}"
                    self.message_emitted.emit(message)
                    logging.info(login_result)
            else:
                message = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 网络连接一切正常"
                self.message_emitted.emit(message)
                logging.info("网络连接一切正常")
            time.sleep(10)

    def stop(self):
        self._stop_event.set()
