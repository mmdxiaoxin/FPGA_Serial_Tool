import sqlite3
import logging
from datetime import datetime
from .global_vars import g_vars
import os

class DataStorage:
    def __init__(self):
        self.db_path = os.path.join(g_vars.app_data_dir, 'data', 'temperature_data.db')
        self.init_database()
        
    def init_database(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS temperature_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME,
                    temperature REAL,
                    humidity REAL,
                    other_value REAL
                )
            ''')
            conn.commit()
            conn.close()
            logging.info("数据库初始化成功")
        except Exception as e:
            logging.error(f"数据库初始化失败: {e}")
            
    def save_data(self, temperature, humidity, other_value):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO temperature_data (timestamp, temperature, humidity, other_value)
                VALUES (?, ?, ?, ?)
            ''', (datetime.now(), temperature, humidity, other_value))
            conn.commit()
            conn.close()
        except Exception as e:
            logging.error(f"保存数据失败: {e}")
            
    def get_historical_data(self, limit=1000):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT timestamp, temperature, humidity, other_value
                FROM temperature_data
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,))
            data = cursor.fetchall()
            conn.close()
            return data
        except Exception as e:
            logging.error(f"获取历史数据失败: {e}")
            return [] 