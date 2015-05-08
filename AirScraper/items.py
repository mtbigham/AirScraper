# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AirscraperItem(scrapy.Item):
    depart = scrapy.Field()
    dest = scrapy.Field()
    departDate = scrapy.Field()
    arriveDate = scrapy.Field()
    flightNum = scrapy.Field()
    departTime = scrapy.Field()
    arriveTime = scrapy.Field()
    price = scrapy.Field()
    points = scrapy.Field()