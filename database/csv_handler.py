#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @author  : jhzhong
# @time    : 2023/12/22 8:23
# @function: CSV handler for job listings.

import os
import csv
from datetime import datetime
import loger

class CSVHandler:
    def __init__(self, output_dir):
        """
        Initialize CSV handler
        
        Args:
            output_dir (str): Output directory for CSV files
        """
        self.output_dir = output_dir
        self.today = datetime.now().strftime('%Y-%m-%d')
        self.csv_file = os.path.join(output_dir, f'job_info_{self.today}.csv')
        self._ensure_csv_exists()

    def _ensure_csv_exists(self):
        """Ensure CSV file exists with headers"""
        if not os.path.exists(self.csv_file):
            headers = [
                'category', 'sub_category', 'job_title', 'province', 'job_location',
                'job_company', 'job_industry', 'job_finance', 'job_scale', 'job_welfare',
                'job_salary_range', 'job_experience', 'job_education', 'job_skills', 'create_time'
            ]
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(headers)

    def select_all(self, sql=None, args=None):
        """
        Query all data from CSV
        
        Args:
            sql (str): Not used in CSV handler
            args (tuple/list): Not used in CSV handler
            
        Returns:
            list: All data from CSV
        """
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                return list(reader)
        except Exception as e:
            print(f"Error reading CSV: {str(e)}", level="ERROR")
            raise

    def select_one(self, sql=None, args=None):
        """
        Query first record from CSV
        
        Args:
            sql (str): Not used in CSV handler
            args (tuple/list): Not used in CSV handler
            
        Returns:
            dict: First record from CSV
        """
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                return next(reader, None)
        except Exception as e:
            print(f"Error reading CSV: {str(e)}", level="ERROR")
            raise

    def select_n(self, sql=None, n=1, args=None):
        """
        Query first n records from CSV
        
        Args:
            sql (str): Not used in CSV handler
            n (int): Number of records to fetch
            args (tuple/list): Not used in CSV handler
            
        Returns:
            list: First n records from CSV
        """
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                return [row for _, row in zip(range(n), reader)]
        except Exception as e:
            print(f"Error reading CSV: {str(e)}", level="ERROR")
            raise

    def insert_data(self, sql=None, args=None):
        """
        Insert data into CSV
        
        Args:
            sql (str): Not used in CSV handler
            args (tuple/list): Data to insert
            
        Returns:
            int: Number of records inserted
        """
        try:
            with open(self.csv_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(args)
            return 1
        except Exception as e:
            print(f"Error writing to CSV: {str(e)}", level="ERROR")
            raise

    def insert_job_listing(self, data_row):
        """
        Insert a job listing into CSV
        
        Args:
            data_row (tuple): Data row to insert
            
        Returns:
            int: Number of records inserted
        """
        return self.insert_data(args=data_row)

    def update_data(self, sql=None, args=None):
        """
        Update data in CSV (Not supported)
        
        Args:
            sql (str): Not used in CSV handler
            args (tuple/list): Not used in CSV handler
            
        Returns:
            int: Always returns 0 as updates are not supported
        """
        print("Update operations are not supported for CSV storage", level="WARNING")
        return 0

    def delete_data(self, sql=None, args=None):
        """
        Delete data from CSV (Not supported)
        
        Args:
            sql (str): Not used in CSV handler
            args (tuple/list): Not used in CSV handler
            
        Returns:
            int: Always returns 0 as deletes are not supported
        """
        print("Delete operations are not supported for CSV storage", level="WARNING")
        return 0

    def create_database_and_table(self):
        """
        Create CSV file with headers if not exists
        
        Returns:
            bool: True if successful
        """
        self._ensure_csv_exists()
        return True

    def close(self):
        """Close handler (No-op for CSV)"""
        pass

    def save_data(self, data_rows):
        """
        Save multiple data rows to CSV
        
        Args:
            data_rows (list): List of data rows to save
        """
        try:
            with open(self.csv_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                for row in data_rows:
                    writer.writerow(row)
            print(f"Successfully saved {len(data_rows)} records to CSV")
        except Exception as e:
            print(f"Error saving data to CSV: {str(e)}", level="ERROR")
            raise

def test_csv_handler():
    """Test CSVHandler functionality"""
    # Create test directory
    test_dir = "test_output"
    os.makedirs(test_dir, exist_ok=True)
    
    try:
        # Initialize CSVHandler
        handler = CSVHandler(test_dir)
        
        # Test data
        test_data = [
            ("技术", "后端开发", "Python开发工程师", "北京", "海淀区",
             "测试公司", "互联网", "未融资", "100-499人", "五险一金",
             "15-30K", "3-5年", "本科", "Python,MySQL", "2023-12-22"),
            ("产品", "产品经理", "高级产品经理", "上海", "浦东新区",
             "科技公司", "金融", "B轮", "500-999人", "年终奖",
             "20-40K", "5-10年", "本科", "产品设计,数据分析", "2023-12-22")
        ]
        
        # Test single record insert
        print("\nTesting single record insert:")
        result = handler.insert_job_listing(test_data[0])
        print(f"Insertion result: {result}")
        
        # Test batch save
        print("\nTesting batch save:")
        handler.save_data(test_data)
        
        # Test select all records
        print("\nTesting select all records:")
        all_data = handler.select_all()
        print(f"Found {len(all_data)} records")
        for i, row in enumerate(all_data, 1):
            print(f"Record {i}: {row}")
        
        # Test select one record
        print("\nTesting select one record:")
        one_data = handler.select_one()
        print(f"First record: {one_data}")
        
        # Test select N records
        print("\nTesting select N records:")
        n_data = handler.select_n(n=2)
        print(f"First 2 records: {n_data}")
        
        # Test unsupported operations
        print("\nTesting unsupported operations:")
        update_result = handler.update_data()
        delete_result = handler.delete_data()
        print(f"Update operation result: {update_result}")
        print(f"Delete operation result: {delete_result}")
        
    finally:
        print(f"\nTest completed, save test files in {test_dir}.")

if __name__ == "__main__":
    test_csv_handler() 