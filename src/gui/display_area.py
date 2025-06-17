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
        
        # 创建图表区域（预留）
        self.chart_frame = ttk.LabelFrame(self, text="实时数据图表")
        self.chart_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
    def update_display(self, data):
        display_text = (f"时间: {data['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}\n"
                       f"温度: {data['temperature']:.2f}°C\n"
                       f"湿度: {data['humidity']:.2f}%\n"
                       f"其他值: {data['other_value']:.2f}\n"
                       f"{'='*50}\n")
        
        self.text_display.insert(tk.END, display_text)
        self.text_display.see(tk.END)
        
    def check_alarm_conditions(self, data):
        alarm_config = g_vars.config['alarm']
        alarms = []
        
        if data['temperature'] > alarm_config['temp_high']:
            alarms.append(f"温度过高: {data['temperature']:.2f}°C")
        elif data['temperature'] < alarm_config['temp_low']:
            alarms.append(f"温度过低: {data['temperature']:.2f}°C")
            
        if data['humidity'] > alarm_config['humidity_high']:
            alarms.append(f"湿度过高: {data['humidity']:.2f}%")
        elif data['humidity'] < alarm_config['humidity_low']:
            alarms.append(f"湿度过低: {data['humidity']:.2f}%")
            
        if alarms:
            messagebox.showwarning("报警", "\n".join(alarms)) 