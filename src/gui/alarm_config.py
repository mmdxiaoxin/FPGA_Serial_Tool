import tkinter as tk
from tkinter import ttk, messagebox
from ..core.global_vars import g_vars
import json
import os

class AlarmConfigDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("报警阈值配置")
        self.geometry("400x300")
        self.resizable(False, False)
        
        # 设置模态对话框
        self.transient(parent)
        self.grab_set()
        
        self.setup_ui()
        self.load_current_config()
        
    def setup_ui(self):
        # 主框架
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = ttk.Label(main_frame, text="报警阈值设置", font=("Arial", 14, "bold"))
        title_label.pack(pady=(0, 20))
        
        # 温度设置框架
        temp_frame = ttk.LabelFrame(main_frame, text="温度报警阈值", padding="10")
        temp_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 温度高阈值
        ttk.Label(temp_frame, text="温度高阈值 (°C):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.temp_high_var = tk.DoubleVar()
        self.temp_high_entry = ttk.Entry(temp_frame, textvariable=self.temp_high_var, width=15)
        self.temp_high_entry.grid(row=0, column=1, padx=(10, 0), pady=5)
        
        # 温度低阈值
        ttk.Label(temp_frame, text="温度低阈值 (°C):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.temp_low_var = tk.DoubleVar()
        self.temp_low_entry = ttk.Entry(temp_frame, textvariable=self.temp_low_var, width=15)
        self.temp_low_entry.grid(row=1, column=1, padx=(10, 0), pady=5)
        
        # 湿度设置框架
        humidity_frame = ttk.LabelFrame(main_frame, text="湿度报警阈值", padding="10")
        humidity_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 湿度高阈值
        ttk.Label(humidity_frame, text="湿度高阈值 (%):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.humidity_high_var = tk.DoubleVar()
        self.humidity_high_entry = ttk.Entry(humidity_frame, textvariable=self.humidity_high_var, width=15)
        self.humidity_high_entry.grid(row=0, column=1, padx=(10, 0), pady=5)
        
        # 湿度低阈值
        ttk.Label(humidity_frame, text="湿度低阈值 (%):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.humidity_low_var = tk.DoubleVar()
        self.humidity_low_entry = ttk.Entry(humidity_frame, textvariable=self.humidity_low_var, width=15)
        self.humidity_low_entry.grid(row=1, column=1, padx=(10, 0), pady=5)
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        # 保存按钮
        self.save_btn = ttk.Button(button_frame, text="保存", command=self.save_config)
        self.save_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # 取消按钮
        self.cancel_btn = ttk.Button(button_frame, text="取消", command=self.destroy)
        self.cancel_btn.pack(side=tk.RIGHT)
        
        # 重置按钮
        self.reset_btn = ttk.Button(button_frame, text="重置默认值", command=self.reset_to_default)
        self.reset_btn.pack(side=tk.LEFT)
        
    def load_current_config(self):
        """加载当前配置"""
        alarm_config = g_vars.config.get('alarm', {})
        self.temp_high_var.set(alarm_config.get('temp_high', 40))
        self.temp_low_var.set(alarm_config.get('temp_low', 0))
        self.humidity_high_var.set(alarm_config.get('humidity_high', 90))
        self.humidity_low_var.set(alarm_config.get('humidity_low', 10))
        
    def validate_inputs(self):
        """验证输入值"""
        try:
            temp_high = self.temp_high_var.get()
            temp_low = self.temp_low_var.get()
            humidity_high = self.humidity_high_var.get()
            humidity_low = self.humidity_low_var.get()
            
            # 检查温度范围
            if temp_high <= temp_low:
                messagebox.showerror("错误", "温度高阈值必须大于温度低阈值")
                return False
                
            # 检查湿度范围
            if humidity_high <= humidity_low:
                messagebox.showerror("错误", "湿度高阈值必须大于湿度低阈值")
                return False
                
            # 检查湿度百分比范围
            if humidity_high > 100 or humidity_low < 0:
                messagebox.showerror("错误", "湿度值必须在0-100%之间")
                return False
                
            return True
            
        except tk.TclError:
            messagebox.showerror("错误", "请输入有效的数值")
            return False
            
    def save_config(self):
        """保存配置"""
        if not self.validate_inputs():
            return
            
        # 更新配置
        g_vars.config['alarm'] = {
            'temp_high': self.temp_high_var.get(),
            'temp_low': self.temp_low_var.get(),
            'humidity_high': self.humidity_high_var.get(),
            'humidity_low': self.humidity_low_var.get()
        }
        
        # 保存到文件
        config_path = os.path.join(g_vars.root_dir, 'config', 'config.json')
        try:
            with open(config_path, 'w') as f:
                json.dump(g_vars.config, f, indent=4)
            messagebox.showinfo("成功", "报警阈值配置已保存")
            self.destroy()
        except Exception as e:
            messagebox.showerror("错误", f"保存配置失败: {e}")
            
    def reset_to_default(self):
        """重置为默认值"""
        self.temp_high_var.set(40)
        self.temp_low_var.set(0)
        self.humidity_high_var.set(90)
        self.humidity_low_var.set(10) 