import json
import queue
import os
from cryptography.fernet import Fernet

class GlobalVars:
    def __init__(self):
        self.serial_port = None
        self.is_serial_open = False
        self.buffer = bytearray()
        self.data_queue = queue.Queue()
        self.is_running = True
        
        # 获取项目根目录
        self.root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.config = self.load_config()
        self.encryption_key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.encryption_key)
        
    def load_config(self):
        config_path = os.path.join(self.root_dir, 'config', 'config.json')
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # 确保配置目录存在
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            
            default_config = {
                'serial': {
                    'port': 'COM5',
                    'baud_rate': 115200,
                    'timeout': 1
                },
                'display': {
                    'update_interval': 1000,
                    'max_data_points': 1000
                },
                'storage': {
                    'db_path': os.path.join(self.root_dir, 'data', 'temperature_data.db'),
                    'backup_interval': 3600
                },
                'alarm': {
                    'temp_high': 40,
                    'temp_low': 0,
                    'humidity_high': 90,
                    'humidity_low': 10
                }
            }
            with open(config_path, 'w') as f:
                json.dump(default_config, f, indent=4)
            return default_config

# 创建全局变量实例
g_vars = GlobalVars() 