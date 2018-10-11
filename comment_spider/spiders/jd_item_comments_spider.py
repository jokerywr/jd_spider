# -*- coding: utf-8 -*-

import scrapy, json
from comment_spider.jditems.JDProductCommentsItem import JDProductCommentsItem
import pika
from comment_spider.spiders.easy_spider import EasySpider


class JDItemCommentsSpider(EasySpider):
    name = "jd_item_comments"

    def start_requests(self):
        url = 'http://sclub.jd.com/comment/productPageComments.action?callback=&productId=6430157&score=0&sortType=1' \
              '&page=0&pageSize=10&isShadowSku=0&fold=1 '
        # url = 'http://item.jd.com/6308468.html'

        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'host': 'sclub.jd.com',
            'Referer': 'http://item.jd.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }

        yield scrapy.Request(url=url, callback=self.parse, method="GET", headers=header)

    def parse(self, response):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='47.105.97.114', virtual_host="/product_messages",
                                      credentials=pika.PlainCredentials("admin", "Abcd1234")))
        channel = connection.channel()
        channel.queue_declare(queue="prod_msg")

        commentsResult = json.loads(response.text)
        for comment in commentsResult["comments"]:
            jdProductCommentsItem = JDProductCommentsItem()
            jdProductCommentsItem["commentGUID"] = comment['guid']
            jdProductCommentsItem["commentContent"] = comment['content']
            jdProductCommentsItem['commentCreationTime'] = comment['creationTime']
            jdProductCommentsItem['commentScore'] = comment['score']

            self.save(jdProductCommentsItem)
            channel.basic_publish(exchange='', routing_key='prod_msg', body=comment['content'])
        connection.close()

    def save(self, jdProductCommentsItem):
        print(jdProductCommentsItem)
