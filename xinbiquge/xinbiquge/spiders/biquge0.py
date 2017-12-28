# -*- coding: utf-8 -*-
import re
import scrapy

from xinbiquge.xinbiquge.items import XinbiqugeItem


class Biquge0Spider(scrapy.Spider):
    name = 'biquge0'
    allowed_domains = ['biquge0.com']
    start_urls = ['http://www.biquge0.com/modules/article/index.php?fullflag=1&page=1']

    def parse(self, response):
        page_total = re.compile('class="last">(\d+)</a>').findall(response.text)[0]
        for page in range(1, int(page_total)):
            yield scrapy.Request('http://www.biquge0.com/modules/article/index.php?fullflag=1&page=' + str(page),
                                 callback=self.parse_page)

    def parse_page(self, response):
        book_list = re.compile(
            '<span class="s2"><a href="(.*?)">.*?</a>.*?<span class="s4">.*?</li>').findall(response.text)
        for book in book_list:
            yield scrapy.Request('http://www.biquge0.com/' + book, callback=self.parse_book)

    def parse_book(self, response):
        # print(response.text)
        title = response.xpath('//div[@id="info"]/h1/text()').extract_first()[:-3]
        author = response.xpath('//div[@id="info"]/p[1]/text()').extract_first().split('：')[1]
        category = response.xpath('//div[@id="info"]/p[2]/text()').extract_first().split('：')[1]

        # print(title, author, category)
        book_content = re.compile('<dd><a href="(.*?)" title=".*?</a></dd>').findall(response.text)
        item = XinbiqugeItem()
        item['title'] = title
        item['author'] = author
        item['category'] = category
        item['links'] = [response.url[:-10] + content for content in book_content]
        yield item
