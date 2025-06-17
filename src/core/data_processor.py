import logging
from datetime import datetime

class DataProcessor:
    @staticmethod
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
            try:
                # 解析前3字节为整数
                other_value = int.from_bytes(data[:3], byteorder='big')
                other_value = ((0.1/(other_value*0.00000002))-335)/2.5
                
                # 解析湿度（整数+小数）
                humidity_int = data[3]
                humidity_frac = data[4]
                humidity = float(f"{humidity_int}.{humidity_frac}")
                
                # 解析温度（整数+小数）
                temp_int = data[5]-13
                temp_frac = data[6]
                temperature = float(f"{temp_int}.{temp_frac}")
                
                return {
                    'temperature': temperature,
                    'humidity': humidity,
                    'other_value': other_value,
                    'timestamp': datetime.now()
                }
            except Exception as e:
                logging.error(f"数据处理错误: {e}")
                return None
        return None 