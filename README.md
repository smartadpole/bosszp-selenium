# Boss直聘数据采集工具

这是一个基于 Selenium 的 Boss直聘数据采集工具，可以自动采集职位信息并保存到数据库。

## 功能特点

- 支持多种浏览器（Chrome/Edge/Firefox）
- 自动处理浏览器驱动
- 智能等待和重试机制
- 数据持久化存储（CSV格式）
- 详细的日志记录

## 环境要求

- Python 3.8+
- Chrome/Edge/Firefox 浏览器

## 快速开始

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 运行程序：
```bash
# 基本运行（使用默认配置）
python boss_selenium.py

# 指定浏览器类型
python boss_selenium.py --browser chrome  # 或 edge, firefox

# 使用无头模式（不显示浏览器窗口）
python boss_selenium.py --headless

# 指定输出目录
python boss_selenium.py --output-dir result
```

## 数据保存

程序会自动将采集到的数据保存为CSV文件，默认保存在 `./result` 目录下，文件名为 `job_data_YYYYMMDD.csv`。

### 数据格式
CSV文件包含以下字段：
- 职位名称
- 公司名称
- 工作地点
- 薪资范围
- 工作经验要求
- 学历要求
- 公司规模
- 公司行业
- 职位描述
- 发布时间

### 示例数据
```csv
职位名称,公司名称,工作地点,薪资范围,工作经验要求,学历要求,公司规模,公司行业,职位描述,发布时间
Python开发工程师,XX科技有限公司,北京,15k-30k,3-5年,本科,100-499人,互联网,负责Python后端开发...,2024-03-20
```

## 参数说明

| 参数           | 说明           | 默认值      |
|--------------|--------------|----------|
| --browser    | 指定浏览器类型      | chrome   |
| --headless   | 是否使用无头模式     | False    |
| --output-dir | 输出目录        | ./result |

## 项目结构

```
.
├── boss_selenium.py    # 主程序入口
├── boss_parser.py      # 数据解析模块
├── browser_manager.py  # 浏览器管理模块
├── dbutils.py         # 数据库工具模块
├── loger.py           # 日志管理模块
└── requirements.txt   # 项目依赖
```

## 开发文档

详细的模块说明、使用方法和测试用例请参考 [开发文档](docs/develop.md)。

## 注意事项

1. 确保已安装所需浏览器（chrome、edge、firefox 其中之一）
2. 确保网络连接正常
3. 注意遵守网站的使用条款

## 许可证

MIT License
