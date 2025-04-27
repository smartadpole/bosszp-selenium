#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @author  : jhzhong
# @time    : 2023/12/22 8:23
# @function: Main script for BOSS job listings crawler.

import os
import sys
import time
import argparse
from datetime import datetime
from selenium.webdriver.common.by import By
import loger
from database.mysql_handler import MySQLHandler
from database.csv_handler import CSVHandler
from boss_parser import parse_job_listings
from browser_manager import get_browser

def scrape_job_listings(browser, storage, csv_file):
    """
    Scrape job listings from BOSS website
    
    Args:
        browser (webdriver): Browser instance
        storage: Data storage instance (MySQL or CSV)
        csv_file (str): CSV file path for fallback storage
    """
    # Open BOSS homepage
    index_url = 'https://www.zhipin.com/?city=100010000&ka=city-sites-100010000'
    browser.get(index_url)
    print("Successfully accessed BOSS website")

    # Simulate clicking Internet/AI to show job categories
    show_ele = browser.find_element(by=By.XPATH, value='//*[@id="main"]/div/div[1]/div/div[1]/dl[1]/dd/b')
    show_ele.click()

    for i in range(85):
        try:
            print(f"Processing category index {i}")
            
            current_a = browser.find_elements(by=By.XPATH, value='//*[@id="main"]/div/div[1]/div/div[1]/dl[1]/div/ul/li/div/a')[i]
            current_category = current_a.find_element(by=By.XPATH, value='../../h4').text
            sub_category = current_a.text
            print(f"Scraping {current_category}--{sub_category}")
            
            # Click on the category
            browser.find_elements(by=By.XPATH, value='//*[@id="main"]/div/div[1]/div/div[1]/dl[1]/div/ul/li/div/a')[i].click()

            # Scroll page to load all content
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(10)
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Parse job listings
            parsed_data = parse_job_listings(browser, current_category, sub_category)
            
            if parsed_data:
                try:
                    # Try to save to primary storage
                    for data_row in parsed_data:
                        storage.insert_job_listing(data_row)
                except Exception as e:
                    # If primary storage fails, save to CSV
                    print(f"Primary storage failed: {str(e)}", level="ERROR")
                    print("Falling back to CSV storage")
                    csv_storage = CSVHandler(os.path.dirname(csv_file))
                    csv_storage.save_data(parsed_data)
                    csv_storage.close()

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
            print(f"Error processing category {i}: {str(e)}", level="ERROR")
            continue

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='BOSS job listings crawler')
    parser.add_argument('--driver-type', choices=['chrome', 'edge', 'firefox'], 
                       default='chrome', help='Browser type')
    args = parser.parse_args()

    # Initialize logger
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
    loger.init_logger(output_dir)
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize data storage
    storage = None
    try:
        # Try to connect to MySQL
        db = MySQLHandler(
            host='localhost',
            user='root',
            password='123456',
            database='spider_db'
        )
        db.create_database_and_table()
        storage = db
        print("Successfully connected to MySQL database")
    except Exception as e:
        # Fallback to CSV storage if MySQL connection fails
        print(f"MySQL connection failed: {str(e)}", level="ERROR")
        print("Switching to CSV storage mode")
        storage = CSVHandler(output_dir)
        storage.create_database_and_table()
        print("Successfully initialized CSV storage")

    try:
        # Initialize browser
        browser = get_browser(args.driver_type)
        print(f"Successfully initialized {args.driver_type} browser")

        # Set CSV file path for fallback storage
        csv_file = os.path.join(output_dir, f'job_info_{datetime.now().strftime("%Y%m%d")}.csv')

        # Start scraping
        scrape_job_listings(browser, storage, csv_file)

    except Exception as e:
        print(f"Program execution error: {str(e)}", level="ERROR")
    finally:
        # Close browser and data storage
        if 'browser' in locals():
            browser.quit()
        if storage:
            storage.close()
        print("Crawling completed")

if __name__ == "__main__":
    main()