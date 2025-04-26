#!/usr/bin/python
# -*- coding:utf-8 -*-
# @author  : jhzhong
# @time    : 2023/12/22 8:23
# @function: Web scraper for job listings from BOSS recruitment platform.
# @version : V2

import datetime
import time
import os
import sys
import csv
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

import loger

# Try to import DBUtils, but make database usage optional
try:
    from dbutils import DBUtils
    HAS_DB_UTILS = True
except ImportError:
    HAS_DB_UTILS = False

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'db': 'spider_db',
    'port': 3306,
    'charset': 'utf8'
}

# Chrome driver path
CHROME_DRIVER_PATH = "/usr/bin/chromedriver"  # 默认路径
if not os.path.exists(CHROME_DRIVER_PATH):
    CHROME_DRIVER_PATH = "/usr/local/bin/chromedriver"  # 备选路径

# Backup file for scraped data when database is not available
BACKUP_CSV_FILE = "job_listings_backup.csv"

# City-province mapping dictionary (keeping original Chinese)
CITY_MAP = {
    "北京": ["北京"],
    "天津": ["天津"],
    "山西": ["太原", "阳泉", "晋城", "长治", "临汾", "运城", "忻州", "吕梁", "晋中", "大同", "朔州"],
    "河北": ["沧州", "石家庄", "唐山", "保定", "廊坊", "衡水", "邯郸", "邢台", "张家口", "辛集", "秦皇岛", "定州",
             "承德", "涿州"],
    "山东": ["济南", "淄博", "聊城", "德州", "滨州", "济宁", "菏泽", "枣庄", "烟台", "威海", "泰安", "青岛", "临沂",
             "莱芜", "东营", "潍坊", "日照"],
    "河南": ["郑州", "新乡", "鹤壁", "安阳", "焦作", "濮阳", "开封", "驻马店", "商丘", "三门峡", "南阳", "洛阳", "周口",
             "许昌", "信阳", "漯河", "平顶山", "济源"],
    "广东": ["珠海", "中山", "肇庆", "深圳", "清远", "揭阳", "江门", "惠州", "河源", "广州", "佛山", "东莞", "潮州",
             "汕尾", "梅州", "阳江", "云浮", "韶关", "湛江", "汕头", "茂名"],
    "浙江": ["舟山", "温州", "台州", "绍兴", "衢州", "宁波", "丽水", "金华", "嘉兴", "湖州", "杭州"],
    "宁夏": ["中卫", "银川", "吴忠", "石嘴山", "固原"],
    "江苏": ["镇江", "扬州", "盐城", "徐州", "宿迁", "无锡", "苏州", "南通", "南京", "连云港", "淮安", "常州", "泰州"],
    "湖南": ["长沙", "邵阳", "怀化", "株洲", "张家界", "永州", "益阳", "湘西", "娄底", "衡阳", "郴州", "岳阳", "常德",
             "湘潭"],
    "吉林": ["长春", "长春", "通化", "松原", "四平", "辽源", "吉林", "延边", "白山", "白城"],
    "福建": ["漳州", "厦门", "福州", "三明", "莆田", "宁德", "南平", "龙岩", "泉州"],
    "甘肃": ["张掖", "陇南", "兰州", "嘉峪关", "白银", "武威", "天水", "庆阳", "平凉", "临夏", "酒泉", "金昌", "甘南",
             "定西"],
    "陕西": ["榆林", "西安", "延安", "咸阳", "渭南", "铜川", "商洛", "汉中", "宝鸡", "安康"],
    "辽宁": ["营口", "铁岭", "沈阳", "盘锦", "辽阳", "锦州", "葫芦岛", "阜新", "抚顺", "丹东", "大连", "朝阳", "本溪",
             "鞍山"],
    "江西": ["鹰潭", "宜春", "上饶", "萍乡", "南昌", "景德镇", "吉安", "抚州", "新余", "九江", "赣州"],
    "黑龙江": ["伊春", "七台河", "牡丹江", "鸡西", "黑河", "鹤岗", "哈尔滨", "大兴安岭", "绥化", "双鸭山", "齐齐哈尔",
               "佳木斯", "大庆"],
    "安徽": ["宣城", "铜陵", "六安", "黄山", "淮南", "合肥", "阜阳", "亳州", "安庆", "池州", "宿州", "芜湖", "马鞍山",
             "淮北", "滁州", "蚌埠"],
    "湖北": ["孝感", "武汉", "十堰", "荆门", "黄冈", "襄阳", "咸宁", "随州", "黄石", "恩施", "鄂州", "荆州", "宜昌",
             "潜江", "天门", "神农架", "仙桃"],
    "青海": ["西宁", "海西", "海东", "玉树", "黄南", "海南", "海北", "果洛"],
    "新疆": ["乌鲁木齐", "克州", "阿勒泰", "五家渠", "石河子", "伊犁", "吐鲁番", "塔城", "克拉玛依", "喀什", "和田",
             "哈密", "昌吉", "博尔塔拉", "阿克苏", "巴音郭楞", "阿拉尔", "图木舒克", "铁门关"],
    "贵州": ["铜仁", "黔东南", "贵阳", "安顺", "遵义", "黔西南", "黔南", "六盘水", "毕节"],
    "四川": ["遂宁", "攀枝花", "眉山", "凉山", "成都", "巴中", "广安", "自贡", "甘孜", "资阳", "宜宾", "雅安", "内江",
             "南充", "绵阳", "泸州", "凉山", "乐山", "广元", "甘孜", "德阳", "达州", "阿坝"],
    "上海": ["上海"],
    "广西": ["南宁", "贵港", "玉林", "梧州", "钦州", "柳州", "来宾", "贺州", "河池", "桂林", "防城港", "崇左", "北海",
             "百色"],
    "西藏": ["拉萨", "山南", "日喀则", "那曲", "林芝", "昌都", "阿里"],
    "云南": ["昆明", "红河", "大理", "玉溪", "昭通", "西双版纳", "文山", "曲靖", "普洱", "怒江", "临沧", "丽江", "红河",
             "迪庆", "德宏", "大理", "楚雄", "保山"],
    "内蒙古": ["呼和浩特", "乌兰察布", "兴安", "赤峰", "呼伦贝尔", "锡林郭勒", "乌海", "通辽", "巴彦淖尔", "阿拉善",
               "鄂尔多斯", "包头"],
    "海南": ["海口", "三沙", "三亚", "临高", "五指山", "陵水", "文昌", "万宁", "白沙", "乐东", "澄迈", "屯昌", "定安",
             "东方", "保亭", "琼中", "琼海", "儋州", "昌江"],
    "重庆": ["重庆"]
}

