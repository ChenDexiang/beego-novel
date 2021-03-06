# -*- coding: utf-8 -*-
import scrapy
import redis

class NovelIdsSpider(scrapy.Spider):
    name = 'novel_ids'
    allowed_domains = ['www.23us.so']
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'}

    def start_requests(self):
        url = 'http://www.23us.so/'
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        rds = redis.Redis(host='127.0.0.1', port=6379, password='123456', db=1)
        ids = []
        for id in rds.lrange("novel_id_insert", 0, -1):
            ids.append(int(id))
        urls = response.css('ul.update li .poptext::attr(href)').extract()
        for url in urls:
            id = url.split('/')[-1].replace('.html', '')
            if int(id) not in ids:
                rds.rpush("novel_id_insert", id)

