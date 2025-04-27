# 开发文档

## 1. 项目结构

```
.
├── boss_selenium.py    # 主程序入口
├── boss_parser.py      # 数据解析模块
├── browser_manager.py  # 浏览器管理模块
├── database/           # 数据存储模块
│   ├── mysql_handler.py  # MySQL数据库处理
│   └── csv_handler.py    # CSV文件处理
├── loger.py           # 日志管理模块
└── requirements.txt   # 项目依赖
```

## 2. 日志模块 (loger.py)

### 2.1 功能说明
- 提供统一的日志记录功能
- 支持控制台彩色输出
- 支持日志文件轮转
- 自动记录调用位置信息

### 2.2 核心类和方法
```python
class Logger:
    """日志管理器"""
    def __init__(self):
        # 初始化默认配置
        self.output_dir = DEFAULT_OUTPUT_DIR
        self.log_file = os.path.join(self.output_dir, LOG_FILE)
        self._setup_logging()

    def set_output_dir(self, output_dir):
        """设置日志输出目录"""
        # 如果日志文件已存在，先删除
        if os.path.exists(self.log_file):
            os.remove(self.log_file)
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.log_file = os.path.join(self.output_dir, LOG_FILE)
        self._setup_logging()
```

### 2.3 使用示例
```python
# 基本使用
print("普通信息")
print("错误信息", level="ERROR")

# 设置日志目录
init_logger('./output')
```

### 2.4 测试用例
1. 基本日志输出
```python
print("测试信息")  # 应该输出到控制台和默认日志文件
```

2. 错误日志
```python
print("测试错误", level="ERROR")  # 应该以红色显示
```

3. 自定义日志目录
```python
init_logger('./custom_logs')
print("自定义目录测试")  # 应该输出到新目录的日志文件
```

### 2.5 模块边界
- 输入：日志消息和级别
- 输出：控制台输出和日志文件
- 依赖：无外部依赖
- 限制：日志文件大小限制为10MB

### 2.6 注意事项
- 确保日志目录有写入权限
- 注意日志文件大小限制
- 彩色输出可能在某些终端不显示

## 3. 浏览器管理模块 (browser_manager.py)

### 3.1 功能说明
- 自动检测已安装的浏览器
- 自动下载匹配的浏览器驱动
- 支持多种浏览器(Chrome/Edge/Firefox)
- 提供统一的浏览器初始化接口

### 3.2 核心类和方法
```python
class BrowserManager:
    """浏览器管理器"""
    def get_available_browsers(self):
        """获取可用的浏览器列表"""
        
    def get_browser(self, browser_type=None):
        """初始化指定类型的浏览器"""
        
    def _download_driver(self, browser_type, version):
        """下载指定版本的浏览器驱动"""
```

### 3.3 使用示例
```python
# 获取浏览器实例
browser = get_browser('chrome')  # 使用Chrome浏览器
browser = get_browser()  # 自动选择可用的浏览器
```

### 3.4 测试用例
1. 浏览器检测
```python
browsers = get_available_browsers()
assert 'chrome' in browsers  # 如果安装了Chrome
```

2. 驱动下载
```python
browser = get_browser('chrome')  # 应该自动下载匹配的驱动
```

3. 错误处理
```python
try:
    browser = get_browser('unsupported_browser')
except Exception as e:
    print(f"预期错误: {e}")
```

### 3.5 模块边界
- 输入：浏览器类型
- 输出：WebDriver实例
- 依赖：selenium, webdriver-manager
- 限制：需要网络连接下载驱动

### 3.6 注意事项
- 确保网络连接正常
- 注意浏览器版本兼容性
- 可能需要管理员权限安装驱动

## 4. 数据解析模块 (boss_parser.py)

### 4.1 功能说明
- 解析职位列表页面
- 提取职位详细信息
- 处理城市-省份映射
- 格式化数据输出

### 4.2 核心函数
```python
def parse_job_listings(browser, current_category, sub_category):
    """解析职位列表"""
    
def extract_job_data(job):
    """提取单个职位数据"""
    
def get_province_by_city(city_name, city_map):
    """根据城市获取省份"""
```

### 4.3 使用示例
```python
# 解析职位列表
parsed_data = parse_job_listings(browser, "互联网", "后端开发")
for data in parsed_data:
    print(f"职位: {data[2]}, 公司: {data[5]}")
```

