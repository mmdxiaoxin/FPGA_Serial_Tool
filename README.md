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

## 打包程序

1. 安装PyInstaller
   ```bash
   pip install pyinstaller
   ```

2. 打包命令
   ```bash
   # 基本打包命令（生成单个exe文件，不显示控制台窗口）
   pyinstaller --noconsole --onefile main.py

   # 包含额外数据文件的打包命令
   pyinstaller --noconsole --onefile --add-data "src;src" main.py

   # 添加图标的打包命令
   pyinstaller --noconsole --onefile --icon=path/to/your/icon.ico main.py
   ```

3. 打包说明
   - 打包后的文件位于 `dist` 目录下
   - `--noconsole`: 不显示控制台窗口
   - `--onefile`: 将所有依赖打包成单个exe文件
   - `--add-data`: 添加额外的数据文件
   - `--icon`: 为exe文件添加图标

4. 注意事项
   - 确保所有依赖包都已正确安装
   - 如果程序需要访问外部文件，请使用 `--add-data` 参数
   - 首次运行打包后的程序时，可能会被杀毒软件拦截，需要添加信任
   - 建议在打包前先完整测试程序功能

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

- 程序数据存储在用户文档目录下的 `FPGA_Serial_Tool` 文件夹中：
  - 日志文件：`Documents/FPGA_Serial_Tool/logs/system.log`
  - 数据文件：`Documents/FPGA_Serial_Tool/data/`
  - 配置文件：`Documents/FPGA_Serial_Tool/config/`
- 支持数据导出和备份
- 自动记录系统日志

## 注意事项

1. 首次运行前请确保已正确安装所有依赖
2. 确保有适当的串口访问权限
3. 建议定期备份数据文件
4. 如遇到问题，请查看系统日志文件
5. 打包后的程序会在用户文档目录下自动创建数据存储文件夹 