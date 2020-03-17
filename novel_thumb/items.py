# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NovelThumbItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    category_id = scrapy.Field() 
    article_url_base = scrapy.Field()
    thumb = scrapy.Field()
    allowed_domain = scrapy.Field()


