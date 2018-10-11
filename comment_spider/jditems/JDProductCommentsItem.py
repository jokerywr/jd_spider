# -*- coding: utf-8 -*-

import scrapy

class JDProductCommentsItem(scrapy.Item):

    # SKU info
    skuID = scrapy.Field()
    skuName = scrapy.Field()
    skuFirstCategoryID = scrapy.Field()
    skuSecondCategoryID = scrapy.Field()
    skuThirdCategoryID = scrapy.Field()
    skuColor = scrapy.Field()
    skuSize = scrapy.Field()

    # order info
    orderCreationTime = scrapy.Field()

    # comment info
    commentGUID = scrapy.Field()
    commentContent = scrapy.Field()
    commentCreationTime = scrapy.Field()
    commentScore = scrapy.Field()

    # user info
    userLevelName = scrapy.Field()
    userIsMobile = scrapy.Field()
    userClient = scrapy.Field()
    userNickName = scrapy.Field()