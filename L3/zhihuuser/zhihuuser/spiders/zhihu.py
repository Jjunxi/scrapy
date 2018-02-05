# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from zhihuuser.items import UserItem
import json


class ZhihuSpider(Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    start_user = 'excited-vczh'
    
    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    user_query = 'allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics'
    follower_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset={offset}&limit={limit}'
    follwer_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    follower_count = 0

    def start_requests(self):
        user_url = self.user_url.format(user=self.start_user, 
                                        include=self.user_query)
        yield Request(user_url, callback=self.parse_user)

        follower_url = self.follower_url.format(user=self.start_user, 
                                                include=self.follwer_query,
                                                offset=0,
                                                limit=20)
        yield Request(follower_url, callback=self.parse_follower)


    def parse_user(self, response):
        # print(response.text)
        result = json.loads(response.text)
        item = UserItem()
        for field in item.fields:
            if field in result.keys():
                item[field] = result.get(field)
        yield item

        yield Request(self.follower_url.format(user=result.get('url_token'),
                                               include=self.follwer_query,
                                               limit=20,
                                               offset=0),
                      callback=self.parse_follower)
            

    def parse_follower(self, response):
        results = json.loads(response.text)
        if 'data' in results.keys():
            for result in results.get('data'):
                user_url = self.user_url.format(user=result.get('url_token'), 
                                        include=self.user_query)
                yield Request(user_url, callback=self.parse_user)
        
        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            next_page = results.get('paging').get('next')
            yield Request(next_page, self.parse_follower)
            
            
