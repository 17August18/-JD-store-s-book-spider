# -*- coding: utf-8 -*-
from datetime import datetime
from scrapy.exporters import JsonItemExporter
import pymongo
import redis
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class JdPipeline(object):
    def process_item(self, item, spider):

        # utcnow 为0时区  改为now
        item["crawl_time"] = datetime.now()
        item["spider_name"] = spider.name
        return item

class bookdatajsonPipeline(object):
    # def open_spider(self,spider):
    #     self.file = open("aqi.json","wb")
    #     self.writer = JsonItemExporter(self.file)
    #     self.writer.start_exporting()
    # def process_item(self,item,spider):
    #     self.writer.export_item(item)
    #     return item
    # def close_spider(self,spider):
    #     self.writer.finish_exporting()
    #     self.file.close()
    def open_spider(self, spider):
        self.file = open('jdbook.json', 'wb')
        self.writer = JsonItemExporter(self.file)
        self.writer.start_exporting()

    def process_item(self, item, spider):
        self.writer.export_item(item)
        return item

    def close_spider(self, spider):
        self.writer.finish_exporting()
        self.file.close()

class bookdatamgdbPipeline(object):
    def open_spider(self,spider):
        self.client = pymongo.MongoClient(host = "127.0.0.1",port = 27017)
        self.collection = self.client.JD.book
    def process_item(self,item,spider):
        self.collection.insert(dict(item))
        return item
    def close_spider(self,spider):
        self.client.close()
class bookdataredisPipeline(object):
    # def open_spider(self,spider):
    #     self.client = redis.StrictRedis(host = "127.0.0.1",port = 6379)
    #     self.sava_key = "aqi_redis"
    # def process_item(self,item,spider):
    #     self.client.lpush(self.sava_key,dict(item))
    #     return item
    def open_spider(self, spider):
        # 链接数据库
        self.client = redis.StrictRedis(host="127.0.0.1", port=6379)
        # 存储的key
        self.save_key = 'aqi_redis'

    def process_item(self, item, spider):
        self.client.lpush(self.save_key, dict(item))
        return item
