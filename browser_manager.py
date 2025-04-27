#!/usr/bin/python3
# encoding: utf-8
# @author: sunhao
# @contact: smartadpole@163.com
# @file: logging.py
# @time: 2025/4/27 01:20
# @function: Browser manager for handling browser drivers and version compatibility.

import os
import sys
import platform
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import loger
import time

# Browser configuration constants
BROWSER_CONFIGS = {
    'chrome': {
        'name': 'Google Chrome',
        'windows_reg_path': r"Software\Google\Chrome\BLBeacon",
        'mac_path': '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        'linux_cmd': 'google-chrome',
        'driver_manager': ChromeDriverManager,
        'service_class': ChromeService,
        'options_class': ChromeOptions
    },
    'edge': {
        'name': 'Microsoft Edge',
        'windows_reg_path': r"Software\Microsoft\Edge\BLBeacon",
        'mac_path': '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
        'linux_cmd': 'microsoft-edge',
        'driver_manager': EdgeChromiumDriverManager,
        'service_class': EdgeService,
        'options_class': EdgeOptions
    },
    'firefox': {
        'name': 'Mozilla Firefox',
        'windows_reg_path': r"Software\Mozilla\Mozilla Firefox",
        'mac_path': '/Applications/Firefox.app/Contents/MacOS/firefox',
        'linux_cmd': 'firefox',
        'driver_manager': GeckoDriverManager,
        'service_class': FirefoxService,
        'options_class': FirefoxOptions
    }
}

# Common browser arguments
COMMON_BROWSER_ARGS = ['--no-sandbox', '--disable-dev-shm-usage']  # , '--headless']


class BrowserManager:
    """Browser manager class for handling browser drivers and initialization"""

    def __init__(self):
        self.browser_versions = {}
        self.driver_paths = {}

    def _get_windows_version(self, reg_path):
        """Get browser version from Windows registry"""
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path)
        version, _ = winreg.QueryValueEx(key, "version")
        return version

    def _get_mac_version(self, app_path):
        """Get browser version on macOS"""
        process = subprocess.Popen([app_path, '--version'], stdout=subprocess.PIPE)
        version = process.communicate()[0].decode('UTF-8').replace(f"{BROWSER_CONFIGS['chrome']['name']} ",
                                                                   '').strip()
        return version

    def _get_linux_version(self, cmd):
        """Get browser version on Linux"""
        process = subprocess.Popen([cmd, '--version'], stdout=subprocess.PIPE)
        version = process.communicate()[0].decode('UTF-8').replace(f"{BROWSER_CONFIGS['chrome']['name']} ", '').strip()
        return version

    def check_type(self, browser_type):
        return browser_type in BROWSER_CONFIGS

    def get_browser_version(self, browser_type):
        """
        Get the version of specified browser

        Args:
            browser_type (str): Type of browser ('chrome', 'edge', 'firefox')

        Returns:
            str: Browser version or None if not found
        """
        config = BROWSER_CONFIGS[browser_type]
        try:
            if platform.system() == "Windows":
                return self._get_windows_version(config['windows_reg_path'])
            elif platform.system() == "Darwin":  # macOS
                return self._get_mac_version(config['mac_path'])
            else:  # Linux
                return self._get_linux_version(config['linux_cmd'])
        except Exception as e:
            print(f"Failed to get {browser_type} version: {e}", level="ERROR")
            return None

    def get_driver_path(self, browser_type):
        """
        Get or download driver path for specified browser

        Args:
            browser_type (str): Type of browser ('chrome', 'edge', 'firefox')

        Returns:
            str: Path to driver executable or None if failed
        """
        try:
            # default maybe in ~/.wdm/drivers/[browser_type]/[os]/[version]/
            # e.g. ChromeDriverManager.install()
            return BROWSER_CONFIGS[browser_type]['driver_manager']().install()
        except Exception as e:
            print(f"Failed to get {browser_type} driver: {e}", level="ERROR")
            return None

    def init_browser(self, browser_type):
        """
        Initialize browser with appropriate driver

        Args:
            browser_type (str): Type of browser ('chrome', 'edge', 'firefox')

        Returns:
            webdriver: Initialized browser instance or None if failed
        """
        if not self.check_type(browser_type):
            return None

        try:
            config = BROWSER_CONFIGS[browser_type]
            options = config['options_class']()
            for arg in COMMON_BROWSER_ARGS:
                options.add_argument(arg)

            driver_path = self.get_driver_path(browser_type)
            service = config['service_class'](driver_path)
            return webdriver.__dict__[browser_type.capitalize()](service=service, options=options)

        except Exception as e:
            print(f"Failed to initialize {browser_type} browser: {e}", level="ERROR")
            return None

    def get_available_browser(self):
        """
        Try to initialize any available browser

        Returns:
            webdriver: Initialized browser instance or None if all failed
        """
        for browser_type in BROWSER_CONFIGS.keys():
            print(f"Trying to initialize {browser_type} browser...")
            version = self.get_browser_version(browser_type)
            if version:
                print(f"Detected {browser_type} version: {version}")
                browser = self.init_browser(browser_type)
                if browser:
                    print(f"Successfully initialized {browser_type} browser")
                    return browser

        print("no available browser", level="ERROR")
        return None

def get_browser(driver_type=None):
    """
    Get a browser instance with automatic driver management

    Args:
        driver_type (str, optional): Browser type ('chrome', 'edge', 'firefox')
                                    If None, will try all available browsers

    Returns:
        webdriver: Initialized browser instance or None if failed
    """
    manager = BrowserManager()

    if driver_type:
        if not manager.check_type(driver_type):
            print(f"Unsupported browser type: {driver_type}", level="ERROR")
            return None

        print(f"Initializing {driver_type} browser...")
        return manager.init_browser(driver_type)

    # If no browser type specified, try all available browsers
    return manager.get_available_browser()


def show_browser(browser):
    browser.get("https://www.bing.com")
    print("Opened Bing homepage")

    while True:
        try:
            browser.current_url
            time.sleep(1)
        except:
            print("Browser closed")
            break

if __name__ == '__main__':
    # Test browser initialization and open Bing homepage
    browser = get_browser()
    if browser:
        print("Browser initialized successfully")
        show_browser(browser)
        try:
            browser.quit()
        except:
            pass
    else:
        print("Failed to initialize browser", level="ERROR")
