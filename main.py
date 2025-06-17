# -*- coding: utf-8 -*-
"""
FPGA声学测温系统
"""

import logging
import os
from src.core.global_vars import GlobalVars
from src.core.serial_comm import SerialCommunication
from src.core.data_storage import DataStorage
from src.core.data_processor import DataProcessor
from src.core.system_monitor import SystemMonitor
from src.core.security import SecurityManager
from src.gui.main_window import MainWindow

# 获取项目根目录
root_dir = os.path.dirname(os.path.abspath(__file__))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(root_dir, 'logs', 'system.log')),
        logging.StreamHandler()
    ]
)

def main():
    # 初始化全局变量
    g_vars = GlobalVars()
    
    # 初始化各个模块
    serial_comm = SerialCommunication()
    data_storage = DataStorage()
    data_processor = DataProcessor()
    system_monitor = SystemMonitor()
    security_manager = SecurityManager()
    
    # 创建并运行主窗口
    app = MainWindow(serial_comm, data_storage, data_processor, system_monitor, security_manager)
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()

if __name__ == "__main__":
    main()