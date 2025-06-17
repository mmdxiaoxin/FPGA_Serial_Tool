# -*- coding: utf-8 -*-
"""
Created on Mon Mar 24 20:42:29 2025

@author: ASUS
"""


import tkinter as tk
from tkinter import scrolledtext
import serial
import serial.tools.list_ports
import threading

# 串口配置
SERIAL_PORT = 'COM5'  # 根据实际情况修改串口号
BAUD_RATE = 115200
TIMEOUT = 1

# 全局变量
serial_port = None
is_serial_open = False
buffer = bytearray()  # 数据缓冲区

def toggle_serial():
    global serial_port, is_serial_open
    if not is_serial_open:
        try:
            serial_port = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT)
            is_serial_open = True
            btn_toggle_serial.config(text="关闭串口")
            text_display.insert(tk.END, "串口已打开\n")
            threading.Thread(target=read_serial_data, daemon=True).start()
        except Exception as e:
            text_display.insert(tk.END, f"打开串口失败: {e}\n")
    else:
        if serial_port:
            serial_port.close()
            is_serial_open = False
            btn_toggle_serial.config(text="打开串口")
            text_display.insert(tk.END, "串口已关闭\n")

def process_data(data):
    """
    处理7字节数据格式：
    字节0-2: 其他数据（转为整数）
    字节3: 湿度整数部分
    字节4: 湿度小数部分 
    字节5: 温度整数部分
    字节6: 温度小数部分
    """
    if len(data) == 7:  
        # 解析前3字节为整数
        other_value = int.from_bytes(data[:3], byteorder='big')
        other_value =((0.1/(other_value*0.00000002))-335)/2.5
        # 解析湿度（整数+小数）
        humidity_int = data[3]
        humidity_frac = data[4]
        humidity = float(f"{humidity_int}.{humidity_frac}")
        
        # 解析温度（整数+小数）
        temp_int = data[5]-13
        temp_frac = data[6]
        temperature = float(f"{temp_int}.{temp_frac}")
        
        return (f"湿度: {humidity:.2f}%, "
                f"温度: {other_value:.2f}°C")
    
    return f"原始数据: {data.hex(' ')}"  # 如果数据格式不符，返回原始十六进制数据

def read_serial_data():
    global buffer
    while is_serial_open:
        if serial_port and serial_port.in_waiting:
            data = serial_port.read(serial_port.in_waiting)
            buffer.extend(data)

            while b'\x0D\x0A' in buffer:
                end_index = buffer.find(b'\x0D\x0A')
                packet = buffer[:end_index]
                
                processed_data = process_data(packet)
                text_display.insert(tk.END, f"接收: {processed_data}\n")
                text_display.see(tk.END)
                
                buffer = buffer[end_index + 2:]

def send_data():
    if is_serial_open and serial_port:
        data = entry_send.get()
        if data:
            data_to_send = data.encode() + b'\x0D\x0A'
            serial_port.write(data_to_send)
            text_display.insert(tk.END, f"发送: {data_to_send.hex(' ')}\n")
            entry_send.delete(0, tk.END)
    else:
        text_display.insert(tk.END, "串口未打开，无法发送数据\n")

# 创建GUI界面
root = tk.Tk()
root.title("FPGA串口通信工具")

text_display = scrolledtext.ScrolledText(root, width=80, height=20, wrap=tk.WORD)
text_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

btn_toggle_serial = tk.Button(root, text="打开串口", command=toggle_serial)
btn_toggle_serial.grid(row=1, column=0, padx=10, pady=10)

entry_send = tk.Entry(root, width=60)
entry_send.grid(row=2, column=0, padx=10, pady=10)

btn_send = tk.Button(root, text="发送", command=send_data)
btn_send.grid(row=2, column=1, padx=10, pady=10)

root.mainloop()