# -*- coding: utf-8 -*-

import scrapy,json
from scrapy.spider import Rule

from scrapy.linkextractor import LinkExtractor
import pika
from comment_spider.settings import JD_CATEGORY_QUEUE_NAME
from comment_spider.spiders.mq_crawl_spider import MQCrawlSpider


class JDCategorySpider(MQCrawlSpider):

    name = "jd_category_spider"
    start_urls = ['https://www.jd.com/allSort.aspx']
    links = LinkExtractor(allow="cat=", deny="error\.aspx")
    rules = [Rule(links, callback='parseContent')]

    allowed_domains = ['jd.com']

    def start_requests(self):

        # setup the pika connection
        self.fetchCrawlUrls()
        # setup jd category queue
        self.channel.queue_declare(queue=JD_CATEGORY_QUEUE_NAME)

        # starting request
        url = self.start_urls[0]
        header = {}
        yield scrapy.Request(url=url, callback=self.parse, method="GET", headers=header)

    def parseContent(self, response):

        # url split
        request_url = response.url
        category_code_str = request_url.split("cat=")[1]
        category_code_list = category_code_str.split(",")
        category_code_list_len = len(category_code_list)

        # 1st category name
        first_category_name = response.xpath("//div[@id='J_crumbsBar']//div[@class='crumbs-nav-item one-level']/a/text()").extract_first()
        # 1st category code
        first_category_code = category_code_list[0]

        # check if 1st category is valid
        if None not in (first_category_code, first_category_name):

            # prepare the message payload dict
            payload_dict = {"category_code": first_category_code, "category_name": first_category_name, "category_level": "1", "parent_id": "0"}
            # format into json
            payload_json = json.dumps(payload_dict, ensure_ascii=False)

            # insert 1st category queue into the category queue in mq
            self.channel.basic_publish(exchange='', routing_key=JD_CATEGORY_QUEUE_NAME, body=payload_json)

        # 2nd category_code
        if category_code_list_len == 2:

            # 2nd category_code
            second_category_code = category_code_list[1].split("&")[0]
            second_category_name = response.xpath(
                "//div[@id='J_crumbsBar']//span[@class='curr']/text()").extract_first()
            # prepare the message payload dict
            payload_dict_second = {"category_code": second_category_code,
                            "category_name": second_category_name,
                            "category_level": "2",
                            "parent_id": first_category_code}
            # format into json
            payload_json_second = json.dumps(payload_dict_second, ensure_ascii=False)
            # insert 1st category queue into the category queue in mq
            self.channel.basic_publish(exchange='', routing_key=JD_CATEGORY_QUEUE_NAME, body=payload_json_second)
            print(payload_dict_second)

        elif category_code_list_len == 3:
            second_category_code = category_code_list[1]
            second_category_name = response.xpath("//div[@id='J_crumbsBar']//span[@class='curr']/text()").extract_first()

            # prepare the message payload dict
            payload_dict_second = {"category_code": second_category_code,
                            "category_name": second_category_name,
                            "category_level": "2",
                            "parent_id": first_category_code}

            # format into json
            payload_json_second = json.dumps(payload_dict_second, ensure_ascii=False)



            third_category_code = category_code_list[2]
            third_category_name = response.xpath("//div[@id='J_crumbsBar']//span[@class='curr']/text()").extract()[1]

            # prepare the message payload dict
            payload_dict_third = {"category_code": third_category_code,
                            "category_name": third_category_name,
                            "category_level": "3",
                            "parent_id": second_category_code}

            # format into json
            payload_json_third = json.dumps(payload_dict_third, ensure_ascii=False)

            # insert 1st category queue into the category queue in mq
            self.channel.basic_publish(exchange='', routing_key=JD_CATEGORY_QUEUE_NAME, body=payload_json_second)

            # insert 1st category queue into the category queue in mq
            self.channel.basic_publish(exchange='', routing_key=JD_CATEGORY_QUEUE_NAME, body=payload_json_third)


