#!/usr/bin/python3
# encoding: utf-8
# @author: sunhao
# @contact: smartadpole@163.com
# @file: company_crawler.py
# @time: 2025/4/27 10:30
# @function: Company information crawler for BOSS.

import os
import time
import argparse
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import loger
from database.company_storage import init_company_storage
from browser_manager import get_browser
import random

DEFAULT_OUTPUT_DIR = "result"

def parse_arguments():
    """
    Parse command line arguments

    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(description='BOSS company information crawler')
    parser.add_argument('--driver-type', type=str, default=None,
                        choices=['chrome', 'edge', 'firefox'],
                        help='Specific type of browser driver to use (optional)')
    parser.add_argument('--output-dir', type=str, default=DEFAULT_OUTPUT_DIR,
                        help='Directory to save output files (default: current directory)')
    parser.add_argument('--headless', action='store_true',
                        help='Run browser in headless mode (no GUI)')
    parser.add_argument('--company', type=str, required=True,
                        help='Company name to search for')
    return parser.parse_args()

def save_company_markdown(company_info, output_dir):
    """
    Save company information to markdown file
    
    Args:
        company_info (dict): Company information
        output_dir (str): Output directory
    """
    try:
        # Create company directory
        company_dir = os.path.join(output_dir, 'companies', company_info['name'])
        os.makedirs(company_dir, exist_ok=True)
        
        # Generate markdown content
        markdown_content = f"""# {company_info['name']}

## 基本信息
- 行业：{company_info['industry']}
- 规模：{company_info['size']}
- 融资阶段：{company_info['stage']}
- 地址：{company_info['address']}

## 公司简介
{company_info['description']}

## 公司福利
{chr(10).join(f"- {benefit}" for benefit in company_info['benefits'])}

## 在招岗位
"""
        
        # Save markdown file
        markdown_file = os.path.join(company_dir, f"{company_info['name']}.md")
        with open(markdown_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
            
        print(f"Successfully saved company information to {markdown_file}")
        return markdown_file
    except Exception as e:
        print(f"Error saving company markdown: {str(e)}", level="ERROR")
        return None

def save_job_markdown(job_listings, company_name, output_dir):
    """
    Save job listings to markdown file
    
    Args:
        job_listings (list): List of job listings
        company_name (str): Company name
        output_dir (str): Output directory
    """
    try:
        # Create company directory
        company_dir = os.path.join(output_dir, 'companies', company_name)
        os.makedirs(company_dir, exist_ok=True)
        
        # Generate markdown content
        markdown_content = f"""# {company_name} 在招岗位

"""
        
        for job in job_listings:
            markdown_content += f"""## {job['title']}

### 基本信息
- 薪资：{job['salary']}
- 地点：{job['location']}
- 经验要求：{job['experience']}
- 学历要求：{job['education']}

### 岗位描述
{job['description']}

### 技能要求
{chr(10).join(f"- {skill}" for skill in job['skills'])}

