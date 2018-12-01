# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SecretSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    image_description = scrapy.Field()
    image_urls = scrapy.Field()  # 这里设置一下整个图片下载的整个url
    images = scrapy.Field()  # 设置一下整个的 images