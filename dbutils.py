#!/usr/bin/python
# -*- coding:utf-8 -*-
# @author  : jhzhong
# @time    : 2023/11/30 17:15
# @function: the script is used to do something.
# @version : V1
"""Define DBUtils utility class, encapsulating MySQL database common operations API

    - Method 1(select_all): Query all data
    - Method 2(select_one): Query one data
    - Method 3(select_n): Query first n data
    - Method 4(insert_data): Insert data
    - Method 5(update_data): Update data
    - Method 6(delete_data): Delete data
"""
import pymysql


class DBUtils:
    def __init__(self, host, user, password, db, port=3306, charset='utf8'):
        """
        DBUtils initialization method, called by default when instantiating DBUtils class, only called once
        """
        # Initialize operations, such as establishing database connection
        self.conn = pymysql.connect(host=host, user=user, password=password, db=db, port=port, charset=charset)
        # Get cursor pymysql.cursors.DictCursor specifies return value type as dictionary type
        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)

    def select_all(self, sql, args=None):
        """
        Query all data
        :param sql: SQL for querying data
        :param args: Parameters, can only be tuple or list
        :return: Return result set
        """
        self.cursor.execute(sql, args)
        result = self.cursor.fetchall()
        return result

    def select_n(self, sql, n, args=None):
        """
        Query first n data that meet the conditions
        :param sql: SQL for querying data
        :param n: Number of data to query
        :param args: Parameters, can only be tuple or list
        :return: Return result set
        """
        self.cursor.execute(sql, args)
        result = self.cursor.fetchmany(n)
        return result

    def select_one(self, sql, args=None):
        """
        Query first data that meet the conditions
        :param sql: SQL for querying data
        :param args: Parameters, can only be tuple or list
        :return: Return result set
        """
        self.cursor.execute(sql, args)
        result = self.cursor.fetchone()
        return result

    def insert_data(self, sql, args=None):
        """
        Insert data
        :param sql: SQL for inserting data
        :param args: Parameters, can only be tuple or list
        :return: Return number of affected rows
        """
        self.cursor.execute(sql, args)
        self.conn.commit()
        return self.cursor.rowcount

    def update_data(self, sql, args=None):
        """
        Update data
        :param sql: SQL for updating data
        :param args: Parameters, can only be tuple or list
        :return: Return number of affected rows
        """
        self.cursor.execute(sql, args)
        self.conn.commit()
        return self.cursor.rowcount

    def delete_data(self, sql, args=None):
        """
        Delete data
        :param sql: SQL for deleting data
        :param args: Parameters, can only be tuple or list
        :return: Return number of affected rows
        """
        self.cursor.execute(sql, args)
        self.conn.commit()
        return self.cursor.rowcount

    def create_database_and_table(self):
        """
        Create database and table
        """
        # Create database
        self.cursor.execute("drop database if exists spider_db")
        self.cursor.execute("create database if not exists spider_db")
        self.cursor.execute("use spider_db")
        
        # Create table
        create_table_sql = """
        create table if not exists spider_db.job_info
        (
            category         varchar(255) null comment 'Primary category',
            sub_category     varchar(255) null comment 'Secondary category',
            job_title        varchar(255) null comment 'Job title',
            province         varchar(100) null comment 'Province',
            job_location     varchar(255) null comment 'Job location',
            job_company      varchar(255) null comment 'Company name',
            job_industry     varchar(255) null comment 'Industry type',
            job_finance      varchar(255) null comment 'Financing status',
            job_scale        varchar(255) null comment 'Company size',
            job_welfare      varchar(255) null comment 'Company benefits',
            job_salary_range varchar(255) null comment 'Salary range',
            job_experience   varchar(255) null comment 'Work experience',
            job_education    varchar(255) null comment 'Education requirement',
            job_skills       varchar(255) null comment 'Skill requirements',
            create_time      varchar(50)  null comment 'Crawl time'
        )
        """
        self.cursor.execute(create_table_sql)
        self.conn.commit()
        print("Database and table created successfully!")

    def close(self):
        """
        Close database connection
        """
        self.cursor.close()
        self.conn.close()




# Define main function
if __name__ == '__main__':
    # Instantiate DBUtils
    db = DBUtils('localhost', 'root', '123456', 'mysql')  # First connect to mysql database
    # Create database and table
    db.create_database_and_table()
    # Close database connection
    db.close()