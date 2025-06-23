import tkinter as tk
from tkinter import ttk, scrolledtext
from tkinter import messagebox
from ..core.global_vars import g_vars

class DisplayArea(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="数据显示")
        self.setup_display()
        
    def setup_display(self):
        # 创建数据显示区域
        self.text_display = scrolledtext.ScrolledText(self, width=80, height=20, wrap=tk.WORD)
        self.text_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 创建报警阈值显示区域
        self.alarm_info_frame = ttk.LabelFrame(self, text="当前报警阈值")
        self.alarm_info_frame.pack(fill=tk.X, padx=5, pady=5)
        self.setup_alarm_info()
        
        # 创建图表区域（预留）
        self.chart_frame = ttk.LabelFrame(self, text="实时数据图表")
        self.chart_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
    def setup_alarm_info(self):
        """设置报警阈值信息显示"""
        # 温度阈值显示
        temp_frame = ttk.Frame(self.alarm_info_frame)
        temp_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(temp_frame, text="温度阈值:").pack(side=tk.LEFT)
        self.temp_threshold_label = ttk.Label(temp_frame, text="", foreground="blue")
        self.temp_threshold_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # 湿度阈值显示
        humidity_frame = ttk.Frame(self.alarm_info_frame)
        humidity_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(humidity_frame, text="湿度阈值:").pack(side=tk.LEFT)
        self.humidity_threshold_label = ttk.Label(humidity_frame, text="", foreground="blue")
        self.humidity_threshold_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # 更新阈值显示
        self.update_alarm_info()
        
    def update_alarm_info(self):
        """更新报警阈值信息显示"""
        alarm_config = g_vars.config.get('alarm', {})
        temp_text = f"{alarm_config.get('temp_low', 0)}°C ~ {alarm_config.get('temp_high', 40)}°C"
        humidity_text = f"{alarm_config.get('humidity_low', 10)}% ~ {alarm_config.get('humidity_high', 90)}%"
        
        self.temp_threshold_label.config(text=temp_text)
        self.humidity_threshold_label.config(text=humidity_text)
        
    def update_display(self, data):
        display_text = (f"时间: {data['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}\n"
                       f"温度: {data['temperature']:.2f}°C\n"
                       f"湿度: {data['humidity']:.2f}%\n"
                       f"其他值: {data['other_value']:.2f}\n"
                       f"{'='*50}\n")
        
        self.text_display.insert(tk.END, display_text)
        self.text_display.see(tk.END)
        
    def check_alarm_conditions(self, data):
        alarm_config = g_vars.config.get('alarm', {})
        alarms = []
        
        if data['temperature'] > alarm_config.get('temp_high', 40):
            alarms.append(f"温度过高: {data['temperature']:.2f}°C")
        elif data['temperature'] < alarm_config.get('temp_low', 0):
            alarms.append(f"温度过低: {data['temperature']:.2f}°C")
            
        if data['humidity'] > alarm_config.get('humidity_high', 90):
            alarms.append(f"湿度过高: {data['humidity']:.2f}%")
        elif data['humidity'] < alarm_config.get('humidity_low', 10):
            alarms.append(f"湿度过低: {data['humidity']:.2f}%")
            
        if alarms:
            messagebox.showwarning("报警", "\n".join(alarms)) 