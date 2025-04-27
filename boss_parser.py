#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @author  : jhzhong
# @time    : 2023/12/22 8:23
# @function: Parser for BOSS job listings information.

from datetime import datetime
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import loger

# City-province mapping dictionary
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

def extract_job_data(job):
    """
    Extract job data from a job listing element

    Args:
        job (WebElement): Job listing element

    Returns:
        dict: Extracted job data or None if critical data is missing
    """
    try:
        # Update XPath paths to match actual HTML structure
        job_title = job.find_element(by=By.XPATH, value='.//span[@class="job-name"]').text
        job_salary = job.find_element(by=By.XPATH, value='.//span[@class="job-salary"]').text
        job_location = job.find_element(by=By.XPATH, value='.//ul[@class="tag-list"]/li[1]/a').text
        job_experience = job.find_element(by=By.XPATH, value='.//ul[@class="tag-list"]/li[2]').text
        job_education = job.find_element(by=By.XPATH, value='.//ul[@class="tag-list"]/li[3]').text
        
        # Company information
        job_company = job.find_element(by=By.XPATH, value='.//div[@class="boss-info-attr"]').text.split('·')[0].strip()
        
        # Job description and requirements
        job_desc = job.find_element(by=By.XPATH, value='.//p[@class="desc"]').text
        
        # Job skills/tags
        job_skills = []
        skill_elements = job.find_elements(by=By.XPATH, value='.//ul[@class="job-label-list"]/li')
        for skill in skill_elements:
            job_skills.append(skill.text)
        job_skills = ','.join(job_skills)

        # Job address
        try:
            job_address = job.find_element(by=By.XPATH, value='.//p[@class="job-address-desc"]').text
        except:
            job_address = ""

        # Check if required fields are empty
        if not all([job_title, job_salary, job_location, job_company, job_experience, job_education]):
            return None

        # Return data in the correct order for storage
        return (
            job_title,
            job_salary,
            job_location,
            job_company,
            job_experience,
            job_education,
            job_desc,
            job_skills,
            job_address
        )

    except Exception as e:
        print(f"Error extracting job data: {str(e)}", level="ERROR")
        return None

def parse_job_listings(browser, current_category, sub_category):
    """
    Parse job listings from the page

    Args:
        browser (webdriver): Browser instance
        current_category (str): Main job category
        sub_category (str): Sub category of job

    Returns:
        list: List of parsed job data tuples
    """
    job_detail = browser.find_elements(by=By.XPATH, value='//div[contains(@class, "job-detail-box")]')
    
    parsed_data = []
    for job in job_detail:
        try:
            # Extract job information
            job_data = extract_job_data(job)
            if not job_data:
                continue

            # Find province based on city
            city = job_data[2].split('·')[0]  # job_location
            province = get_province_by_city(city, CITY_MAP)

            # Prepare data row with all fields
            data_row = (
                current_category,  # category
                sub_category,      # sub_category
                job_data[0],       # job_title
                province,          # province
                job_data[2],       # job_location
                job_data[3],       # job_company
                None,              # job_industry (not available in current parsing)
                None,              # job_finance (not available in current parsing)
                None,              # job_scale (not available in current parsing)
                None,              # job_welfare (not available in current parsing)
                None,              # job_salary_range (not available in current parsing)
                job_data[4],       # job_experience
                job_data[5],       # job_education
                job_data[7],       # job_skills
                job_data[8],       # job_address
                job_data[1],       # job_salary
                job_data[6],       # job_desc
                datetime.now().strftime('%Y-%m-%d')  # create_time
            )

            # Log extracted data
            print(f"Parsed: {job_data[0]} at {job_data[3]} in {city}")
            
            parsed_data.append(data_row)

        except Exception as e:
            print(f"Error parsing job data: {str(e)}", level="ERROR")
            continue
            
    return parsed_data 