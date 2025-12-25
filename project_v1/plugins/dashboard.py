from PySide6.QtWidgets import QVBoxLayout, QLabel, QPushButton
from core.plugin_base import PluginInterface
from core.database import db  # 导入统一数据库


class DashboardPlugin(PluginInterface):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.label = QLabel("欢迎使用功能 A：数据仪表盘")
        self.btn = QPushButton("记录一条日志到数据库")

        self.btn.clicked.connect(self.log_data)

        layout.addWidget(self.label)
        layout.addWidget(self.btn)
        self.setLayout(layout)

    def get_name(self):
        return "仪表盘"

    def log_data(self):
        # 使用统一数据库存储数据
        db.execute_query("INSERT INTO system_logs (message) VALUES (?)", ("用户点击了按钮",))
        self.label.setText("数据已保存！")


# 这一行非常重要，主程序会寻找这个变量来加载插件
plugin_class = DashboardPlugin