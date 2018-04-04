# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FlipkartTshirtsMenItem(scrapy.Item):
    # define the fields for your item here like:
    file_name = scrapy.Field()
    image_urls = scrapy.Field()
    id = scrapy.Field()
    flipkart_product_id = scrapy.Field()
    title = scrapy.Field()
    key_specs = scrapy.Field()
    analytics_data = scrapy.Field()
    rating = scrapy.Field()