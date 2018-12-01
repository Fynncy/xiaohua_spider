# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .models import IdorImage
from scrapy.crawler import Crawler
import mongoengine
from .settings import IMAGES_STORE
import os


class SecretSpiderPipeline(object):
    def __init__(self, database, host, port, username, password):
        self.database = database
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def process_item(self, item, spider):
        '''
        这里对整个的图片进程进行转化
        :param item: 获取到的item
        :param spider:
        :return:
        '''
        idor = IdorImage(description=item['image_description'])
        for image in item['images']:
            full_path = os.path.join(IMAGES_STORE, image['path'])
            photo = open(full_path, 'rb')
            idor.image.put(photo, content_type='image/jpeg')
            idor.save()
        return item

    def open_spider(self, spider):
        mongoengine.connection.disconnect()
        mongoengine.connect(self.database, host=self.host, port=self.port, username=self.username,
                            password=self.password)

    def close_spider(self, spider):
        mongoengine.connection.disconnect()

    @classmethod
    def from_crawler(cls, crawler: Crawler):
        database = crawler.settings.get('MONGODB_DATABASE')
        host = crawler.settings.get('MONGODB_HOST')
        port = crawler.settings.get('MONGODB_PORT')
        username = crawler.settings.get('MONGODB_USERNAME')
        password = crawler.settings.get('MONGODB_PASSWORD')

        return cls(database=database, host=host, port=port, username=username, password=password)
