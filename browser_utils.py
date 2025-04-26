#!/usr/bin/python3
# encoding: utf-8
'''
@author: sunhao
@contact: smartadpole@163.com
@file: logging.py
@time: 2025/4/27 01:20
@desc:
'''

import os
import sys
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import loger

# System driver directories to search
SYSTEM_DRIVER_DIRS = [
    '/usr/bin',
    '/usr/local/bin',
    '/opt/homebrew/bin',  # macOS
    os.path.expanduser('~/.local/bin'),  # User local bin
]

def find_driver(driver_dir=None):
    """
    Find available browser drivers in the specified directory or system directories
    
    Args:
        driver_dir (str, optional): Specific directory to search. If None, searches system directories
        
    Returns:
        dict: Dictionary of found drivers with their paths
    """
    drivers = {}
    search_dirs = [driver_dir] if driver_dir else SYSTEM_DRIVER_DIRS
    
    for dir_path in search_dirs:
        if not os.path.exists(dir_path):
            continue
            
        for file in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file)
            if os.path.isfile(file_path) and os.access(file_path, os.X_OK):
                if 'chromedriver' in file.lower():
                    drivers['chrome'] = file_path
                elif 'msedgedriver' in file.lower():
                    drivers['edge'] = file_path
                elif 'geckodriver' in file.lower():
                    drivers['firefox'] = file_path
                    
    return drivers

def init_browser(driver_path):
    """
    Initialize browser based on the driver type
    
    Args:
        driver_path (str): Path to the browser driver
        
    Returns:
        webdriver: Initialized browser instance or None if failed
    """
    try:
        # Common options for all browsers
        common_args = ['--no-sandbox', '--disable-dev-shm-usage']
        
        if 'chromedriver' in driver_path.lower():
            # Import Chrome specific modules
            from selenium.webdriver.chrome.service import Service as ChromeService
            from selenium.webdriver.chrome.options import Options as ChromeOptions
            
            # Chrome setup
            options = ChromeOptions()
            for arg in common_args:
                options.add_argument(arg)
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            service = ChromeService(executable_path=driver_path)
            browser = webdriver.Chrome(service=service, options=options)
            
        elif 'msedgedriver' in driver_path.lower():
            # Import Edge specific modules
            from selenium.webdriver.edge.service import Service as EdgeService
            from selenium.webdriver.edge.options import Options as EdgeOptions
            
            # Edge setup
            options = EdgeOptions()
            for arg in common_args:
                options.add_argument(arg)
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            service = EdgeService(executable_path=driver_path)
            browser = webdriver.Edge(service=service, options=options)
            
        elif 'geckodriver' in driver_path.lower():
            # Import Firefox specific modules
            from selenium.webdriver.firefox.service import Service as FirefoxService
            from selenium.webdriver.firefox.options import Options as FirefoxOptions
            
            # Firefox setup
            options = FirefoxOptions()
            for arg in common_args:
                options.add_argument(arg)
            options.add_argument('--headless')
            service = FirefoxService(executable_path=driver_path)
            browser = webdriver.Firefox(service=service, options=options)
            
        else:
            print(f"Unsupported driver type: {driver_path}")
            return None
            
        return browser
        
    except WebDriverException as e:
        print(f"Failed to initialize browser: {e}", level="ERROR")
        return None
    except ImportError as e:
        print(f"Failed to import required modules: {e}", level="WARNING")
        return None

def get_browser(driver_dir=None):
    """
    Get a browser instance by searching for available drivers
    
    Args:
        driver_dir (str, optional): Specific directory to search for drivers
        
    Returns:
        webdriver: Initialized browser instance or None if failed
    """
    # Find available drivers
    drivers = find_driver(driver_dir)
    if not drivers:
        print("No supported browser drivers found in system directories", level="WARNING")
        return None
        
    # Try to initialize browser with available drivers
    for browser_type, driver_path in drivers.items():
        print(f"Trying to initialize {browser_type} browser...")
        browser = init_browser(driver_path)
        if browser:
            print(f"Successfully initialized {browser_type} browser")
            return browser
            
    print("Failed to initialize any browser")
    return None 