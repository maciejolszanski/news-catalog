"""
This file contains logic of application
"""


import subprocess
import os


if __name__ == "__main__":

    spider_name = "wp_spider"
    parent_dir = os.getcwd()
    scrapy_path = os.path.join(parent_dir, "scrapy_project")
    scrapy_comamnnd = ["scrapy", "crawl", spider_name, "-O",
                       "test.jsonl", "-a", "prefix=j"]
    subprocess.run(scrapy_comamnnd, cwd=scrapy_path)
