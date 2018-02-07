# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
import requests

class ZhihuuserSpiderMiddleware(object):
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


class RandomUserAgentMiddleware(UserAgentMiddleware):
    
    def __init__(self, user_agent):
        self.user_agent = user_agent

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            user_agent=crawler.settings.get('USER_AGENTS')
        )

    def process_request(self, request, spider):
        agent = random.choice(self.user_agent)
        request.headers['User-Agent'] = agent
        print(agent)
        # return None 


class ProxyMiddleware(object):
    
    def __init__(self):
        self.proxy_url = 'http://localhost:5000/random'
        self.proxy_in_use = False
        self.change_proxy = False
        self.proxy = self.get_proxy()
        self.count = 0

    def get_proxy(self):
        try:
            response = requests.get(self.proxy_url)
            if response.status_code == 200:
                # print(response.text)
                return response.text
            return None
        except expression as identifier:
            return None

    def process_request(self, request, spider):
        if not self.proxy_in_use:
            return None

        if not self.change_proxy:
            request.meta['proxy'] = self.proxy
            print(self.proxy)
            return None
        else:
            self.proxy = self.get_proxy()
            self.change_proxy = False
            return request


    def process_response(self, request, response, spider):
        if response.status == 200:
            return response
        else: #302, 403, 301
            if self.count < 3:
                self.count += 1
            else:
                self.count = 0
                if not self.proxy_in_use:
                    self.proxy_in_use = True
                else:
                    self.change_proxy = True
            return request

    def process_spider_exception(self, request, exception, spider):
        return request


