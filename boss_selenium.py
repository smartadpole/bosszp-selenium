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
import argparse
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

from dbutils import DBUtils
from browser_utils import get_browser
from boss_parser import process_job_listings

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'db': 'spider_db',
    'port': 3306,
    'charset': 'utf8'
}

# Backup file for scraped data when database is not available
BACKUP_CSV_FILE = "job_listings_backup.csv"

# System driver directories to search
SYSTEM_DRIVER_DIRS = [
    '/usr/bin',
    '/usr/local/bin',
    '/opt/homebrew/bin',  # macOS
    os.path.expanduser('~/.local/bin'),  # User local bin
]

def parse_arguments():
    """
    Parse command line arguments
    
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(description='BOSS job listing scraper')
    parser.add_argument('--driver-dir', type=str, default=None,
                       help='Specific directory containing browser drivers (optional)')
    return parser.parse_args()

def setup_database():
    """
    Setup database connection if available

    Returns:
        bool: True if database setup is successful, False otherwise
    """
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

            # Process job listings
            process_job_listings(browser, current_category, sub_category, today, use_db, DB_CONFIG)

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

if __name__ == '__main__':
    args = parse_arguments()

    use_database = setup_database()
    browser = get_browser(args.driver_dir)
    if not browser:
        print("Failed to initialize browser. Exiting...")
        sys.exit(1)


    try:
        scrape_job_listings(browser, use_database)
    except Exception as e:
        print(f"An error occurred during scraping: {e}")
        traceback.print_exc()
    finally:
        # Cleanup
        if browser:
            browser.quit()
        print("Scraping completed.")