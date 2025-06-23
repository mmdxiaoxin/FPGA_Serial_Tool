import tkinter as tk
from tkinter import ttk
import threading
import time
import logging
from ..core.global_vars import g_vars
from .serial_controls import SerialControls
from .display_area import DisplayArea

class MainWindow(tk.Tk):
    def __init__(self, serial_comm, data_storage, data_processor, system_monitor, security_manager):
        super().__init__()
        
        self.title("FPGA声学测温系统")
        self.geometry("1400x900")
        
        # 初始化组件
        self.serial_comm = serial_comm
        self.data_storage = data_storage
        self.data_processor = data_processor
        self.system_monitor = system_monitor
        self.security_manager = security_manager
        
        self.setup_gui()
        self.start_data_thread()
        
    def setup_gui(self):
        # 创建主框架
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建左侧控制面板（固定宽度）
        self.control_frame = SerialControls(self.main_frame, self.serial_comm, self.security_manager, self)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10), pady=5)
        
        # 创建右侧滚动区域
        self.right_frame = ttk.Frame(self.main_frame)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 创建画布和滚动条
        self.canvas = tk.Canvas(self.right_frame)
        self.scrollbar = ttk.Scrollbar(self.right_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # 创建右侧数据显示区域
        self.display_frame = DisplayArea(self.scrollable_frame)
        self.display_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 布局画布和滚动条
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # 绑定鼠标滚轮事件
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # 状态栏
        self.setup_status_bar()
        
    def setup_status_bar(self):
        self.status_bar = ttk.Label(self, text="就绪", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def refresh_alarm_display(self):
        """刷新报警阈值显示"""
        self.display_frame.update_alarm_info()
        
    def start_data_thread(self):
        def read_serial_data():
            while g_vars.is_running:
                if g_vars.is_serial_open and g_vars.serial_port:
                    try:
                        if g_vars.serial_port.in_waiting:
                            data = g_vars.serial_port.read(g_vars.serial_port.in_waiting)
                            g_vars.buffer.extend(data)
                            
                            while b'\x0D\x0A' in g_vars.buffer:
                                end_index = g_vars.buffer.find(b'\x0D\x0A')
                                packet = g_vars.buffer[:end_index]
                                
                                processed_data = self.data_processor.process_data(packet)
                                if processed_data:
                                    # 存储数据
                                    self.data_storage.save_data(
                                        processed_data['temperature'],
                                        processed_data['humidity'],
                                        processed_data['other_value']
                                    )
                                    
                                    # 更新显示
                                    self.display_frame.update_display(processed_data)
                                    
                                    # 更新系统监控
                                    self.system_monitor.update_stats(True)
                                    
                                    # 检查报警条件
                                    self.display_frame.check_alarm_conditions(processed_data)
                                else:
                                    self.system_monitor.update_stats(False)
                                    
                                g_vars.buffer = g_vars.buffer[end_index + 2:]
                    except Exception as e:
                        logging.error(f"读取数据错误: {e}")
                        self.system_monitor.update_stats(False)
                time.sleep(0.01)
                
        self.data_thread = threading.Thread(target=read_serial_data, daemon=True)
        self.data_thread.start()
        
    def on_closing(self):
        g_vars.is_running = False
        if g_vars.is_serial_open:
            self.serial_comm.close_port()
        self.destroy()

    def _on_mousewheel(self, event):
        """处理鼠标滚轮事件"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units") 