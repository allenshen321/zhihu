# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from zhihu.settings import MONGODB_COLLECTION, MONGODB_DB, MONGODB_PORT, MONGODB_SERVER


class ZhihuPipeline(object):
    def __init__(self):
        self.connection = pymongo.MongoClient(MONGODB_SERVER, MONGODB_PORT)
        self.db = self.connection[MONGODB_DB]
        self.collection = self.db[MONGODB_COLLECTION]

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item
