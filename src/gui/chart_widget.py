import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import numpy as np

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

class ChartWidget(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # 数据存储
        self.timestamps = []
        self.temperatures = []
        self.humidities = []
        self.other_values = []
        
        # 图表配置
        self.max_data_points = 100  # 最大显示数据点
        self.update_interval = 1000  # 更新间隔（毫秒）
        
        self.setup_chart()
        
    def setup_chart(self):
        """设置图表"""
        # 创建matplotlib图形（调整尺寸以适应新布局）
        self.fig = Figure(figsize=(12, 8), dpi=100)
        self.fig.patch.set_facecolor('#f0f0f0')
        
        # 创建子图
        self.ax1 = self.fig.add_subplot(211)  # 温度图表
        self.ax2 = self.fig.add_subplot(212)  # 湿度图表
        
        # 设置图表样式
        self.setup_plot_style()
        
        # 创建画布
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # 创建控制按钮
        self.setup_controls()
        
    def setup_plot_style(self):
        """设置图表样式"""
        # 温度图表
        self.ax1.set_title('Temperature Curve', fontsize=12, fontweight='bold')
        self.ax1.set_ylabel('Temperature (°C)', fontsize=10)
        self.ax1.grid(True, alpha=0.3)
        self.ax1.set_facecolor('#f8f8f8')
        
        # 湿度图表
        self.ax2.set_title('Humidity Curve', fontsize=12, fontweight='bold')
        self.ax2.set_ylabel('Humidity (%)', fontsize=10)
        self.ax2.set_xlabel('Time', fontsize=10)
        self.ax2.grid(True, alpha=0.3)
        self.ax2.set_facecolor('#f8f8f8')
        
        # 调整子图间距
        self.fig.tight_layout()
        
    def setup_controls(self):
        """设置控制按钮"""
        control_frame = ttk.Frame(self)
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 清除数据按钮
        self.clear_btn = ttk.Button(control_frame, text="清除图表", command=self.clear_chart)
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        # 保存图表按钮
        self.save_btn = ttk.Button(control_frame, text="保存图表", command=self.save_chart)
        self.save_btn.pack(side=tk.LEFT, padx=5)
        
        # 数据点数量显示
        self.data_count_label = ttk.Label(control_frame, text="数据点: 0")
        self.data_count_label.pack(side=tk.RIGHT, padx=5)
        
    def add_data_point(self, data):
        """添加数据点"""
        timestamp = data['timestamp']
        
        # 添加新数据点
        self.timestamps.append(timestamp)
        self.temperatures.append(data['temperature'])
        self.humidities.append(data['humidity'])
        self.other_values.append(data['other_value'])
        
        # 限制数据点数量
        if len(self.timestamps) > self.max_data_points:
            self.timestamps.pop(0)
            self.temperatures.pop(0)
            self.humidities.pop(0)
            self.other_values.pop(0)
        
        # 更新图表
        self.update_chart()
        
        # 更新数据点计数
        self.data_count_label.config(text=f"数据点: {len(self.timestamps)}")
        
    def update_chart(self):
        """更新图表"""
        if not self.timestamps:
            return
            
        # 清除旧图表
        self.ax1.clear()
        self.ax2.clear()
        
        # 设置图表样式
        self.setup_plot_style()
        
        # 绘制温度曲线
        self.ax1.plot(self.timestamps, self.temperatures, 'r-', linewidth=2, label='Temperature')
        self.ax1.scatter(self.timestamps, self.temperatures, color='red', s=20, alpha=0.7)
        
        # 添加温度阈值线
        from ..core.global_vars import g_vars
        alarm_config = g_vars.config.get('alarm', {})
        temp_high = alarm_config.get('temp_high', 40)
        temp_low = alarm_config.get('temp_low', 0)
        
        if self.timestamps:
            self.ax1.axhline(y=temp_high, color='orange', linestyle='--', alpha=0.7, label=f'High Temp: {temp_high}°C')
            self.ax1.axhline(y=temp_low, color='blue', linestyle='--', alpha=0.7, label=f'Low Temp: {temp_low}°C')
        
        self.ax1.legend()
        
        # 绘制湿度曲线
        self.ax2.plot(self.timestamps, self.humidities, 'b-', linewidth=2, label='Humidity')
        self.ax2.scatter(self.timestamps, self.humidities, color='blue', s=20, alpha=0.7)
        
        # 添加湿度阈值线
        humidity_high = alarm_config.get('humidity_high', 90)
        humidity_low = alarm_config.get('humidity_low', 10)
        
        if self.timestamps:
            self.ax2.axhline(y=humidity_high, color='orange', linestyle='--', alpha=0.7, label=f'High Humidity: {humidity_high}%')
            self.ax2.axhline(y=humidity_low, color='blue', linestyle='--', alpha=0.7, label=f'Low Humidity: {humidity_low}%')
        
        self.ax2.legend()
        
        # 格式化时间轴
        if len(self.timestamps) > 1:
            time_range = max(self.timestamps) - min(self.timestamps)
            if time_range.total_seconds() > 3600:  # 超过1小时
                self.ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
            else:
                self.ax2.xaxis.set_major_formatter(mdates.DateFormatter('%M:%S'))
            
            self.ax2.xaxis.set_major_locator(mdates.AutoDateLocator())
        
        # 自动调整y轴范围
        if self.temperatures:
            temp_margin = (max(self.temperatures) - min(self.temperatures)) * 0.1
            self.ax1.set_ylim(min(self.temperatures) - temp_margin, max(self.temperatures) + temp_margin)
        
        if self.humidities:
            hum_margin = (max(self.humidities) - min(self.humidities)) * 0.1
            self.ax2.set_ylim(min(self.humidities) - hum_margin, max(self.humidities) + hum_margin)
        
        # 刷新画布
        self.canvas.draw()
        
    def clear_chart(self):
        """清除图表数据"""
        self.timestamps.clear()
        self.temperatures.clear()
        self.humidities.clear()
        self.other_values.clear()
        
        # 清除图表
        self.ax1.clear()
        self.ax2.clear()
        self.setup_plot_style()
        self.canvas.draw()
        
        # 更新计数
        self.data_count_label.config(text="数据点: 0")
        
    def save_chart(self):
        """保存图表"""
        try:
            from datetime import datetime
            filename = f"temperature_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            self.fig.savefig(filename, dpi=300, bbox_inches='tight')
            
            import tkinter.messagebox as messagebox
            messagebox.showinfo("保存成功", f"图表已保存为: {filename}")
        except Exception as e:
            import tkinter.messagebox as messagebox
            messagebox.showerror("保存失败", f"保存图表时发生错误: {e}")
            
    def get_statistics(self):
        """获取统计信息"""
        if not self.temperatures or not self.humidities:
            return None
            
        return {
            'temp_avg': np.mean(self.temperatures),
            'temp_max': np.max(self.temperatures),
            'temp_min': np.min(self.temperatures),
            'humidity_avg': np.mean(self.humidities),
            'humidity_max': np.max(self.humidities),
            'humidity_min': np.min(self.humidities),
            'data_points': len(self.timestamps)
        } 