def setup_database():
    """
    Setup database connection if available

    Returns:
        bool: True if database setup is successful, False otherwise
    """
    if not HAS_DB_UTILS:
        print("DBUtils module not found. Data will be saved to CSV file.")
        return False

    try:
        db = DBUtils(DB_CONFIG['host'], DB_CONFIG['user'], DB_CONFIG['password'], 'mysql')
        db.create_database_and_table()
        db.close()
        print("Database connection successful and initialized.")
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        print("Data will be saved to CSV file instead.")
        return False


def init_browser():
    """
    Initialize Chrome browser for scraping

    Returns:
        webdriver: Initialized Chrome browser instance or None if failed
    """
    try:
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--headless')  # 无头模式，不显示浏览器窗口
        chrome_options.add_argument('--disable-gpu')
        
        # Set executable path
        if not os.path.exists(CHROME_DRIVER_PATH):
            print(f"Chrome driver not found at {CHROME_DRIVER_PATH}")
            return None
            
        # Set executable permissions
        try:
            os.chmod(CHROME_DRIVER_PATH, 0o755)  # 设置可执行权限
        except Exception as e:
            print(f"Failed to set permissions for Chrome driver: {e}")
            
        # Initialize browser
        service = Service(executable_path=CHROME_DRIVER_PATH)
        browser = webdriver.Chrome(service=service, options=chrome_options)
        return browser
    except WebDriverException as e:
        print(f"Failed to initialize browser: {e}", level="ERROR")
        return None


