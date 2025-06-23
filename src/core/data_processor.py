import logging
from datetime import datetime

class DataProcessor:
    @staticmethod
    def process_data(data):
        """
        处理7字节数据格式：
        字节0-2: 温度数据（转为整数，然后转换为温度值）
        字节3: 湿度整数部分
        字节4: 湿度小数部分 
        字节5: 其他值整数部分
        字节6: 其他值小数部分
        """
        if len(data) == 7:
            try:
                # 解析前3字节为温度值
                temp_raw = int.from_bytes(data[:3], byteorder='big')
                temperature = ((0.1/(temp_raw*0.00000002))-335)/2.5
                
                # 解析湿度（整数+小数）
                humidity_int = data[3]
                humidity_frac = data[4]
                humidity = float(f"{humidity_int}.{humidity_frac}")
                
                # 解析其他值（整数+小数）
                other_int = data[5]
                other_frac = data[6]
                other_value = float(f"{other_int}.{other_frac}")
                
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