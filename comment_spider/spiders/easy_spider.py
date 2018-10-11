# -*- coding: utf-8 -*-

import scrapy,json
import pika
from comment_spider.settings import PIKA_SERVER,PIKA_VHOST,PIKA_USER,PIKA_PASS

class EasySpider(scrapy.Spider):

    name = 'easyspider'

    def fetchCrawlUrls(self):

        try:

            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=PIKA_SERVER, virtual_host=PIKA_VHOST,credentials=pika.PlainCredentials(PIKA_USER,PIKA_PASS)))
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue="jd_product_comments_queue")

        except:
            pass

if __name__ == "__main__":

    es = EasySpider()

    es.fetchCrawlUrls()