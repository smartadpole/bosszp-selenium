#!/usr/bin/python3 python
# encoding: utf-8
'''
@author: 孙昊
@contact: smartadpole@163.com
@file: logging.py
@time: 2025/4/27 00:14
@desc: 
'''
import sys, os

CURRENT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.join(CURRENT_DIR, '../'))


import builtins
import logging
import os
import sys


COLORS = {
        'DEBUG': '\033[94m',     # Blue
        # 'INFO': '\033[92m',      # Green
        'WARNING': '\033[93m',   # Yellow
        'ERROR': '\033[91m',     # Red
        'CRITICAL': '\033[41m',  # Red background with white text
        'RESET': '\033[97m'      # Reset to white, origin is 0m
}

class ColoredFormatter(logging.Formatter):
    """Custom colored formatter"""
    def format(self, record):
        levelname = record.levelname
        msg = super().format(record)
        return f"{COLORS.get(levelname, COLORS['RESET'])}{msg}{COLORS['RESET']}"

def setup_colored_logging():
    """Set up colored logging output"""
    console = logging.StreamHandler()
    console.setFormatter(ColoredFormatter('%(asctime)s [%(levelname)s] %(message)s'))

    file_handler = logging.FileHandler("boss_scraper.log")
    file_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    if logger.handlers:
        logger.handlers = []

    logger.addHandler(console)
    logger.addHandler(file_handler)

original_print = builtins.print

def print_to_logging(*args, level="INFO", **kwargs):
    for k in ['end', 'flush']:
        kwargs.pop(k, None)

    caller = f"[{os.path.basename(sys._getframe(1).f_globals['__file__'])}:{sys._getframe(1).f_lineno}] "
    message = caller + ' '.join(str(arg) for arg in args)

    log_level = level.upper() if isinstance(level, str) else level
    if log_level == "DEBUG" or log_level == logging.DEBUG:
        logging.debug(message)
    elif log_level == "WARNING" or log_level == logging.WARNING:
        logging.warning(message)
    elif log_level == "ERROR" or log_level == logging.ERROR:
        logging.error(message)
    elif log_level == "CRITICAL" or log_level == logging.CRITICAL:
        logging.critical(message)
    else:
        logging.info(message)

setup_colored_logging()
builtins.print = print_to_logging


def main():
    print("This is a print message.")


if __name__ == '__main__':
    main()