def get_province_by_city(city_name, city_map):
    """
    Get province name based on city name

    Args:
        city_name (str): Name of the city
        city_map (dict): Dictionary mapping provinces to cities

    Returns:
        str: Province name or empty string if not found
    """
    for province, cities in city_map.items():
        if city_name in cities:
            return province
    return ''


def create_csv_backup_file(headers):
    """
    Create a CSV backup file with headers

    Args:
        headers (list): List of column headers
    """
    with open(BACKUP_CSV_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)


def save_to_csv(data_row):
    """
    Save a row of data to CSV backup file

    Args:
        data_row (tuple): Data to save
    """
    with open(BACKUP_CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(data_row)

def save_progress(category_index):
    """Save crawling progress"""
    with open('crawl_progress.txt', 'w') as f:
        f.write(str(category_index))

def load_progress():
    """Load crawling progress"""
    try:
        with open('crawl_progress.txt', 'r') as f:
            return int(f.read().strip())
    except:
        return 0

def scrape_job_listings(browser, use_db=False):
    """
    Main function to scrape job listings from BOSS website

    Args:
        browser (webdriver): Initialized browser instance
        use_db (bool): Whether to use database for storage
    """
    # Create CSV file if not using database
    if not use_db:
        headers = ["category", "sub_category", "job_title", "province", "job_location",
                   "job_company", "job_industry", "job_finance", "job_scale", "job_welfare",
                   "job_salary_range", "job_experience", "job_education", "job_skills", "create_time"]
        create_csv_backup_file(headers)

    # Open BOSS homepage
    index_url = 'https://www.zhipin.com/?city=100010000&ka=city-sites-100010000'
    browser.get(index_url)

    # Simulate clicking Internet/AI to show job categories
    show_ele = browser.find_element(by=By.XPATH, value='//*[@id="main"]/div/div[1]/div/div[1]/dl[1]/dd/b')
    show_ele.click()

    today = datetime.date.today().strftime('%Y-%m-%d')

    for i in range(85):
        try:
            logging.info(f"Processing category index {i}")
            # Save progress
            save_progress(i)

            current_a = browser.find_elements(by=By.XPATH, value='//*[@id="main"]/div/div[1]/div/div[1]/dl[1]/div/ul/li/div/a')[i]
            current_category = current_a.find_element(by=By.XPATH, value='../../h4').text
            sub_category = current_a.text
            print("{} Crawling {}--{}".format(today, current_category, sub_category))
            browser.find_elements(by=By.XPATH, value='//*[@id="main"]/div/div[1]/div/div[1]/dl[1]/div/ul/li/div/a')[i].click()

            # Scroll page to load all content
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(10)
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Scrape job details
            process_job_listings(browser, current_category, sub_category, today, use_db)

            try:
                # Return to homepage
                browser.back()
                # Simulate clicking Internet/AI to show job categories
                show_ele = browser.find_element(by=By.XPATH, value='//*[@id="main"]/div/div[1]/div/div[1]/dl[1]/dd/b')
                show_ele.click()
            except:
                browser.get(index_url)
                # Simulate clicking Internet/AI to show job categories
                show_ele = browser.find_element(by=By.XPATH, value='//*[@id="main"]/div/div[1]/div/div[1]/dl[1]/dd/b')
                show_ele.click()
        except Exception as e:
            print(f"Error processing category {i}: {e}")
            # Try to recover and continue with next category
            try:
                browser.get(index_url)
                show_ele = browser.find_element(by=By.XPATH, value='//*[@id="main"]/div/div[1]/div/div[1]/dl[1]/dd/b')
                show_ele.click()
                time.sleep(5)
            except:
                print("Failed to recover, exiting...")
                break

    time.sleep(10)


def process_job_listings(browser, current_category, sub_category, today, use_db=False):
    """
    Process job listings and save to database or CSV

    Args:
        browser (webdriver): Browser instance
        current_category (str): Main job category
        sub_category (str): Sub category of job
        today (str): Current date string
        use_db (bool): Whether to use database for storage
    """
    job_detail = browser.find_elements(by=By.XPATH,
                                       value='//*[@id="wrap"]/div[2]/div[2]/div/div[1]/div[2]/ul/li')

    for job in job_detail:
        db = None
        try:
            # Extract job information
            job_data = extract_job_data(job)
            if not job_data:
                continue

            # Find province based on city
            city = job_data['job_location'].split('·')[0]
            province = get_province_by_city(city, CITY_MAP)

            # Prepare data row
            data_row = (
                current_category, sub_category, job_data['job_title'], province, job_data['job_location'],
                job_data['job_company'], job_data['job_industry'], job_data['job_finance'],
                job_data['job_scale'], job_data['job_welfare'], job_data['job_salary_range'],
                job_data['job_experience'], job_data['job_education'], job_data['job_skills'], today
            )

            # Log extracted data
            print(f"提取: {job_data['job_title']} at {job_data['job_company']} in {city}")

            # Save data either to database or CSV
            if use_db:
                db = DBUtils(DB_CONFIG['host'], DB_CONFIG['user'], DB_CONFIG['password'], DB_CONFIG['db'])
                db.insert_data(
                    "insert into job_info(category, sub_category,job_title,province,job_location,job_company,job_industry,"
                    "job_finance,job_scale,job_welfare,job_salary_range,job_experience,job_education,job_skills,create_time) "
                    "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    args=data_row)
            else:
                save_to_csv(data_row)

        except Exception as e:
            print(f"Error occurred while processing job: {e}")
            traceback.print_exc()
        finally:
            if db:
                db.close()


def extract_job_data(job):
    """
    Extract job data from a job listing element

    Args:
        job (WebElement): Job listing web element

    Returns:
        dict: Dictionary of job details or None if critical data is missing
    """
    try:
        job_title = job.find_element(by=By.XPATH, value="./div[1]/a/div[1]/span[1]").text.strip()
    except:
        return None

    # Extract all job details
    job_data = {
        'job_title': job_title,
        'job_location': job.find_element(by=By.XPATH, value="./div[1]/a/div[1]/span[2]/span").text.strip(),
        'job_company': job.find_element(by=By.XPATH, value="./div[1]/div/div[2]/h3/a").text.strip(),
        'job_industry': job.find_element(by=By.XPATH, value="./div[1]/div/div[2]/ul/li[1]").text.strip(),
        'job_finance': job.find_element(by=By.XPATH, value="./div[1]/div/div[2]/ul/li[2]").text.strip(),
        'job_salary_range': job.find_element(by=By.XPATH, value="./div[1]/a/div[2]/span[1]").text.strip(),
        'job_experience': job.find_element(by=By.XPATH, value="./div[1]/a/div[2]/ul/li[1]").text.strip(),
        'job_education': job.find_element(by=By.XPATH, value="./div[1]/a/div[2]/ul/li[2]").text.strip(),
    }

    # Extract optional fields with fallbacks
    try:
        job_data['job_scale'] = job.find_element(by=By.XPATH, value="./div[1]/div/div[2]/ul/li[3]").text.strip()
    except:
        job_data['job_scale'] = "None"

    try:
        job_data['job_welfare'] = job.find_element(by=By.XPATH, value="./div[2]/div").text.strip()
    except:
        job_data['job_welfare'] = 'None'

    try:
        job_data['job_skills'] = ','.join(
            [skill.text.strip() for skill in job.find_elements(by=By.XPATH, value="./div[2]/ul/li")])
    except:
        job_data['job_skills'] = 'None'

    return job_data


if __name__ == '__main__':
    # Setup database - if fails, will use CSV backup
    use_database = setup_database()
    browser = init_browser()
    if not browser:
        print("Browser initialization failed. Exiting...")
        sys.exit(1)

    try:
        # Start crawling
        scrape_job_listings(browser, use_database)
    except Exception as e:
        print(f"An error occurred during scraping: {e}")
        traceback.print_exc()
    finally:
        # Always close browser
        if browser:
            browser.quit()

    print("Scraping completed.")