from PySide6.QtWidgets import (QApplication, QMainWindow, QTabWidget,
                               QDockWidget, QTextEdit, QWidget,
                               QVBoxLayout, QHBoxLayout, QLabel,
                               QLineEdit, QPushButton, QMessageBox) # 新增了 QHBoxLayout, QLineEdit, QPushButton, QMessageBox
from PySide6.QtCore import Qt
from core.database import db
import os
import sys
import importlib


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("模块化 Python 项目框架")
        self.resize(1000, 600)

        # --- 核心布局设置 ---

        # 1. 创建中央区域（标签页容器 - 满足需求 4）
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # 2. 创建常驻全局数据窗口（侧边栏 - 满足需求 5）
        self.setup_global_dock()

        # 3. 动态加载插件（满足需求 3）
        self.load_plugins()

    def setup_global_dock(self):
        """
        设置顶部常驻全局数据栏，包含输入和修改功能
        """
        self.global_dock = QDockWidget("全局项目配置", self)

        # 1. 设置允许停靠的区域（这里限制只能在顶部或底部，防止用户拖到左右两边导致布局崩坏）
        self.global_dock.setAllowedAreas(Qt.TopDockWidgetArea | Qt.BottomDockWidgetArea)
        # 禁止浮动（可选，看你喜好，禁止浮动会让界面更稳固）
        self.global_dock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)

        # 2. 创建容器和水平布局 (Horizontal Layout)
        dock_content = QWidget()
        layout = QHBoxLayout()  # 注意这里改成了 QHBoxLayout，让控件横向排列
        layout.setContentsMargins(10, 5, 10, 5)  # 设置一点边距，不让控件贴边

        # --- 控件定义 ---

        # 项目名称输入
        layout.addWidget(QLabel("当前项目:"))
        self.input_project_name = QLineEdit()
        self.input_project_name.setPlaceholderText("请输入项目名称...")
        self.input_project_name.setText("未命名项目")  # 默认值
        layout.addWidget(self.input_project_name)

        # 操作员输入
        layout.addWidget(QLabel("操作员:"))
        self.input_operator = QLineEdit()
        self.input_operator.setPlaceholderText("请输入姓名...")
        self.input_operator.setFixedWidth(100)  # 限制宽度，因为名字通常不长
        layout.addWidget(self.input_operator)

        # 批次号（模拟一个不可修改的只读数据，比如自动生成的ID）
        layout.addWidget(QLabel("批次ID:"))
        self.lbl_batch_id = QLineEdit("2023-BATCH-001")
        self.lbl_batch_id.setReadOnly(True)  # 设置为只读
        self.lbl_batch_id.setStyleSheet("background-color: #e0e0e0; color: #555;")  # 变灰显示
        self.lbl_batch_id.setFixedWidth(120)
        layout.addWidget(self.lbl_batch_id)

        # 保存/更新按钮
        self.btn_update_global = QPushButton("更新配置")
        # 绑定点击事件到下面新写的函数
        self.btn_update_global.clicked.connect(self.on_global_data_update)
        layout.addWidget(self.btn_update_global)

        # 弹簧（Spacer）：把上面的控件都顶到左边，防止它们分散在整个长条里
        layout.addStretch()

        # 3. 应用布局
        dock_content.setLayout(layout)
        self.global_dock.setWidget(dock_content)

        # 4. 关键修改：将 Dock 放置在窗口顶部 (TopDockWidgetArea)
        self.addDockWidget(Qt.TopDockWidgetArea, self.global_dock)

    def on_global_data_update(self):
        """
        当用户点击“更新配置”按钮时触发
        """
        # 1. 获取输入框的内容
        project_name = self.input_project_name.text()
        operator = self.input_operator.text()

        # 2. 简单的校验
        if not project_name or not operator:
            QMessageBox.warning(self, "警告", "项目名称和操作员不能为空！")
            return

        # 3. (可选) 存入数据库
        # 这里演示如何利用之前写的 db 模块更新数据
        try:
            # 假设我们在数据库里建一个 global_config 表（这里只是演示逻辑）
            # 实际使用中，你可以在 database.py 里建表
            print(f"正在保存全局数据 -> 项目: {project_name}, 操作员: {operator}")

            # 为了演示，我们只往之前的 system_logs 表插一条记录证明修改成功
            db.execute_query(
                "INSERT INTO system_logs (message) VALUES (?)",
                (f"全局配置更新: 项目设为 {project_name}, 操作员设为 {operator}",)
            )

            QMessageBox.information(self, "成功", "全局配置已更新并保存到数据库！")

        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存失败: {e}")

    def load_plugins(self):
        """自动扫描 plugins 文件夹并加载功能"""
        plugin_folder = "plugins"

        # 遍历 plugins 目录下的所有文件
        for filename in os.listdir(plugin_folder):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = filename[:-3]  # 去掉 .py 后缀

                try:
                    # 动态导入模块
                    module = importlib.import_module(f"{plugin_folder}.{module_name}")

                    # 检查模块里是否有 plugin_class 变量
                    if hasattr(module, 'plugin_class'):
                        plugin_instance = module.plugin_class()
                        # 添加到标签页
                        self.tabs.addTab(plugin_instance, plugin_instance.get_name())
                        print(f"插件加载成功: {module_name}")
                except Exception as e:
                    print(f"插件 {module_name} 加载失败: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 设置样式表，让界面看起来更成熟（满足需求 1）
    app.setStyleSheet("""
        QMainWindow { background-color: #f0f0f0; }
        QTabWidget::pane { border: 1px solid #C2C7CB; }
        QTabBar::tab { background: #E1E1E1; padding: 10px; }
        QTabBar::tab:selected { background: white; }
    """)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())