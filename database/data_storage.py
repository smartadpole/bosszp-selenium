#!/usr/bin/python3
# encoding: utf-8
# @author: sunhao
# @contact: smartadpole@163.com
# @file: logging.py
# @time: 2025/4/27 10:30
# @function: Data storage module for job listings.

import os
from datetime import datetime
from database import MySQLHandler, CSVHandler
import loger

class DataStorage:
    def __init__(self, output_dir, storage_type='mysql', db_config=None):
        """
        Initialize data storage
        
        Args:
            output_dir (str): Base output directory
            storage_type (str): Storage type, 'mysql' or 'csv'
            db_config (dict): Database configuration if using MySQL
        """
        self.output_dir = output_dir
        self.storage_type = storage_type
        self.db_config = db_config
        
        # Create output directories
        self.mysql_dir = os.path.join(output_dir, 'mysql')
        self.csv_dir = os.path.join(output_dir, 'csv')
        os.makedirs(self.mysql_dir, exist_ok=True)
        os.makedirs(self.csv_dir, exist_ok=True)
        
        # Initialize storage handler
        if storage_type == 'mysql':
            if not db_config:
                raise ValueError("Database configuration is required for MySQL storage")
            self.handler = MySQLHandler(**db_config)
            self.handler.create_database_and_table()
        else:
            self.handler = CSVHandler(self.csv_dir)

    def save_data(self, data_rows):
        """
        Save data using configured storage handler
        
        Args:
            data_rows (list): List of data rows to save
        """
        try:
            if self.storage_type == 'mysql':
                # Add create_time to each row
                today = datetime.now().strftime('%Y-%m-%d')
                for row in data_rows:
                    row_with_time = row + (today,)
                    self.handler.insert_job_listing(row_with_time)
            else:
                self.handler.save_data(data_rows)
                
            print(f"Successfully saved {len(data_rows)} records using {self.storage_type} storage")
        except Exception as e:
            print(f"Error saving data: {str(e)}", level="ERROR")
            # If MySQL fails, try CSV as fallback
            if self.storage_type == 'mysql':
                print("Trying CSV as fallback storage...")
                csv_handler = CSVHandler(self.csv_dir)
                csv_handler.save_data(data_rows)
            else:
                raise

    def close(self):
        """Close storage handler"""
        if hasattr(self.handler, 'close'):
            self.handler.close()

    def query_data(self, sql, args=None, n=None):
        """
        Query data from storage
        
        Args:
            sql (str): SQL query
            args (tuple/list): Query parameters
            n (int): Number of records to fetch (None for all)
            
        Returns:
            list/dict: Query results
        """
        if self.storage_type != 'mysql':
            raise ValueError("Query operations are only supported for MySQL storage")
            
        try:
            if n is None:
                return self.handler.select_all(sql, args)
            elif n == 1:
                return self.handler.select_one(sql, args)
            else:
                return self.handler.select_n(sql, n, args)
        except Exception as e:
            print(f"Error querying data: {str(e)}", level="ERROR")
            raise

    def update_data(self, sql, args=None):
        """
        Update data in storage
        
        Args:
            sql (str): SQL update statement
            args (tuple/list): Update parameters
            
        Returns:
            int: Number of affected rows
        """
        if self.storage_type != 'mysql':
            raise ValueError("Update operations are only supported for MySQL storage")
            
        try:
            return self.handler.update_data(sql, args)
        except Exception as e:
            print(f"Error updating data: {str(e)}", level="ERROR")
            raise

    def delete_data(self, sql, args=None):
        """
        Delete data from storage
        
        Args:
            sql (str): SQL delete statement
            args (tuple/list): Delete parameters
            
        Returns:
            int: Number of affected rows
        """
        if self.storage_type != 'mysql':
            raise ValueError("Delete operations are only supported for MySQL storage")
            
        try:
            return self.handler.delete_data(sql, args)
        except Exception as e:
            print(f"Error deleting data: {str(e)}", level="ERROR")
            raise

def init_storage(output_dir):
    """
    Initialize data storage (MySQL or CSV)

    Args:
        output_dir (str): Directory for output files

    Returns:
        storage: Initialized storage instance
    """
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
        print(f"MySQL connection failed: {str(e)}", level="WARNING")
        print("Switching to CSV storage mode", level="WARNING")
        storage = CSVHandler(output_dir)
        storage.create_database_and_table()
        print("Successfully initialized CSV storage")

    return storage
