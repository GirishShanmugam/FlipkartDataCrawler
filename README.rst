=========================
 Flipkart Data Crawler
=========================

Data Crawler for Flipkart using Scrapy in Python

Instructions
------------

#. To install Scrapy using ``conda``, run:

        conda install -c conda-forge scrapy

   Alternatively, if you’re already familiar with installation of Python packages, you can install Scrapy and its dependencies from ``PyPI`` with:

        pip install Scrapy

#. Enter the URL's to crawl from in ``start_urls`` list in ``/flipkart_crawler/spiders/flipkart_spider.py``:

        start_urls = ['https://www.flipkart.com/mens-clothing/tshirts/pr?sid=2oq,s9b,j9y&otracker=nmenu_sub_Men_0_T-Shirts']

#. Run this command to get the data:

        scrapy crawl product_category_list_crawler
