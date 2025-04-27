#!/usr/bin/python3
# encoding: utf-8
# @author: sunhao
# @contact: smartadpole@163.com
# @file: logging.py
# @time: 2025/4/27 10:30
# @function: MySQL database handler for job listings.

import pymysql
import loger
from datetime import datetime

# 定义表列信息
JOB_INFO_COLUMNS = [
    ('category', 'VARCHAR(255)', 'Primary category'),
    ('sub_category', 'VARCHAR(255)', 'Secondary category'),
    ('job_title', 'VARCHAR(255)', 'Job title'),
    ('province', 'VARCHAR(100)', 'Province'),
    ('job_location', 'VARCHAR(255)', 'Job location'),
    ('job_company', 'VARCHAR(255)', 'Company name'),
    ('job_industry', 'VARCHAR(255)', 'Industry type'),
    ('job_finance', 'VARCHAR(255)', 'Financing status'),
    ('job_scale', 'VARCHAR(255)', 'Company size'),
    ('job_welfare', 'VARCHAR(255)', 'Company benefits'),
    ('job_salary_range', 'VARCHAR(255)', 'Salary range'),
    ('job_experience', 'VARCHAR(255)', 'Work experience'),
    ('job_education', 'VARCHAR(255)', 'Education requirement'),
    ('job_skills', 'VARCHAR(255)', 'Skill requirements'),
    ('job_address', 'VARCHAR(255)', 'Job address'),
    ('job_salary', 'VARCHAR(255)', 'Salary'),
    ('job_desc', 'TEXT', 'Job description'),
    ('create_time', 'VARCHAR(50)', 'Crawl time')
]

# 获取列名列表
COLUMN_NAMES = [col[0] for col in JOB_INFO_COLUMNS]

class MySQLHandler:
    def __init__(self, host, user, password, database, port=3306, charset='utf8mb4'):
        """
        Initialize MySQL handler
        
        Args:
            host (str): Database host
            user (str): Database user
            password (str): Database password
            database (str): Database name
            port (int): Database port
            charset (str): Database charset
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.charset = charset
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        """Connect to database"""
        try:
            self.conn = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
                charset=self.charset
            )
            self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        except Exception as e:
            print(f"Error connecting to database: {str(e)}", level="WARNING")
            raise

    def create_database_and_table(self):
        """Create database and table if not exists"""
        try:
            # Create database
            self.cursor.execute("CREATE DATABASE IF NOT EXISTS spider_db")
            self.cursor.execute("USE spider_db")
            
            # Create table
            create_table_sql = f"""
            CREATE TABLE IF NOT EXISTS job_info (
                id INT AUTO_INCREMENT PRIMARY KEY,
                {', '.join([f"{col[0]} {col[1]} NULL COMMENT '{col[2]}'" for col in JOB_INFO_COLUMNS])},
                INDEX idx_category (category),
                INDEX idx_job_title (job_title),
                INDEX idx_job_company (job_company)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """
            self.cursor.execute(create_table_sql)
            self.conn.commit()
            print("Database and table created successfully")
        except Exception as e:
            self.conn.rollback()
            print(f"Error creating database and table: {str(e)}", level="ERROR")
            raise

    def insert_data(self, sql, args=None):
        """
        Insert data
        
        Args:
            sql (str): SQL insert statement
            args (tuple/list): Insert parameters
            
        Returns:
            int: Number of affected rows
        """
        try:
            self.cursor.execute(sql, args)
            self.conn.commit()
            return self.cursor.rowcount
        except Exception as e:
            self.conn.rollback()
            print(f"Error inserting data: {str(e)}", level="ERROR")
            raise

    def insert_job_listing(self, data_row):
        """
        Insert a job listing into the database
        
        Args:
            data_row (dict): Data row to insert
            
        Returns:
            int: Number of affected rows
        """
        if isinstance(data_row, dict):
            # Convert dictionary to tuple using column names
            current_time = datetime.now().strftime('%Y-%m-%d')
            data_tuple = tuple(data_row.get(col, '') for col in COLUMN_NAMES[:-1]) + (data_row.get('create_time', current_time),)
        else:
            data_tuple = data_row

        # Generate SQL using column names
        columns = ', '.join(COLUMN_NAMES)
        placeholders = ', '.join(['%s'] * len(COLUMN_NAMES))
        sql = f"INSERT INTO job_info({columns}) VALUES ({placeholders})"
        
        return self.insert_data(sql, data_tuple)

    def save_data(self, data_rows):
        """
        Save multiple data rows to database
        
        Args:
            data_rows (list): List of data rows to save (can be dict or tuple)
        """
        try:
            # Convert all rows to tuples if they are dictionaries
            converted_rows = []
            current_time = datetime.now().strftime('%Y-%m-%d')
            
            for row in data_rows:
                if isinstance(row, dict):
                    # Convert dictionary to tuple using column names
                    converted_row = tuple(row.get(col, '') for col in COLUMN_NAMES[:-1]) + (row.get('create_time', current_time),)
                    converted_rows.append(converted_row)
                else:
                    converted_rows.append(row)

            # Generate SQL using column names
            columns = ', '.join(COLUMN_NAMES)
            placeholders = ', '.join(['%s'] * len(COLUMN_NAMES))
            sql = f"INSERT INTO job_info({columns}) VALUES ({placeholders})"
            
            self.cursor.executemany(sql, converted_rows)
            self.conn.commit()
            print(f"Successfully saved {len(converted_rows)} records to MySQL")
        except Exception as e:
            self.conn.rollback()
            print(f"Error saving data to MySQL: {str(e)}", level="ERROR")
            raise

    def close(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def select_all(self, sql, args=None):
        """
        Query all data
        
        Args:
            sql (str): SQL query
            args (tuple/list): Query parameters
            
        Returns:
            list: Query results
        """
        try:
            self.cursor.execute(sql, args)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error querying data: {str(e)}", level="ERROR")
            raise

    def select_one(self, sql, args=None):
        """
        Query single data
        
        Args:
            sql (str): SQL query
            args (tuple/list): Query parameters
            
        Returns:
            dict: Query result
        """
        try:
            self.cursor.execute(sql, args)
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Error querying data: {str(e)}", level="ERROR")
            raise

    def select_n(self, sql, n, args=None):
        """
        Query first n data
        
        Args:
            sql (str): SQL query
            n (int): Number of records to fetch
            args (tuple/list): Query parameters
            
        Returns:
            list: Query results
        """
        try:
            self.cursor.execute(sql, args)
            return self.cursor.fetchmany(n)
        except Exception as e:
            print(f"Error querying data: {str(e)}", level="ERROR")
            raise

    def update_data(self, sql, args=None):
        """
        Update data
        
        Args:
            sql (str): SQL update statement
            args (tuple/list): Update parameters
            
        Returns:
            int: Number of affected rows
        """
        try:
            self.cursor.execute(sql, args)
            self.conn.commit()
            return self.cursor.rowcount
        except Exception as e:
            self.conn.rollback()
            print(f"Error updating data: {str(e)}", level="ERROR")
            raise

    def delete_data(self, sql, args=None):
        """
        Delete data
        
        Args:
            sql (str): SQL delete statement
            args (tuple/list): Delete parameters
            
        Returns:
            int: Number of affected rows
        """
        try:
            self.cursor.execute(sql, args)
            self.conn.commit()
            return self.cursor.rowcount
        except Exception as e:
            self.conn.rollback()
            print(f"Error deleting data: {str(e)}", level="ERROR")
            raise 