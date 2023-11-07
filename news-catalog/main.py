"""
This file contains logic of application
"""


import subprocess
import os


if __name__ == "__main__":

    spiders_to_run = ["wp_spider"]
    parent_dir = os.getcwd()
    scrapy_path = os.path.join(parent_dir, "scrapy_project")
    css_prefix = 'j'

    for spider in spiders_to_run:
        scrapy_comamnnd = ["scrapy", "crawl", spider, "-O",
                           "test.jsonl", "-a", f"prefix={css_prefix}"]
        subprocess.run(scrapy_comamnnd, cwd=scrapy_path)
