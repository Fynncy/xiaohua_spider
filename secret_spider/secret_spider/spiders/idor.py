# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.response import Response
from ..items import SecretSpiderItem
from ..settings import SITE_BASE_URL
from scrapy.http.request import Request


class IdorSpider(scrapy.Spider):
    name = 'idor'
    allowed_domains = ['xiaohuar.com']
    start_urls = ['http://www.xiaohuar.com/list-1-0.html']

    def parse(self, response: Response):
        '''
        对获得到的结果进行转换
        :param response: 获得到的url
        :return: 直接返回item
        '''
        # 首先提取出所有的图片
        image_lists = response.xpath('.//div[@id = "list_img"]//img')
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        for image in image_lists:
            description = image.xpath('.//@alt').extract()[0]
            src = image.xpath('.//@src').extract_first()
            item = SecretSpiderItem(image_description=description)
            if src.startswith('http') or src.startswith('https'):
                item['image_urls'] = [src]
            else:
                full_url = SITE_BASE_URL + src
                item['image_urls'] = [full_url]
            yield item

        # 下面这一段代码 我们来判断是否有下一页来决定是否来构造对应得url(无法通过有效的响应得出来是否存在下一页)
        pages = response.xpath('//div[@class="page_num"]//a')
        next_page_url = ''
        for page in pages:
            page_text = page.xpath('./text()').extract_first()
            page_url = page.xpath('./@href').extract_first()
            if page_text == '下一页':
                next_page_url = page_url
        if next_page_url is not '':
            yield Request(url=next_page_url, callback=self.parse)
