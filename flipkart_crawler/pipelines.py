# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
import scrapy


class MyImagesPipeline(ImagesPipeline):
    #Name download filename
    def file_path(self, request, response=None, info=None):
        return request.meta.get('filename', '')

    #Name thumbnail version
    def thumb_path(self, request, thumb_id, response=None, info=None):
        image_guid = thumb_id + response.url.split('/')[-1]
        return 'thumbs/%s/%s.jpg' % (thumb_id, image_guid)

    def get_media_requests(self, item, info):
        meta = {'filename': item['file_name']}
        return (scrapy.Request(url=image, meta=meta) for image in item['image_urls'])