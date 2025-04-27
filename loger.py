#!/usr/bin/python3 python
# encoding: utf-8
'''
@author: sunhao
@contact: smartadpole@163.com
@file: logging.py
@time: 2025/4/27 00:14
@desc: Logging module for the project
'''
import sys
import os
import builtins
import logging
from logging.handlers import RotatingFileHandler

DEFAULT_OUTPUT_DIR = './'
LOG_FILE = 'scraper.log'
DEFAULT_FILE_SIZE = 1000 # 1000MB

COLORS = {
    'DEBUG': '\033[94m',     # Blue
    'WARNING': '\033[93m',   # Yellow
    'ERROR': '\033[91m',     # Red
    'CRITICAL': '\033[41m',  # Red background with white text
    'RESET': '\033[97m'      # Reset to white
}

class ColoredFormatter(logging.Formatter):
    """Custom colored formatter"""
    def format(self, record):
        levelname = record.levelname
        msg = super().format(record)
        return f"{COLORS.get(levelname, COLORS['RESET'])}{msg}{COLORS['RESET']}"

class Logger:
    """Logger class for managing logging configuration"""
    
    def __init__(self):
        self.output_dir = DEFAULT_OUTPUT_DIR
        self.log_file = os.path.join(self.output_dir, LOG_FILE)
        self._setup_logging()
        
    def set_output_dir(self, output_dir):
        """Set output directory for logs"""
        if os.path.exists(self.log_file):
            os.remove(self.log_file)
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.log_file = os.path.join(self.output_dir, LOG_FILE)
        self._setup_logging()
        
    def _setup_logging(self):
        """Setup logging configuration"""
        # Create console handler
        console = logging.StreamHandler()
        console.setFormatter(ColoredFormatter('%(asctime)s [%(levelname)s] %(message)s'))

        # Create file handler
        file_handler = RotatingFileHandler(
            self.log_file,
            maxBytes=DEFAULT_FILE_SIZE*1024*1024,  # XX MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))

        # Configure root logger
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        # Clear existing handlers
        if logger.handlers:
            logger.handlers = []

        # Add handlers
        logger.addHandler(console)
        logger.addHandler(file_handler)

# Create global logger manager instance
logger_manager = Logger()

def print_to_logging(*args, level="INFO", **kwargs):
    """Custom print function that logs messages"""
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

# replace print
builtins.print = print_to_logging

def init_logger(output_dir):
    """Initialize logger with custom output directory"""
    logger_manager.set_output_dir(output_dir)

def main():
    """Test function"""
    print("This is a test message")
    print("This is an error message", level="ERROR")

if __name__ == '__main__':
    main()
