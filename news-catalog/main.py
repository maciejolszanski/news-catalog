"""
This file contains logic of application
"""

import subprocess
import os

if __name__ == "__main__":
    
    spider_name = "wp_spider"
    parent_dir = os.getcwd()
    scrapy_path = os.path.join(parent_dir, "scrapy_data")
    subprocess.run(["scrapy", "crawl", spider_name], cwd=scrapy_path)