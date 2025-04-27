#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @author  : jhzhong
# @time    : 2023/12/22 8:23
# @function: Main script for BOSS job listings crawler.

import os
import time
import argparse
from datetime import datetime
from selenium.webdriver.common.by import By
import loger
from database.data_storage import init_storage
from boss_parser import parse_job_listings
from browser_manager import get_browser
import random

BACKUP_CSV_FILE = os.path.join("job_listings_backup.csv")
PROCESS_FILE = os.path.join("crawl_progress.txt")
DEFAULT_OUTPUT_DIR = "result"

def parse_arguments():
    """
    Parse command line arguments

    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(description='BOSS job listing scraper')
    parser.add_argument('--driver-type', type=str, default=None,
                        choices=['chrome', 'edge', 'firefox'],
                        help='Specific type of browser driver to use (optional)')
    parser.add_argument('--output-dir', type=str, default=DEFAULT_OUTPUT_DIR,
                        help='Directory to save output files (default: current directory)')
    parser.add_argument('--headless', action='store_true',
                        help='Run browser in headless mode (no GUI)')
    return parser.parse_args()

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

    # Wait for manual verification
    print("Please complete the manual verification if required...", level="WARNING")
    time.sleep(15)  # Wait for 15 seconds to allow manual verification

    # Simulate clicking Internet/AI to show job categories
    show_ele = browser.find_element(by=By.XPATH, value='//div[contains(@class, "job-menu")]//b')
    show_ele.click()

    # Get all category elements
    category_elements = browser.find_elements(by=By.XPATH, value='//div[contains(@class, "job-menu")]//div/a')
    total_categories = len(category_elements)
    print(f"Found {total_categories} categories to process")

    for i in range(total_categories):
        try:
            print(f"Processing category index {i}")

            current_a = category_elements[i]
            current_category = current_a.find_element(by=By.XPATH, value='../../h4').text
            sub_category = current_a.text
            print(f"Scraping {current_category}--{sub_category}")

            # Click on the category
            current_a.click()

            # Scroll page to load all content
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(5, 15))
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Parse job listings
            parsed_data = parse_job_listings(browser, current_category, sub_category)

            if parsed_data:
                try:
                    # Try to save to primary storage
                    storage.save_data(parsed_data)
                except Exception as e:
                    # If primary storage fails, save to CSV
                    print(f"Primary storage failed: {str(e)}", level="ERROR")
                    print("Falling back to CSV storage")
                    storage.close()

            try:
                # Return to homepage
                browser.back()
                # Simulate clicking Internet/AI to show job categories
                show_ele = browser.find_element(by=By.XPATH, value='//div[contains(@class, "job-menu")]//b')
                show_ele.click()
                # Refresh category elements after going back
                category_elements = browser.find_elements(by=By.XPATH, value='//div[contains(@class, "job-menu")]//div/a')
            except:
                browser.get(index_url)
                # Wait for manual verification again if needed
                print("Please complete the manual verification if required...", level="WARNING")
                time.sleep(15)  # Wait for 15 seconds to allow manual verification
                # Simulate clicking Internet/AI to show job categories
                show_ele = browser.find_element(by=By.XPATH, value='//div[contains(@class, "job-menu")]//b')
                show_ele.click()
                # Refresh category elements after reloading
                category_elements = browser.find_elements(by=By.XPATH, value='//div[contains(@class, "job-menu")]//div/a')

        except Exception as e:
            print(f"Error processing category {i}: {str(e)}", level="ERROR")
            continue


def main():
    args = parse_arguments()

    # Initialize logger
    output_dir = args.output_dir if args.output_dir else os.path.join(os.getcwd(), DEFAULT_OUTPUT_DIR)
    loger.init_logger(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    # Initialize data storage
    storage = init_storage(output_dir)

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
