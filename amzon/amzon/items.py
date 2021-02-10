# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmzonItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    star= scrapy.Field()
    rank = scrapy.Field()
    preview_img_link = scrapy.Field()
    view_times= scrapy.Field()
    price = scrapy.Field()
    category = scrapy.Field()
    features = scrapy.Field()
    crawl_time = scrapy.Field()


    # reviews = scrapy.Field()


