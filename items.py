# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    crawl_time = scrapy.Field()
    spider_name = scrapy.Field()
    big_name = scrapy.Field()
    small_name = scrapy.Field()
    book_name = scrapy.Field()
    # 图书图片：
    book_img =scrapy.Field()
    # 图书作者:book_author =
    book_author = scrapy.Field()
    # 出版社：book_story =
    book_story =scrapy.Field()
    # 出版时间：book_time =
    book_time = scrapy.Field()
    # 价格：book_price =
    book_price = scrapy.Field()
