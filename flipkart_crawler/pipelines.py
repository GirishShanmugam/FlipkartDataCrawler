# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import hashlib

from scrapy.pipelines.images import ImagesPipeline
import scrapy
from scrapy.exceptions import DropItem


class MyImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        image_path = request.meta['page_url'][:request.meta['page_url'].rfind('/')]
        image_path = image_path[image_path.rfind('/') + len('/'):]
        image_guid = '/flipkart/'+ image_path + '/' + hashlib.sha1(request.url).hexdigest() +'.jpg'
        return image_guid

    def get_media_requests(self, item, info):
        yield scrapy.Request(item['image_urls'][0], meta=item)
