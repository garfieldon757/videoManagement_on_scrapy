# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class categoryItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()

class productItem(scrapy.Item):
    video_name = scrapy.Field()
    brand_name = scrapy.Field()
    language = scrapy.Field()
    contury_or_region = scrapy.Field()
    ad_year = scrapy.Field()
    ad_type = scrapy.Field()
    ad_video_coverLink = scrapy.Field()
    ad_video_sourceLink = scrapy.Field()
