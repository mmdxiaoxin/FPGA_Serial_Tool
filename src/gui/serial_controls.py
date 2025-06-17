import tkinter as tk
from tkinter import ttk, messagebox
from ..core.global_vars import g_vars

class SerialControls(ttk.LabelFrame):
    def __init__(self, parent, serial_comm, security_manager):
        super().__init__(parent, text="串口控制")
        self.serial_comm = serial_comm
        self.security_manager = security_manager
        self.setup_controls()
        
    def setup_controls(self):
        # 串口选择
        ttk.Label(self, text="串口:").pack(pady=5)
        self.port_var = tk.StringVar()
        self.port_combo = ttk.Combobox(self, textvariable=self.port_var)
        self.port_combo['values'] = self.serial_comm.available_ports
        self.port_combo.pack(pady=5)
        
        # 波特率选择
        ttk.Label(self, text="波特率:").pack(pady=5)
        self.baud_var = tk.StringVar(value=str(g_vars.config['serial']['baud_rate']))
        self.baud_combo = ttk.Combobox(self, textvariable=self.baud_var)
        self.baud_combo['values'] = ['9600', '19200', '38400', '57600', '115200']
        self.baud_combo.pack(pady=5)
        
        # 串口控制按钮
        self.btn_toggle_serial = ttk.Button(self, text="打开串口", command=self.toggle_serial)
        self.btn_toggle_serial.pack(pady=10)
        
        # 数据发送区域
        ttk.Label(self, text="发送数据:").pack(pady=5)
        self.entry_send = ttk.Entry(self, width=30)
        self.entry_send.pack(pady=5)
        self.btn_send = ttk.Button(self, text="发送", command=self.send_data)
        self.btn_send.pack(pady=5)
        
    def toggle_serial(self):
        if not g_vars.is_serial_open:
            port = self.port_var.get()
            baud_rate = int(self.baud_var.get())
            if self.serial_comm.open_port(port, baud_rate, g_vars.config['serial']['timeout']):
                self.btn_toggle_serial.config(text="关闭串口")
                self.security_manager.log_operation("串口操作", f"打开串口 {port}")
            else:
                messagebox.showerror("错误", "打开串口失败")
        else:
            self.serial_comm.close_port()
            self.btn_toggle_serial.config(text="打开串口")
            self.security_manager.log_operation("串口操作", "关闭串口")
            
    def send_data(self):
        data = self.entry_send.get()
        if data:
            if self.serial_comm.send_data(data):
                self.entry_send.delete(0, tk.END)
                self.security_manager.log_operation("数据发送", f"发送数据: {data}")
            else:
                messagebox.showerror("错误", "发送数据失败") 