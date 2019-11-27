# -*- coding: utf-8 -*-
import scrapy
from JD.items import JdItem
import json
from copy import deepcopy

class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['jd.com','p.3.cn']
    start_urls = ['https://book.jd.com/booksort.html']
    page = 0

    def parse(self, response):
        # 图书大分类：
        dt_list = response.xpath('//*[@id="booksort"]/div[2]/dl/dt')
        # 遍历dt得到dd
        # following—sibling::*[1]
        for dt in dt_list:
            item = JdItem()
            item['big_name'] = dt.xpath('./a/text()').extract_first()
            # 小分类：
            em_list = dt.xpath('./following-sibling::*[1]/em')
            for em in em_list:
                item['small_name'] = em.xpath('a/text()').extract_first()
                small_link = 'http:' + em.xpath('a/@href').extract_first()
                #开启第二层
                yield scrapy.Request(small_link,callback=self.parse_book,meta = {"book":deepcopy(item)})
    def parse_book(self,response):
        item = response.meta["book"]
        # 数据列表所有的书：
        book_list = response.xpath('//div[@id="plist"]/ul/li')
        for book in book_list:
            # 图书名字：
            item['book_name'] = book.xpath('.//div[@class="p-name"]/a/em/text()').extract_first().strip()
            # 图书图片：
            item['book_img'] = "https:" + book.xpath('.//div[@class="p-img"]/a/img/@src').extract_first()
            # 图书作者:book_author =
            item['book_author'] = book.xpath('.//span[@class="author_type_1"]/a/text()').extract_first()
            # 出版社：book_story =
            item['book_story']= book.xpath('.//span[@class="p-bi-store"]/a/text()').extract_first()
            # 出版['时间：book_time =
            item['book_time'] = book.xpath('.//span[@class="p-bi-date"]/text()').extract_first().strip()
            # 价格：book_price =
            # item['book_price'] = book.xpath('.//div[@class="p-price"]/strong/i/text()').extract_first()
            # 价格网址
            """
            https://p.3.cn/prices/mgets?skuIds=J_
            
            """
            book_id = book.xpath('./div/@data-sku').extract_first()
            price_url = "https://p.3.cn/prices/mgets?skuIds=J_{}".format(book_id)
            yield scrapy.Request(price_url,callback=self.parse_price,meta={"book":deepcopy(item)})
            # yield item
            self.page += 1
            if price_url is None:
                return
            # 列表翻页
            # 取出下一页的url
            next_url = response.xpath('//a[@class="pn-next"]/@href').extract_first()
            # 发送请求
            yield response.follow(
                next_url,
                callback = self.parse_book,
                meta = {"book":item}
            )
    def parse_price(self,response):
        item = response.meta['book']
        # print(response.body)
        # with open("abc.txt","w",encoding='utf-8') as f:
        #     f.write(response.text)
        # print(response.hearder)
        item['book_price'] = json.loads(response.body.decode())[0]['p']
        yield item