### 4.4 测试用例
1. 数据提取
```python
job_data = extract_job_data(job_element)
assert 'job_title' in job_data
assert 'job_company' in job_data
```

2. 城市映射
```python
province = get_province_by_city('北京', CITY_MAP)
assert province == '北京'
```

### 4.5 模块边界
- 输入：WebElement对象
- 输出：格式化后的数据元组
- 依赖：selenium
- 限制：需要页面结构稳定

### 4.6 注意事项
- 注意页面结构变化
- 处理缺失字段
- 注意编码问题

## 5. 数据存储模块 (database/)

### 5.1 MySQL处理 (mysql_handler.py)

#### 5.1.1 功能说明
- 管理数据库连接
- 创建数据表
- 插入职位数据
- 事务处理

#### 5.1.2 核心类和方法
```python
class MySQLHandler:
    def __init__(self, host, user, password, database):
        """初始化数据库连接"""
        
    def create_database_and_table(self):
        """创建数据库和表"""
        
    def insert_job_listing(self, data_row):
        """插入职位数据"""
```

#### 5.1.3 使用示例
```python
# 创建数据库连接
db = MySQLHandler('localhost', 'root', '123456', 'spider_db')
db.create_database_and_table()

# 插入数据
db.insert_job_listing(job_data)
```

### 5.2 CSV处理 (csv_handler.py)

#### 5.2.1 功能说明
- 创建CSV文件
- 写入职位数据
- 文件管理

#### 5.2.2 核心类和方法
```python
class CSVHandler:
    def __init__(self, output_dir):
        """初始化CSV处理器"""
        
    def create_database_and_table(self):
        """创建CSV文件"""
        
    def save_data(self, data):
        """保存数据到CSV"""
```

#### 5.2.3 使用示例
```python
# 创建CSV处理器
csv = CSVHandler('./output')
csv.create_database_and_table()

# 保存数据
csv.save_data(job_data)
```

## 6. 主程序 (boss_selenium.py)

### 6.1 功能说明
- 程序入口
- 命令行参数解析
- 模块协调
- 错误处理

### 6.2 核心函数
```python
def main():
    """主函数"""
    
def scrape_job_listings(browser, storage, csv_file):
    """爬取职位列表"""
```

### 6.3 使用示例
```bash
# 运行程序
python boss_selenium.py --driver-type chrome
```

### 6.4 测试用例
1. 参数解析
```python
# 测试命令行参数
python boss_selenium.py --driver-type edge
```

2. 错误处理
```python
# 测试数据库连接失败
# 应该自动切换到CSV存储
```

### 6.5 模块边界
- 输入：命令行参数
- 输出：爬取的数据
- 依赖：所有其他模块
- 限制：需要网络连接

### 6.6 注意事项
- 注意异常处理
- 合理设置超时
- 遵守爬虫规则

## 7. 开发指南

### 7.1 环境配置
1. 安装Python 3.8+
2. 安装依赖包
```bash
pip install -r requirements.txt
```
3. 安装浏览器(Chrome/Edge/Firefox)

### 7.2 代码规范
1. 遵循PEP 8规范
2. 使用类型注解
3. 添加必要的注释
4. 编写单元测试

### 7.3 调试技巧
1. 使用日志定位问题
2. 检查网络请求
3. 验证数据格式
4. 测试异常情况

### 7.4 性能优化
1. 合理设置等待时间
2. 优化数据库操作
3. 使用连接池
4. 批量处理数据

### 7.5 安全考虑
1. 保护数据库凭证
2. 限制请求频率
3. 验证输入数据
4. 处理敏感信息

## 8. 常见问题

### 8.1 浏览器驱动问题
Q: 驱动下载失败
A: 检查网络连接，或手动下载驱动

Q: 版本不匹配
A: 更新浏览器或驱动版本

### 8.2 数据存储问题
Q: 数据库连接失败
A: 检查配置和网络

Q: CSV写入失败
A: 检查文件权限

### 8.3 爬取问题
Q: 页面加载超时
A: 调整等待时间

Q: 数据解析错误
A: 检查页面结构变化

## 9. 更新日志

### v1.0.0
- 初始版本发布
- 支持多浏览器
- 实现数据存储
- 添加日志功能

### v1.1.0
- 优化浏览器管理
- 改进错误处理
- 添加单元测试
- 更新文档 