# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re

import requests


class SaveContentToLocalPipeline(object):
    def process_item(self, item, spider):
        title = item['title']
        author = item['author']
        category = item['category']
        links = item['links']
        for link in links:
            response = requests.get(link)
            response.encoding = 'gbk'
            # print(response.text)
            content = re.compile('<!--go-->(.*?)<!--over-->', re.S).findall(response.text)[0].replace('&nbsp;',
                                                                                                      '').replace(
                '<br /', '')[:-183]
            chapter = re.compile('<h1>(.*?)</h1>').findall(response.text)[0]
            with open('xiaoshuo/' + '[' + category + ']' + title + '(' + author + ')' + '-' + chapter + '.txt',
                      'w') as f:
                f.write(content)
                f.close()
