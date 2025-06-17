import serial
import serial.tools.list_ports
import logging
from .global_vars import g_vars

class SerialCommunication:
    def __init__(self):
        self.available_ports = []
        self.update_ports()
        
    def update_ports(self):
        self.available_ports = [port.device for port in serial.tools.list_ports.comports()]
        
    def open_port(self, port, baud_rate, timeout):
        try:
            g_vars.serial_port = serial.Serial(port, baud_rate, timeout=timeout)
            g_vars.is_serial_open = True
            logging.info(f"串口 {port} 已打开")
            return True
        except Exception as e:
            logging.error(f"打开串口失败: {e}")
            return False
            
    def close_port(self):
        if g_vars.serial_port:
            g_vars.serial_port.close()
            g_vars.is_serial_open = False
            logging.info("串口已关闭")
            
    def send_data(self, data):
        if g_vars.is_serial_open and g_vars.serial_port:
            try:
                data_to_send = data.encode() + b'\x0D\x0A'
                g_vars.serial_port.write(data_to_send)
                logging.info(f"发送数据: {data_to_send.hex(' ')}")
                return True
            except Exception as e:
                logging.error(f"发送数据失败: {e}")
                return False
        return False 