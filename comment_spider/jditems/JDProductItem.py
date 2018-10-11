# -*- coding: utf-8 -*-

import scrapy

class JDProductItem(scrapy.Item):
    productID = scrapy.Field()
    skuID = scrapy.Field()
    skuIDs = scrapy.Field()