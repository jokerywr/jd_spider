#coding=utf8

import scrapy,pika
from scrapy.spider import CrawlSpider
from comment_spider.settings import PIKA_SERVER,PIKA_VHOST,PIKA_USER,PIKA_PASS,JD_CATEGORY_QUEUE_NAME

class MQCrawlSpider(CrawlSpider):

    name = 'easyspider'

    def fetchCrawlUrls(self):

        try:

            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=PIKA_SERVER, virtual_host=PIKA_VHOST,credentials=pika.PlainCredentials(PIKA_USER,PIKA_PASS)))
            self.channel = self.connection.channel()


        except:
            pass

if __name__ == "__main__":

    es = MQCrawlSpider()

    es.fetchCrawlUrls()