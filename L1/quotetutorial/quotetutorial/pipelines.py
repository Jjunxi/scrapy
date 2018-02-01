# -*- coding: utf-8 -*-

import pymongo
from scrapy.exceptions import DropItem

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class TextPipeline(object):
    
    def __init__(self):
        self.limit = 50

    def process_item(self, item, spider):
        if item['text']:
            if len(item['text']) > self.limit:
                item['text'] =  item['text'][0:self.limit].rstrip() + '...'
                return item
        else:
            return DropItem('Text Error %s' % item)


class MongoPipeline(object):
    
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
    
    # get settings from settings.py
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri = crawler.settings.get('MONGO_URI'),
            mongo_db = crawler.settings.get('MONGO_DB')
        )

    # just start spider
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        if item:
            name = item.__class__.__name__
            self.db[name].insert(dict(item))
            return item
        else:
            return DropItem('Mongo Error %s' % item)

    def close_spider(self, spider):
        self.client.close()