#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @author  : jhzhong
# @time    : 2023/12/22 8:23
# @function: MySQL database handler for job listings.

import pymysql
import loger

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
        self.conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port,
            charset=charset
        )
        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)

    def create_database_and_table(self):
        """Create database and table if not exists"""
        try:
            # Create database
            self.cursor.execute("CREATE DATABASE IF NOT EXISTS spider_db")
            self.cursor.execute("USE spider_db")
            
            # Create table
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS job_info (
                id INT AUTO_INCREMENT PRIMARY KEY,
                category VARCHAR(255) NULL COMMENT 'Primary category',
                sub_category VARCHAR(255) NULL COMMENT 'Secondary category',
                job_title VARCHAR(255) NULL COMMENT 'Job title',
                province VARCHAR(100) NULL COMMENT 'Province',
                job_location VARCHAR(255) NULL COMMENT 'Job location',
                job_company VARCHAR(255) NULL COMMENT 'Company name',
                job_industry VARCHAR(255) NULL COMMENT 'Industry type',
                job_finance VARCHAR(255) NULL COMMENT 'Financing status',
                job_scale VARCHAR(255) NULL COMMENT 'Company size',
                job_welfare VARCHAR(255) NULL COMMENT 'Company benefits',
                job_salary_range VARCHAR(255) NULL COMMENT 'Salary range',
                job_experience VARCHAR(255) NULL COMMENT 'Work experience',
                job_education VARCHAR(255) NULL COMMENT 'Education requirement',
                job_skills VARCHAR(255) NULL COMMENT 'Skill requirements',
                create_time VARCHAR(50) NULL COMMENT 'Crawl time',
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
            data_row (tuple): Data row to insert
            
        Returns:
            int: Number of affected rows
        """
        sql = """
        INSERT INTO job_info(
            category, sub_category, job_title, province, job_location,
            job_company, job_industry, job_finance, job_scale, job_welfare,
            job_salary_range, job_experience, job_education, job_skills, create_time
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        return self.insert_data(sql, data_row)

    def close(self):
        """Close database connection"""
        self.cursor.close()
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