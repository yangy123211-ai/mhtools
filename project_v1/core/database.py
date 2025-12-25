import sqlite3
import os

class DatabaseManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            # 初始化数据库连接
            cls._instance.conn = sqlite3.connect("app_data.db")
            cls._instance.cursor = cls._instance.conn.cursor()
            cls._instance.init_db()
        return cls._instance

    def init_db(self):
        """初始化基础表结构"""
        # 示例：创建一个日志表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def execute_query(self, query, params=()):
        """统一执行查询"""
        self.cursor.execute(query, params)
        self.conn.commit()
        return self.cursor

# 全局引用
db = DatabaseManager()