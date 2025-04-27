# 开发文档

## 1. 项目结构

```
.
├── boss_selenium.py    # 主程序入口
├── boss_parser.py      # 数据解析模块
├── browser_manager.py  # 浏览器管理模块
├── dbutils.py         # 数据库工具模块
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
# 自动选择浏览器
browser = get_browser()

# 指定浏览器类型
browser = get_browser('chrome')
```

### 3.4 测试用例
1. 自动检测浏览器
```python
browser = get_browser()
assert browser is not None  # 应该成功初始化一个浏览器
```

2. 指定浏览器类型
```python
browser = get_browser('edge')
assert isinstance(browser, webdriver.Edge)  # 应该是Edge浏览器实例
```

3. 浏览器版本不匹配
```python
# 应该自动下载匹配的驱动
browser = get_browser('chrome')
assert browser is not None
```

### 3.5 模块边界
- 输入：浏览器类型(可选)
- 输出：WebDriver实例
- 依赖：selenium, webdriver-manager
- 限制：需要网络连接下载驱动

### 3.6 注意事项
- 确保网络连接正常
- 浏览器版本需要与驱动匹配
- 注意浏览器自动更新可能导致驱动不匹配

## 4. 数据解析模块 (boss_parser.py)

### 4.1 功能说明
- 解析Boss直聘网页数据
- 提取职位信息
- 处理城市和省份映射
- 数据清洗和格式化

### 4.2 核心类和方法
```python
def extract_job_data(element):
    """从网页元素中提取职位数据"""
    
def process_job_listings(driver):
    """处理职位列表数据"""
```

### 4.3 使用示例
```python
# 解析职位数据
job_data = extract_job_data(element)

# 处理职位列表
jobs = process_job_listings(driver)
```

### 4.4 测试用例
1. 职位数据提取
```python
element = driver.find_element(...)
job_data = extract_job_data(element)
assert 'title' in job_data  # 应该包含职位标题
```

2. 城市省份映射
```python
province = get_province_by_city('北京')
assert province == '北京'  # 应该返回正确的省份
```

### 4.5 模块边界
- 输入：WebDriver实例或网页元素
- 输出：结构化数据
- 依赖：selenium
- 限制：需要匹配的网页结构

### 4.6 注意事项
- 网页结构变化可能导致解析失败
- 需要定期更新解析规则
- 注意处理异常情况

## 5. 数据库工具模块 (dbutils.py)

### 5.1 功能说明
- 数据库连接管理
- 数据插入和更新
- 查询操作封装
- 事务管理

### 5.2 核心类和方法
```python
class DBUtils:
    """数据库工具类"""
    def connect(self):
        """建立数据库连接"""
        
    def insert_job(self, job_data):
        """插入职位数据"""
```

### 5.3 使用示例
```python
# 连接数据库
db = DBUtils()
db.connect()

# 插入数据
db.insert_job(job_data)
```

### 5.4 测试用例
1. 数据库连接
```python
db = DBUtils()
assert db.connect()  # 应该成功连接数据库
```

2. 数据插入
```python
job_data = {...}
assert db.insert_job(job_data)  # 应该成功插入数据
```

### 5.5 模块边界
- 输入：数据库连接信息和数据
- 输出：数据库操作结果
- 依赖：pymysql
- 限制：需要有效的数据库连接

### 5.6 注意事项
- 确保数据库连接信息正确
- 注意事务处理
- 做好错误处理和重试机制 