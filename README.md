# 一、BOSS 直聘爬虫项目

这是一个使用 Selenium 实现的 BOSS 直聘网站职位信息爬虫项目。

## 二、项目结构

```
.
├── boss_selenium.py    # 主爬虫脚本
├── boss_parser.py      # 职位数据解析模块
├── dbutils.py          # 数据库工具模块
├── browser_manager.py  # 浏览器管理模块
├── requirements.txt    # 项目依赖
└── README.md          # 项目文档
```

## 三、环境准备

1. 安装 Python 依赖：
```bash
pip install -r requirements.txt
```

2. 创建数据库和表：
```sql
CREATE DATABASE IF NOT EXISTS spider_db DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

USE spider_db;

CREATE TABLE IF NOT EXISTS job_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category VARCHAR(255) COMMENT '职位分类',
    sub_category VARCHAR(255) COMMENT '职位子分类',
    job_title VARCHAR(255) COMMENT '职位名称',
    province VARCHAR(255) COMMENT '省份',
    job_location VARCHAR(255) COMMENT '工作地点',
    job_company VARCHAR(255) COMMENT '公司名称',
    job_industry VARCHAR(255) COMMENT '行业类型',
    job_finance VARCHAR(255) COMMENT '融资情况',
    job_scale VARCHAR(255) COMMENT '公司规模',
    job_welfare VARCHAR(255) COMMENT '公司福利',
    job_salary_range VARCHAR(255) COMMENT '薪资范围',
    job_experience VARCHAR(255) COMMENT '工作经验要求',
    job_education VARCHAR(255) COMMENT '学历要求',
    job_skills VARCHAR(255) COMMENT '技能要求',
    create_time DATETIME COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

## 四、浏览器管理模块

`browser_manager.py` 模块提供了一个统一的接口来管理不同的浏览器及其驱动。支持：

- Chrome
- Edge
- Firefox

### 功能特点

1. 自动检测浏览器版本
2. 自动下载和管理浏览器驱动
3. 支持多种浏览器
4. 统一的浏览器初始化接口
5. 跨平台兼容（Windows、macOS、Linux）

### 使用示例

1. 基本用法：
```python
from browser_manager import get_browser

# 获取浏览器实例（自动选择可用的浏览器）
browser = get_browser()
if browser:
    browser.get("https://www.example.com")
    # 使用浏览器进行操作
    browser.quit()
```

2. 指定浏览器类型：
```python
from browser_manager import get_browser

# 获取特定类型的浏览器实例
browser = get_browser(drive_type='chrome')  # 或 'edge' 或 'firefox'
if browser:
    browser.get("https://www.example.com")
    # 使用浏览器进行操作
    browser.quit()
```

3. 测试浏览器功能：
```python
# 直接从命令行运行测试
python browser_manager.py
```

### 浏览器配置

模块使用配置字典来管理浏览器设置：

```python
BROWSER_CONFIGS = {
    'chrome': {
        'name': 'Google Chrome',
        'windows_reg_path': r"Software\Google\Chrome\BLBeacon",
        'mac_path': '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        'linux_cmd': 'google-chrome',
        'driver_manager': ChromeDriverManager,
        'service_class': ChromeService,
        'options_class': ChromeOptions
    },
    # Edge 和 Firefox 的类似配置
}
```

### 通用浏览器参数

模块为所有浏览器使用通用参数：
```python
COMMON_BROWSER_ARGS = ['--no-sandbox', '--disable-dev-shm-usage']  # 可以通过添加 '--headless' 启用无头模式
```

## 五、运行爬虫

1. 运行主脚本：
```bash
python boss_selenium.py
```

2. 脚本将执行以下操作：
   - 初始化浏览器
   - 连接数据库（如果可用）
   - 开始爬取职位信息
   - 将数据保存到数据库或 CSV 文件

## 六、数据存储

- 如果数据库连接成功，数据将保存到 MySQL 数据库
- 如果数据库连接失败，数据将保存到 CSV 文件（job_listings_backup.csv）

## 七、注意事项

- 确保已安装所需的浏览器
- 脚本会自动下载和管理浏览器驱动
- 爬取进度保存在 crawl_progress.txt 中，可以从中断处继续
