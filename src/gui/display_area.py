import tkinter as tk
from tkinter import ttk, scrolledtext
from tkinter import messagebox
from ..core.global_vars import g_vars
from .chart_widget import ChartWidget
import time

class DisplayArea(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="数据显示")
        
        # 报警状态跟踪
        self.alarm_states = {
            'temp_high': False,    # 温度过高报警状态
            'temp_low': False,     # 温度过低报警状态
            'humidity_high': False, # 湿度过高报警状态
            'humidity_low': False   # 湿度过低报警状态
        }
        self.last_alarm_time = 0   # 上次报警时间
        self.alarm_cooldown = 30   # 报警冷却时间（秒）
        
        self.setup_display()
        
    def setup_display(self):
        # 创建数据显示区域（限制高度）
        text_frame = ttk.LabelFrame(self, text="数据显示")
        text_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.text_display = scrolledtext.ScrolledText(text_frame, width=80, height=8, wrap=tk.WORD)
        self.text_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 创建信息显示区域（水平排列）
        info_frame = ttk.Frame(self)
        info_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 左侧：报警阈值显示
        self.alarm_info_frame = ttk.LabelFrame(info_frame, text="当前报警阈值")
        self.alarm_info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        self.setup_alarm_info()
        
        # 中间：报警状态显示
        self.alarm_status_frame = ttk.LabelFrame(info_frame, text="报警状态")
        self.alarm_status_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.setup_alarm_status()
        
        # 右侧：统计信息显示
        self.stats_frame = ttk.LabelFrame(info_frame, text="数据统计")
        self.stats_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        self.setup_stats_display()
        
        # 创建图表区域（占据剩余空间）
        chart_container = ttk.LabelFrame(self, text="实时数据图表")
        chart_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.chart_widget = ChartWidget(chart_container)
        self.chart_widget.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
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
        
        # 配置状态显示
        status_frame = ttk.Frame(self.alarm_info_frame)
        status_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(status_frame, text="配置状态:").pack(side=tk.LEFT)
        self.config_status_label = ttk.Label(status_frame, text="", foreground="green")
        self.config_status_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # 更新阈值显示
        self.update_alarm_info()
        
    def update_alarm_info(self):
        """更新报警阈值信息显示"""
        alarm_config = g_vars.config.get('alarm', {})
        temp_text = f"{alarm_config.get('temp_low', 0)}°C ~ {alarm_config.get('temp_high', 40)}°C"
        humidity_text = f"{alarm_config.get('humidity_low', 10)}% ~ {alarm_config.get('humidity_high', 90)}%"
        
        self.temp_threshold_label.config(text=temp_text)
        self.humidity_threshold_label.config(text=humidity_text)
        
        # 更新配置状态
        from datetime import datetime
        status_text = f"已更新 ({datetime.now().strftime('%H:%M:%S')})"
        self.config_status_label.config(text=status_text)
        
    def setup_alarm_status(self):
        """设置报警状态显示"""
        # 温度报警状态
        temp_status_frame = ttk.Frame(self.alarm_status_frame)
        temp_status_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(temp_status_frame, text="温度状态:").pack(side=tk.LEFT)
        self.temp_status_label = ttk.Label(temp_status_frame, text="正常", foreground="green")
        self.temp_status_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # 湿度报警状态
        humidity_status_frame = ttk.Frame(self.alarm_status_frame)
        humidity_status_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(humidity_status_frame, text="湿度状态:").pack(side=tk.LEFT)
        self.humidity_status_label = ttk.Label(humidity_status_frame, text="正常", foreground="green")
        self.humidity_status_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # 重置报警状态按钮
        reset_frame = ttk.Frame(self.alarm_status_frame)
        reset_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.reset_alarm_btn = ttk.Button(reset_frame, text="重置报警状态", command=self.reset_alarm_states)
        self.reset_alarm_btn.pack(side=tk.RIGHT)
        
    def update_alarm_status_display(self):
        """更新报警状态显示"""
        # 更新温度状态
        if self.alarm_states['temp_high'] or self.alarm_states['temp_low']:
            self.temp_status_label.config(text="报警", foreground="red")
        else:
            self.temp_status_label.config(text="正常", foreground="green")
            
        # 更新湿度状态
        if self.alarm_states['humidity_high'] or self.alarm_states['humidity_low']:
            self.humidity_status_label.config(text="报警", foreground="red")
        else:
            self.humidity_status_label.config(text="正常", foreground="green")
        
    def update_display(self, data):
        display_text = (f"时间: {data['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}\n"
                       f"温度: {data['temperature']:.2f}°C\n"
                       f"湿度: {data['humidity']:.2f}%\n"
                       f"其他值: {data['other_value']:.2f}\n"
                       f"{'='*50}\n")
        
        self.text_display.insert(tk.END, display_text)
        self.text_display.see(tk.END)
        
        # 更新图表
        self.chart_widget.add_data_point(data)
        
        # 更新统计信息
        self.update_stats_display()
        
    def check_alarm_conditions(self, data):
        """检查报警条件，防止重复弹窗"""
        alarm_config = g_vars.config.get('alarm', {})
        current_time = time.time()
        new_alarms = []
        
        # 检查温度报警
        temp_high_threshold = alarm_config.get('temp_high', 40)
        temp_low_threshold = alarm_config.get('temp_low', 0)
        
        if data['temperature'] > temp_high_threshold:
            if not self.alarm_states['temp_high']:
                new_alarms.append(f"温度过高: {data['temperature']:.2f}°C")
                self.alarm_states['temp_high'] = True
        else:
            # 温度恢复正常，重置报警状态
            self.alarm_states['temp_high'] = False
            
        if data['temperature'] < temp_low_threshold:
            if not self.alarm_states['temp_low']:
                new_alarms.append(f"温度过低: {data['temperature']:.2f}°C")
                self.alarm_states['temp_low'] = True
        else:
            # 温度恢复正常，重置报警状态
            self.alarm_states['temp_low'] = False
        
        # 检查湿度报警
        humidity_high_threshold = alarm_config.get('humidity_high', 90)
        humidity_low_threshold = alarm_config.get('humidity_low', 10)
        
        if data['humidity'] > humidity_high_threshold:
            if not self.alarm_states['humidity_high']:
                new_alarms.append(f"湿度过高: {data['humidity']:.2f}%")
                self.alarm_states['humidity_high'] = True
        else:
            # 湿度恢复正常，重置报警状态
            self.alarm_states['humidity_high'] = False
            
        if data['humidity'] < humidity_low_threshold:
            if not self.alarm_states['humidity_low']:
                new_alarms.append(f"湿度过低: {data['humidity']:.2f}%")
                self.alarm_states['humidity_low'] = True
        else:
            # 湿度恢复正常，重置报警状态
            self.alarm_states['humidity_low'] = False
        
        # 检查是否有新的报警，并且距离上次报警时间超过冷却时间
        if new_alarms and (current_time - self.last_alarm_time) > self.alarm_cooldown:
            self.last_alarm_time = current_time
            self.show_alarm_dialog(new_alarms)
        
        # 更新报警状态显示
        self.update_alarm_status_display()
        
    def show_alarm_dialog(self, alarms):
        """显示报警对话框"""
        alarm_text = "\n".join(alarms)
        messagebox.showwarning("报警", f"{alarm_text}\n\n注意：相同报警在30秒内不会重复弹出")
        
    def reset_alarm_states(self):
        """重置所有报警状态"""
        for key in self.alarm_states:
            self.alarm_states[key] = False
        self.last_alarm_time = 0
        self.update_alarm_status_display()
        
    def setup_stats_display(self):
        """设置统计信息显示"""
        # 温度统计
        temp_stats_frame = ttk.Frame(self.stats_frame)
        temp_stats_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(temp_stats_frame, text="温度统计:").pack(side=tk.LEFT)
        self.temp_stats_label = ttk.Label(temp_stats_frame, text="暂无数据", foreground="gray")
        self.temp_stats_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # 湿度统计
        humidity_stats_frame = ttk.Frame(self.stats_frame)
        humidity_stats_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(humidity_stats_frame, text="湿度统计:").pack(side=tk.LEFT)
        self.humidity_stats_label = ttk.Label(humidity_stats_frame, text="暂无数据", foreground="gray")
        self.humidity_stats_label.pack(side=tk.LEFT, padx=(5, 0))
        
    def update_stats_display(self):
        """更新统计信息显示"""
        stats = self.chart_widget.get_statistics()
        if stats:
            # 更新温度统计
            temp_text = f"平均: {stats['temp_avg']:.2f}°C, 最高: {stats['temp_max']:.2f}°C, 最低: {stats['temp_min']:.2f}°C"
            self.temp_stats_label.config(text=temp_text, foreground="black")
            
            # 更新湿度统计
            humidity_text = f"平均: {stats['humidity_avg']:.2f}%, 最高: {stats['humidity_max']:.2f}%, 最低: {stats['humidity_min']:.2f}%"
            self.humidity_stats_label.config(text=humidity_text, foreground="black")
        else:
            self.temp_stats_label.config(text="暂无数据", foreground="gray")
            self.humidity_stats_label.config(text="暂无数据", foreground="gray") 