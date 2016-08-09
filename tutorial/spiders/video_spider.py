# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Spider
from tutorial.items import categoryItem,productItem
from scrapy.http import Request
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class VideoSpiderSpider(Spider):
    name = "video_spider"
    allowed_domains = ["cnad.com"]
    start_urls = [ "http://k.cnad.com" ]

    def start_requests(self):
        result_total = Request(self.start_urls[0], callback = self.parse_category)
        print result_total

    def parse_category(self,response):
        # 获取分类信息
        category_list_temp = response.selector.xpath(u'//div[@class="left180"]/div')
        category_list = category_list_temp[0].xpath(u'div/ul/li')
        category_item_dict = []

        for category_item in category_list:
            item = categoryItem()
            item['title'] = category_item.xpath(u'a/@title').extract()[0]
            item['link'] = category_item.xpath(u'a/@href').extract()[0]
            item['desc'] = ""
            category_item_dict.append(item.values())
            # tutirialItem类的对象不可以json序列化，需要其中的value属性（这是一个列表对象）进行序列化。

        production_box_item_list_total = []
        for category_item in category_item_dict:
            print "当前分类是：" + category_item[2] + ";"
            url = "http://k.cnad.com" + category_item[1]
            production_box_item_list_total = scrapy.Request( url = url ,
                                  callback = self.parse_video ,
                                  meta = {'production_box_item_list_total' : production_box_item_list_total}
                                )

        yield production_box_item_list_total


    def parse_video(self,response):

        page_box_list =  response.selector.xpath(u'//div[@class="page_box"]/div/a')
        page_count = page_box_list[-2].xpath(u'text()').extract()[0]
        print "当前分类视频资源页面数共计：" + page_count + "页"

        production_box_item_list = []
        production_box_item_list_total = response.meta["production_box_item_list_total"]
        base_url = response.url
        for page_index in range(int(page_count)):
            url = base_url + "&page=" + str(page_index + 1)
            production_box_item_list= scrapy.Request( url = url ,
                                  callback= self.parse_video_pagely ,
                                  meta = {'production_box_item_list' : production_box_item_list}
                                )
            production_box_item_list_total.append(production_box_item_list)

        yield production_box_item_list_total

    def parse_video_pagely(self , response):
        production_box_list = response.selector.xpath(u'//div[@class="main_box"]/div[@class="production_box"]')
        website_url = "http://k.cnad.com"
        for production_box in production_box_list:
            item = productItem()
            video_cover_image_link = urls_join(website_url ,  production_box.xpath(u'p[@class="pro_pic"]/a/img/@src').extract()[0])
            if video_cover_image_link[0:4] == "http":
                item["video_name"] = production_box.xpath(u'h3/a/text()').extract()[0].lstrip()
                item["brand_name"] = production_box.xpath(u'p/span')[0].xpath(u'text()').extract()[0]
                item["language"] = production_box.xpath(u'p/span')[1].xpath(u'text()').extract()[0]
                item["contury_or_region"] = production_box.xpath(u'p/span')[2].xpath(u'text()').extract()[0]
                item["ad_year"] = production_box.xpath(u'p/span')[3].xpath(u'text()').extract()[0]
                item["ad_type"] = production_box.xpath(u'p/span')[4].xpath(u'text()').extract()[0]
                item["ad_video_coverLink"] = video_cover_image_link,
                item["ad_video_sourceLink"] = urls_join(website_url , production_box.xpath(u'p[@class="pro_pic"]/a/@href').extract()[0])
            else:
                item["video_name"] = production_box.xpath(u'h3/a/text()').extract()[0].lstrip()
                item["brand_name"] = production_box.xpath(u'p/span')[0].xpath(u'text()').extract()[0]
                item["language"] = production_box.xpath(u'p/span')[1].xpath(u'text()').extract()[0]
                item["contury_or_region"] = production_box.xpath(u'p/span')[2].xpath(u'text()').extract()[0]
                item["ad_year"] = production_box.xpath(u'p/span')[3].xpath(u'text()').extract()[0]
                item["ad_type"] = production_box.xpath(u'p/span')[4].xpath(u'text()').extract()[0]
                item["ad_video_coverLink"] = urls_join(website_url , video_cover_image_link)
                item["ad_video_sourceLink"] = urls_join(website_url , production_box.xpath(u'p[@class="pro_pic"]/a/@href').extract()[0])

            production_box_item_list = response.meta["production_box_item_list"]
            production_box_item_list.append(item)

        yield production_box_item_list

def urls_join(*parts):
    return "".join(parts)