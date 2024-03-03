import sys
import os
import json
import base64
import threading
import time
import logging
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy, QTextEdit, QLineEdit, QCheckBox, QComboBox, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QTimer
import requests

from authentication_utils import login, logout

# 定义保存加密后的登录信息的函数
def save_encrypted_login_info(username, password, operator):
    login_info = {
        'username': base64.b64encode(username.encode()).decode(),
        'password': base64.b64encode(password.encode()).decode(),
        'operator': base64.b64encode(operator.encode()).decode()
    }
    with open('login_info.json', 'w') as f:
        json.dump(login_info, f)

# 定义读取解密后的登录信息的函数
def load_decrypted_login_info():
    try:
        with open('login_info.json', 'r') as f:
            login_info = json.load(f)
            return base64.b64decode(login_info['username']).decode(), base64.b64decode(login_info['password']).decode(), base64.b64decode(login_info['operator']).decode()
    except FileNotFoundError:
        return None, None, None

class LoginWindow(QWidget):
    # 添加一个信号，在用户登录成功时发射
    login_successful = pyqtSignal()
    # 添加一个信号，在窗口关闭时发射
    window_closed = pyqtSignal()

    def show_progress_message(self, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("提示")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.NoButton)  # 不显示按钮
        msg_box.show()
        QTimer.singleShot(5000, msg_box.close)  # 延迟 2 秒后关闭消息框

    def __init__(self):
        super().__init__()
        self.setWindowTitle("校园网登录界面")
        self.init_ui()

    def init_ui(self):
        # 自定义窗口大小
        window_width = 500
        window_height = 400
        self.setFixedSize(window_width, window_height)  # 设置窗口固定大小

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        # 创建水平布局，用于水平居中
        hbox_layout = QHBoxLayout()

        # 账号输入框
        self.account_label = QLabel("账号:")
        self.account_label.setFont(QFont("Arial", 12))  # 设置字体大小
        self.account_entry = QLineEdit()
        self.account_entry.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        hbox_layout.addWidget(self.account_label)
        hbox_layout.addWidget(self.account_entry)

        # 添加空白小部件，用于调整布局
        hbox_layout.addStretch(1)

        main_layout.addLayout(hbox_layout)

        # 密码输入框
        self.password_label = QLabel("密码:")
        self.password_label.setFont(QFont("Arial", 12))  # 设置字体大小
        self.password_entry = QLineEdit()
        self.password_entry.setEchoMode(QLineEdit.Password)
        self.password_entry.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        hbox_layout2 = QHBoxLayout()
        hbox_layout2.addWidget(self.password_label)
        hbox_layout2.addWidget(self.password_entry)
        hbox_layout2.addStretch(1)
        main_layout.addLayout(hbox_layout2)

        # 显示密码复选框
        self.show_password_checkbox = QCheckBox("显示密码")
        self.show_password_checkbox.setFont(QFont("Arial", 12))  # 设置字体大小
        self.show_password_checkbox.stateChanged.connect(self.toggle_password_visibility)
        main_layout.addWidget(self.show_password_checkbox)

        # 创建水平布局，用于对齐下拉框
        hbox_layout3 = QHBoxLayout()

        # 运营商下拉框
        self.operator_label = QLabel("运营商:")
        self.operator_label.setFont(QFont("Arial", 12))  # 设置字体大小
        hbox_layout3.addWidget(self.operator_label)
        self.operator_combo = QComboBox()
        self.operator_combo.setFont(QFont("Arial", 12))  # 设置字体大小
        self.operator_combo.addItems(["中国移动", "中国电信", "中国联通", "校园网"])
        hbox_layout3.addWidget(self.operator_combo)
        hbox_layout3.addStretch(1)
        main_layout.addLayout(hbox_layout3)

        # 登录按钮
        self.login_button = QPushButton("登录")
        self.login_button.setFont(QFont("Arial", 14))  # 设置字体大小
        self.login_button.clicked.connect(self.login)
        main_layout.addWidget(self.login_button)

        # 注销按钮
        self.logout_button = QPushButton("注销")
        self.logout_button.setFont(QFont("Arial", 14))  # 设置字体大小
        self.logout_button.clicked.connect(self.logout)
        main_layout.addWidget(self.logout_button)

        self.setLayout(main_layout)

        # 加载登录信息
        username, password, operator = load_decrypted_login_info()

        # 如果有保存的登录信息，则显示到UI中
        if username and password and operator:
            self.account_entry.setText(username)
            self.password_entry.setText(password)
            index = self.operator_combo.findText(operator)
            if index != -1:
                self.operator_combo.setCurrentIndex(index)

    def login(self):
        account = self.account_entry.text()
        password = self.password_entry.text()
        operator = self.operator_combo.currentText()

        if operator == "中国移动":
            operator_code = "cmcc"
        elif operator == "中国电信":
            operator_code = "telecom"
        elif operator == "中国联通":
            operator_code = "unicom"
        elif operator == "校园网":
            operator_code = ""
        else:
            operator_code = ""

        # 执行登录操作
        login_result = login(login_url, account, password, operator_code)
        if login_result == 1:
            save_encrypted_login_info(account, password, operator_code)
            self.show_message_box('登录成功！')
            login_result = "登录成功"
            logging.info(login_result)
            time.sleep(1)
            # 登录成功时发射信号
            self.login_successful.emit()
        elif login_result == 2:
            save_encrypted_login_info(account, password, operator_code)
            self.show_message_box('你已经在线，点击OK进入监控...')
            logging.info("已经在线状态")
            self.login_successful.emit()
        else:
            self.show_message_box(login_result)
            logging.info(login_result)

    def logout(self):
        logout_result = logout(logout_url, self.account_entry.text())
        self.show_message_box(logout_result)

    def show_message_box(self, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("提示")
        msg_box.setText(message)
        msg_box.exec_()

    def toggle_password_visibility(self, state):
        if state == Qt.Checked:
            self.password_entry.setEchoMode(QLineEdit.Normal)
        else:
            self.password_entry.setEchoMode(QLineEdit.Password)


class MonitorWindow(QWidget):
    # 添加一个信号，在窗口关闭时发射
    window_closed = pyqtSignal()

    def __init__(self, monitor_thread):
        super().__init__()
        self.setWindowTitle("校园网自动监控中")
        self.setWindowFlags(Qt.Window | Qt.WindowMinimizeButtonHint)
        self.resize(700, 500)  # 设置监控窗口的大小
        self.monitor_thread = monitor_thread
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.monitor_label = QLabel("监控信息")
        self.monitor_label.setFont(QFont("Arial", 13))

        self.monitor_text = QTextEdit()
        self.monitor_text.setReadOnly(True)

        self.stop_button = QPushButton("停止监控")
        self.stop_button.clicked.connect(self.stop_monitoring)

        layout.addWidget(self.monitor_label)
        layout.addWidget(self.monitor_text)
        layout.addWidget(self.stop_button)

        self.setLayout(layout)

    def stop_monitoring(self):
        self.monitor_thread.stop()
        self.close()  # 关闭监控窗口
        login_window.show()  # 显示登录窗口


class MonitorThread(QObject):
    # 添加一个信号，用于发送监控信息
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
                # 发射监控信息信号
                message = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 无法访问网络，正在重新登录校园网..."
                self.message_emitted.emit(message)
                logging.info("无法访问网络，正在重新登录校园网...")  # 将日志信息写入文件
                login_result = login(login_url, self.username, self.password, self.operator_code)
                if login_result == 1 or login_result == 2:
                    message = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 重新登陆成功"
                    self.message_emitted.emit(message)
                    logging.info("重新登陆成功")  # 将日志信息写入文件
                else:
                    message = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {login_result}"
                    self.message_emitted.emit(message)
                    logging.info(login_result)  # 将日志信息写入文件
            else:
                # 发射监控信息信号
                message = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 网络连接一切正常"
                self.message_emitted.emit(message)
                logging.info("网络连接一切正常")  # 将日志信息写入文件
            time.sleep(10)  # 每隔五分钟检查一次


    def stop(self):
        self._stop_event.set()


def check_internet_connection():
    try:
        # 从系统环境变量中获取代理设置(你开了代理我也不怕)
        http_proxy = os.environ.get('HTTP_PROXY') 
        https_proxy = os.environ.get('HTTPS_PROXY')
        # 构造代理字典
        proxies = {
            'http': http_proxy,
            'https': https_proxy,
        }
        response = requests.get("https://www.baidu.com", timeout=5 ,proxies=proxies)
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        return False


# 要登录的URL
login_url = "http://10.0.1.5:801/eportal/portal/login"
logout_url = "http://10.0.1.5:801/eportal/portal/mac/unbind"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    logging.basicConfig(filename='monitor.log', level=logging.INFO, format='%(asctime)s - %(message)s')
    # 监听登录成功信号
    def on_login_successful():
        login_window.close()  # 关闭登录界面
        # 启动监视线程
        username, password, operator = login_window.account_entry.text(), login_window.password_entry.text(), login_window.operator_combo.currentText()
        operator_code = ""
        if operator == "中国移动":
            operator_code = "cmcc"
        elif operator == "中国电信":
            operator_code = "telecom"
        elif operator == "中国联通":
            operator_code = "unicom"
        elif operator == "校园网":
            operator_code = ""
        monitor_thread = MonitorThread(username, password, operator_code)
        monitor_thread_obj = threading.Thread(target=monitor_thread.run)
        monitor_thread_obj.start()
        global monitor_window
        monitor_window = MonitorWindow(monitor_thread)
        monitor_thread.message_emitted.connect(monitor_window.monitor_text.append)
        monitor_window.show()

    login_window.login_successful.connect(on_login_successful)
    login_window.show()

    # 监听登录窗口关闭信号
    def on_login_window_closed():
        sys.exit()  # 退出应用程序
    login_window.window_closed.connect(on_login_window_closed)
    
    sys.exit(app.exec_())
