# BOSS 直聘爬虫工具

## 功能说明

本工具包含两个主要爬虫：

1. `boss_selenium.py` - 职位分类爬虫
   - 按职位分类爬取 BOSS 直聘上的职位信息
   - 支持 MySQL 和 CSV 两种存储方式

2. `company_crawler.py` - 公司信息爬虫
   - 根据公司名称搜索并爬取公司信息
   - 爬取公司基本信息、在招职位等
   - 以 Markdown 格式保存信息

## 环境要求

- Python 3.6+
- Chrome/Edge/Firefox 浏览器
- 对应的浏览器驱动

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 公司信息爬虫

```bash
python company_crawler.py --company "公司名称" [--driver-type chrome|edge|firefox] [--output-dir 输出目录] [--headless]
```

参数说明：
- `--company`: 必需，要搜索的公司名称
- `--driver-type`: 可选，浏览器类型，支持 chrome/edge/firefox
- `--output-dir`: 可选，输出目录，默认为 "result"
- `--headless`: 可选，无头模式运行（不显示浏览器界面）

示例：
```bash
# 搜索"腾讯"公司信息
python company_crawler.py --company "腾讯" --driver-type chrome

# 无头模式搜索"阿里巴巴"公司信息
python company_crawler.py --company "阿里巴巴" --headless
```

### 输出文件结构

```
result/
  companies/
    公司名称/
      company_info.md    # 公司基本信息
      jobs.md            # 在招职位信息
```

### 文件格式说明

1. `company_info.md` 包含：
   - 公司名称
   - 行业
   - 规模
   - 融资阶段
   - 公司简介
   - 公司福利

2. `jobs.md` 包含：
   - 职位名称
   - 薪资范围
   - 工作地点
   - 经验要求
   - 学历要求
   - 职位描述
   - 技能要求

## 注意事项

1. 首次运行时需要手动完成验证码验证
2. 建议使用无头模式运行，减少资源占用
3. 爬取速度受网络状况影响，请耐心等待
4. 如遇到验证码，程序会暂停等待手动验证

## 常见问题

1. 爬取速度慢
   - 使用无头模式
   - 减少页面加载等待时间
   - 优化网络连接

## 更新日志

### v1.0.0 (2024-03-21)
- 初始版本发布
- 支持公司信息爬取
- 支持职位信息爬取
- 支持 Markdown 格式保存
