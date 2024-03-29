import logging
import sys
import time

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy, QLineEdit, QCheckBox, \
    QComboBox, QMessageBox, QDialog

from utils import save_encrypted_login_info, load_decrypted_login_info

from authentication_utils import login, logout, login_unmac
from network_utils import validate_ip,validate_mac,format_mac

# 要登录的URL
login_url = "http://10.0.1.5:801/eportal/portal/login"
logout_url = "http://10.0.1.5:801/eportal/portal/mac/unbind"


class CustomDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("单独设置WAN_IP与MAC地址")

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 添加文字标签
        label = QLabel(
            "由于你可能连接了校园网再套了层局域网(也就是单独路由器),比如在实验室中，你可以自己找到路由器的WAN_IP和MAC地址来填写")
        label.setFont(QFont("Arial", 13))
        label.setAlignment(Qt.AlignCenter)
        label.setWordWrap(True)  # 允许自动换行
        layout.addWidget(label)

        # 添加说明标签和输入框
        self.ip_label = QLabel("WLAN用户IP:")
        self.ip_entry = QLineEdit()
        layout.addWidget(self.ip_label)
        layout.addWidget(self.ip_entry)

        self.mac_label = QLabel("WLAN用户MAC:")
        self.mac_entry = QLineEdit()
        layout.addWidget(self.mac_label)
        layout.addWidget(self.mac_entry)

        # 添加确认按钮
        self.confirm_button = QPushButton("确认")
        self.confirm_button.clicked.connect(self.confirm)
        layout.addWidget(self.confirm_button)

        self.setLayout(layout)

    def confirm(self):
        # 在此处处理确认按钮点击事件
        wlan_user_ip = self.ip_entry.text()
        wlan_user_mac = self.mac_entry.text()

        # 可以在此处进行进一步处理，如向服务器发送数据等
        self.accept()


class LoginWindow(QWidget):
    login_successful = pyqtSignal()
    window_closed = pyqtSignal()

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
        self.account_label = QLabel("学号:")
        self.account_label.setFont(QFont("Arial", 13))  # 设置字体大小
        self.account_entry = QLineEdit()
        self.account_entry.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        hbox_layout.addWidget(self.account_label)
        hbox_layout.addWidget(self.account_entry)

        # 添加空白小部件，用于调整布局
        hbox_layout.addStretch(1)

        main_layout.addLayout(hbox_layout)

        # 密码输入框
        self.password_label = QLabel("密码:")
        self.password_label.setFont(QFont("Arial", 13))  # 设置字体大小
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
        self.show_password_checkbox.setFont(QFont("Arial", 13))  # 设置字体大小
        self.show_password_checkbox.stateChanged.connect(self.toggle_password_visibility)
        main_layout.addWidget(self.show_password_checkbox)

        # 创建水平布局，用于对齐下拉框
        hbox_layout3 = QHBoxLayout()

        # 运营商下拉框
        self.operator_label = QLabel("运营商:")
        self.operator_label.setFont(QFont("Arial", 13))  # 设置字体大小
        hbox_layout3.addWidget(self.operator_label)
        self.operator_combo = QComboBox()
        self.operator_combo.setFont(QFont("Arial", 13))  # 设置字体大小
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

        if account == '' or password == '':
            self.show_message_box('请填学号或密码！')
        else:
            # 执行登录操作
            login_id, login_msg = login(login_url, account, password, operator_code)
            if login_id == 1:
                save_encrypted_login_info(account, password, operator_code)
                self.show_message_box('登录成功！')
                login_result = "登录成功"
                logging.info(login_result)
                time.sleep(1)
                # 登录成功时发射信号
                self.login_successful.emit()
            elif login_id == 2:
                save_encrypted_login_info(account, password, operator_code)
                self.show_message_box('你已经在线，点击OK进入监控...')
                logging.info("已经在线状态")
                self.login_successful.emit()
            elif login_id == 3:
                self.handle_login_id_3()
            else:
                self.show_message_box(login_msg)
                logging.info(login_msg)

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

    def handle_login_id_3(self):
        dialog = CustomDialog()
        if dialog.exec_() == QDialog.Accepted:
            # 用户点击了确认按钮
            wlan_user_ip = dialog.ip_entry.text().replace(" ", "")
            wlan_user_mac = dialog.mac_entry.text()
            if validate_mac(wlan_user_mac):
                wlan_user_mac = format_mac(wlan_user_mac)
            elif validate_ip(wlan_user_ip):
                wlan_user_ip = wlan_user_ip
            else:
                self.show_message_box('IP或MAC地址格式填写错误，请检查，MAC请使用\'-\'或\':\'连接；IP请使用10开头的点分十进制地址')
                self.handle_login_id_3()
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
            # 在此处处理用户输入的数据，可以将其发送到服务器等
            if account == '' or password == '':
                self.show_message_box('请填学号或密码！')
            else:
                # 执行登录操作
                login_id, login_msg = login_unmac(login_url, account, password, wlan_user_ip, wlan_user_mac,
                                                  operator_code)
                if login_id == 1:
                    save_encrypted_login_info(account, password, operator_code)
                    self.show_message_box('登录成功！')
                    login_result = "登录成功"
                    logging.info(login_result)
                    time.sleep(1)
                    # 登录成功时发射信号
                    self.login_successful.emit()
                elif login_id == 2:
                    save_encrypted_login_info(account, password, operator_code)
                    self.show_message_box('你已经在线，点击OK进入监控...')
                    logging.info("已经在线状态")
                    self.login_successful.emit()
                elif login_id == 3:
                    self.show_message_box('还是填写错误，你的路由器不是这个wan_ip或mac')
                    self.handle_login_id_3()
                else:
                    self.show_message_box(login_msg)
                    logging.info(login_msg)
