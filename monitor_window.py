from PyQt5.QtWidgets import QWidget, QLabel, QTextEdit, QPushButton, QVBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSignal,Qt
from monitor_thread import MonitorThread
import sys
class MonitorWindow(QWidget):
    window_closed = pyqtSignal()

    def __init__(self, monitor_thread):
        super().__init__()
        self.setWindowTitle("校园网自动监控中")
        self.setWindowFlags(Qt.Window | Qt.WindowMinimizeButtonHint)
        self.resize(700, 500)
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
        sys.exit()