---
"""
        
        # Save markdown file
        markdown_file = os.path.join(company_dir, f"{company_name}_jobs.md")
        with open(markdown_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
            
        print(f"Successfully saved job listings to {markdown_file}")
        return markdown_file
    except Exception as e:
        print(f"Error saving job markdown: {str(e)}", level="ERROR")
        return None

def scrape_company_info(browser, company_name, storage):
    """
    Scrape company information and job listings
    
    Args:
        browser (webdriver): Browser instance
        company_name (str): Company name to search for
        storage: Company storage instance
    """
    try:
        # Open BOSS search page
        search_url = f'https://www.zhipin.com/web/geek/jobs?query={company_name}'
        browser.get(search_url)
        print("Successfully accessed BOSS search page")
        
        # Wait for manual verification
        print("Please complete the manual verification if required...", level="WARNING")
        time.sleep(15)  # Wait for 15 seconds to allow manual verification
        
        # Wait for search results to load
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".c-company-card"))
        )
        
        # Find company link in search results
        company_links = browser.find_elements(By.CSS_SELECTOR, ".c-company-card .card-content")
        if not company_links:
            print(f"No company found with name: {company_name}", level="ERROR")
            return
            
        # Click on the first company link
        company_links[0].click()
        
        # Wait for company page to load
        time.sleep(5)
        
        # Parse company information
        company_info = parse_company_info(browser)
        if company_info:
            # Save company information
            storage.save_company_info(company_info)
        
        # Parse job listings
        job_listings = parse_job_listings(browser)
        if job_listings:
            # Save job listings
            storage.save_job_listings(job_listings, company_name)
            
    except Exception as e:
        print(f"Error scraping company info: {str(e)}", level="ERROR")

def parse_company_info(browser):
    """
    Parse company information from the company page
    
    Args:
        browser (webdriver): Browser instance
        
    Returns:
        dict: Company information
    """
    try:
        # Wait for company info to load
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".c-company-card"))
        )
        
        company_info = {}
        
        # Basic company info
        company_info['name'] = browser.find_element(By.CSS_SELECTOR, ".company-name").text
        company_info['industry'] = browser.find_element(By.CSS_SELECTOR, ".company-info-tag:nth-child(3)").text
        company_info['size'] = browser.find_element(By.CSS_SELECTOR, ".company-info-tag:nth-child(2)").text
        company_info['stage'] = browser.find_element(By.CSS_SELECTOR, ".company-info-tag:nth-child(1)").text
        
        # Company description and benefits will be in the company detail page
        company_info['description'] = ""
        company_info['benefits'] = []
        
        # Company address will be in the job detail page
        company_info['address'] = ""
        
        return company_info
    except Exception as e:
        print(f"Error parsing company info: {str(e)}", level="ERROR")
        return None

def parse_job_listings(browser):
    """
    Parse job listings from the company page
    
    Args:
        browser (webdriver): Browser instance
        
    Returns:
        list: List of job listings
    """
    try:
        # Wait for job listings to load
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".job-card-box"))
        )
        
        job_listings = []
        job_elements = browser.find_elements(By.CSS_SELECTOR, ".job-card-box")
        
        for job in job_elements:
            job_info = {}
            
            # Basic job info
            job_info['title'] = job.find_element(By.CSS_SELECTOR, ".job-name").text
            job_info['salary'] = job.find_element(By.CSS_SELECTOR, ".job-salary").text
            
            # Location and requirements
            tags = job.find_elements(By.CSS_SELECTOR, ".tag-list li")
            if len(tags) >= 2:
                job_info['experience'] = tags[0].text
                job_info['education'] = tags[1].text
            
            # Click on job to get more details
            job_link = job.find_element(By.CSS_SELECTOR, ".job-name")
            job_link.click()
            
            # Wait for job detail to load
            time.sleep(2)
            
            try:
                # Get job description
                job_info['description'] = browser.find_element(By.CSS_SELECTOR, ".job-detail-body .desc").text
                
                # Get job skills
                skills = browser.find_elements(By.CSS_SELECTOR, ".job-label-list li")
                job_info['skills'] = [skill.text for skill in skills]
                
                # Get company address
                address = browser.find_element(By.CSS_SELECTOR, ".job-address-desc").text
                job_info['location'] = address
                
            except Exception as e:
                print(f"Error parsing job details: {str(e)}", level="ERROR")
            
            job_listings.append(job_info)
            
            # Go back to job list
            browser.back()
            time.sleep(1)
            
        return job_listings
    except Exception as e:
        print(f"Error parsing job listings: {str(e)}", level="ERROR")
        return []

def main():
    args = parse_arguments()

    # Initialize logger
    output_dir = args.output_dir if args.output_dir else os.path.join(os.getcwd(), DEFAULT_OUTPUT_DIR)
    loger.init_logger(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    # Initialize company storage
    storage = init_company_storage(output_dir)

    try:
        # Initialize browser
        browser = get_browser(args.driver_type)
        print(f"Successfully initialized {args.driver_type} browser")

        # Start scraping
        scrape_company_info(browser, args.company, storage)

    except Exception as e:
        print(f"Program execution error: {str(e)}", level="ERROR")
    finally:
        # Close browser
        if 'browser' in locals():
            browser.quit()
        print("Crawling completed")

if __name__ == "__main__":
    main() 