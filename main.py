import sys
from PyQt5.QtWidgets import QApplication
from login_window import LoginWindow
import logging
from PyQt5.QtGui import QIcon
import threading
import image

from monitor_thread import MonitorThread
from monitor_window import MonitorWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(':/icon.png'))
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
