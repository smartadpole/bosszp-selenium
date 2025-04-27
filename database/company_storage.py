#!/usr/bin/python3
# encoding: utf-8
# @author: sunhao
# @contact: smartadpole@163.com
# @file: company_storage.py
# @time: 2025/4/27 10:30
# @function: Company information storage module.

import os
from datetime import datetime
import loger

class CompanyStorage:
    def __init__(self, output_dir):
        """
        Initialize company storage
        
        Args:
            output_dir (str): Output directory for markdown files
        """
        self.output_dir = os.path.join(output_dir, 'companies')
        os.makedirs(self.output_dir, exist_ok=True)

    def save_company_info(self, company_info):
        """
        Save company information to markdown file
        
        Args:
            company_info (dict): Company information
            
        Returns:
            str: Path to saved markdown file
        """
        try:
            # Create company directory
            company_dir = os.path.join(self.output_dir, company_info['name'])
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

    def save_job_listings(self, job_listings, company_name):
        """
        Save job listings to markdown file
        
        Args:
            job_listings (list): List of job listings
            company_name (str): Company name
            
        Returns:
            str: Path to saved markdown file
        """
        try:
            # Create company directory
            company_dir = os.path.join(self.output_dir, company_name)
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

def init_company_storage(output_dir):
    """
    Initialize company storage

    Args:
        output_dir (str): Directory for output files

    Returns:
        CompanyStorage: Initialized company storage instance
    """
    return CompanyStorage(output_dir) 