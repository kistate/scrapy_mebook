# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MebbokItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    cover = scrapy.Field()
    intro = scrapy.Field()
    down_url = scrapy.Field()
    category = scrapy.Field()
    target_urls = scrapy.Field()
    down_info = scrapy.Field()
