# -*- coding: utf-8 -*-
import scrapy


class ZhihucomSpider(scrapy.Spider):
    name = 'zhihuspider'
    start_urls = ['http://ip.chinaz.com/getip.aspx']

    def parse(self, response):
        print(response.text)
