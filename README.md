# FPGA声学测温系统

## 环境配置

### 使用Conda安装

1. 安装Conda（如果尚未安装）
   - 访问 [Miniconda官网](https://docs.conda.io/en/latest/miniconda.html) 下载并安装Miniconda
   - 或访问 [Anaconda官网](https://www.anaconda.com/products/distribution) 下载并安装Anaconda

2. 创建并激活环境
   ```bash
   # 创建环境
   conda env create -f environment.yml

   # 激活环境
   conda activate fpga_serial_tool
   ```

3. 验证安装
   ```bash
   # 检查Python版本
   python --version

   # 检查已安装的包
   conda list
   ```

## 运行程序

1. 确保已激活环境
   ```bash
   conda activate fpga_serial_tool
   ```

2. 运行程序
   ```bash
   python main.py
   ```

## 功能说明

1. 串口通信
   - 支持自动检测可用串口
   - 可配置波特率
   - 实时数据显示

2. 数据处理
   - 温度数据解析
   - 湿度数据解析
   - 数据存储和导出

3. 系统监控
   - 运行状态监控
   - 数据质量监控
   - 系统日志记录

4. 安全功能
   - 数据加密
   - 操作日志
   - 访问控制

## 配置文件

程序首次运行时会自动创建 `config.json` 配置文件，包含以下配置项：

```json
{
    "serial": {
        "port": "COM5",
        "baud_rate": 115200,
        "timeout": 1
    },
    "display": {
        "update_interval": 1000,
        "max_data_points": 1000
    },
    "storage": {
        "db_path": "temperature_data.db",
        "backup_interval": 3600
    },
    "alarm": {
        "temp_high": 40,
        "temp_low": 0,
        "humidity_high": 90,
        "humidity_low": 10
    }
}
```

## 数据存储

- 数据存储在 SQLite 数据库中（temperature_data.db）
- 支持数据导出和备份
- 自动记录系统日志（system.log）

## 注意事项

1. 首次运行前请确保已正确安装所有依赖
2. 确保有适当的串口访问权限
3. 建议定期备份数据库文件
4. 如遇到问题，请查看系统日志文件 