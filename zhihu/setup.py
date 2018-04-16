# coding=utf-8

from scrapy import cmdline

# 启动知乎爬虫
cmdline.execute('scapy crawl zhihucom'.split())

# 启动测试proxy
#cmdline.execute('scrapy crawl zhihuspider'.split())
