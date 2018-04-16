# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random
import requests
import json
import time
import logging

from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy import signals
from scrapy.utils.response import response_status_message

from .settings import USER_AGENTS
from .get_ipport import get_proxy, get_ip_port_queue

# 全局的ip代理队列, 全局变量
IP_PORT_QUEUE = get_ip_port_queue()
IP_PORT = IP_PORT_QUEUE.get()

# shi xiao ip_port lie biao




class RandomUserAgent(object):
    def process_request(self, request, spider):
        user_agent = random.choice(USER_AGENTS)
        request.headers.setdefault('User-Agent', user_agent)


class RandomProxy(object):

    def process_request(self, request, spider):
        # 判断队列是否为空,若为空,则重新填充队列
        # 声明全局变量
        global IP_PORT_QUEUE
        global IP_PORT

        if IP_PORT_QUEUE.empty():
            IP_PORT_QUEUE = get_ip_port_queue()
        # 获取ip代理
        if request.meta.get('proxy', False):
            print('重试ip代理是%s' % request.meta.get('proxy'))
        ip_port = IP_PORT
        print('当前代理是%s' % ip_port)

        request.meta['proxy'] = 'http://' + ip_port

    def process_response(self, request, response, spider):
        if response.status != 200:
            # 如果返回状态码不是200, 则删除ip,并重新向队列中添加一个新的ip
            proxy = request.meta.get('proxy')
            ip_port = proxy.split(':')[1][2:]
            print('%s代理请求异常了!!!!' % ip_port)
            # delete ip
            requests.get('http://127.0.0.1:8000/delete?ip=%s' % ip_port)
            global IP_PORT
            global IP_PORT_QUEUE
            if IP_PORT_QUEUE.empty():
                IP_PORT_QUEUE = get_ip_port_queue()
            IP_PORT = IP_PORT_QUEUE.get()
            request.meta['proxy'] = 'http://' + IP_PORT
            return request
        return response


class MyRetryMiddleware(RetryMiddleware):
    logger = logging.getLogger(__name__)

    def delete_proxy(self, proxy):
        if proxy:
            ip_port = proxy.split(':')[1][2:]
            # delete proxy from proxies pool
            requests.get('http://127.0.0.1:8000/delete?ip=%s' % ip_port)

    def process_response(self, request, response, spider):
        if request.meta.get('dont_retry', False):
            return response
        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            # 删除该代理
            self.delete_proxy(request.meta.get('proxy', False))
            # 设置新的ip代理
            global IP_PORT_QUEUE
            global IP_PORT
            if IP_PORT_QUEUE.empty():
                IP_PORT_QUEUE = get_ip_port_queue()
            IP_PORT = IP_PORT_QUEUE.get()
            # request.meta['proxy'] = IP_PORT
            # 删除当前代理
            request.meta.pop('proxy')
            request.meta['proxy'] = 'http://' + IP_PORT
            print('retry代理%s' % request.meta.get('proxy', '无'))
            # time.sleep(random.randint(3, 5))
            self.logger.warning('返回值异常, 进行重试...')
            # return self._retry(request, reason, spider) or response
            return request
        return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY) \
                and not request.meta.get('dont_retry', False):
            # 删除该代理
            self.delete_proxy(request.meta.get('proxy', False))
            request.meta.pop('proxy')
            #  设置新的ip代理
            global IP_PORT_QUEUE
            global IP_PORT
            if IP_PORT_QUEUE.empty():
                IP_PORT_QUEUE = get_ip_port_queue()
            IP_PORT = IP_PORT_QUEUE.get()
            request.meta['proxy'] = 'http://' + IP_PORT
            print('retry代理%s' % request.meta.get('proxy', '无'))
            self.logger.warning('连接异常, 进行重试...')
            # return self._retry(request, exception, spider)
            return request


class ZhihuSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
