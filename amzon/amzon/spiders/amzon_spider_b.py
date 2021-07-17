import scrapy
from amzon.items import AmzonItem
from datetime import datetime
from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector
from selenium.webdriver.common.by import By
from selenium.webdriver import PhantomJS
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pymongo
from scrapy.utils.project import get_project_settings
from datetime import datetime,timedelta
from scrapy_redis.spiders import  RedisSpider


class AmzonTelsaRedisSpider(RedisSpider):
    name = 'tesla_amazon_redis'
    # allowed_domains = ['amazon.com']
    redis_key = "tesla:start_urls"
    # start_urls = ['https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_0_amazon-devices_1']
    # start_urls = [
    #     'https://www.amazon.com/s?k=tesla+accessories&crid=90RZC7XATMXS&sprefix=tesla+accessories%2Caps%2C438&ref=nb_sb_ss_ts-doa-p_1_17']
    # collection_name = 'amzon_popular'
    custom_settings = {
        'ITEM_PIPELINES': {'amzon.pipelines.AmazonTelsaPipeline': 301}
    }

    def __init__(self):
        self.mongo_uri = get_project_settings().get('MONGO_URI')
        self.mongo_db = get_project_settings().get('MONGO_DATABASE')
        self.collection = 'telsa'
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def make_requests_from_url(self, url):
        return SeleniumRequest(url=url,
                              callback=self.parse_more,
                              wait_time=30,
                              wait_until=EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.a-pagination')),
                              cb_kwargs={'current_page':1}
                              )
    def parse_more(self, response,current_page):
        '''抓取商品链接及在本页能够获取的其他信息，并传递至下个函数内'''

        driver = response.request.meta.get('driver')
        items = response.css('div.a-section.a-spacing-medium')
        for item in items:
            preview_img_url = item.css('img.s-image').attrib.get('src')
            item_name = item.css('h2.a-size-mini span::text').get()
            item_url = item.css('h2.a-size-mini a').attrib.get('href')
            item_star = item.css('i.a-star-small-4-5 span::text').get()
            review_counts = item.css('span.a-size-base::text').get()
            review_url = item.css('a.a-link-normal').attrib.get('href')
            item_price = item.css('span.a-price-whole::text').get()
            # coll = self.db[self.collection]
            # docs = coll.find({'item_url':item_url}) if
            # if docs:
            #     close_time = [doc['crawl_time'] for doc in docs]
            #     timespan = max(close_time)-datetime.now()
            # print(more_button)
            # if (not coll.find_one({'item_url':item_url}))\
            #     or ( not coll.find_one({'item_name':item_name})) \
            #     or (coll.find_one({'item_url':item_url}) and\
            #         ((max([doc['crawl_time'] for doc in coll.find({'item_url':item_url})])-datetime.now()) or timespan.hour>8)):

            yield response.follow(url=item_url,
                                  callback=self.parse_item,
                                  cb_kwargs={'preview_img_url': preview_img_url,
                                             'item_name': item_name,
                                             'item_star': item_star,
                                             'review_counts': review_counts,
                                             'review_url': review_url,
                                             'item_price': item_price})

    def parse_item(self, response, item_star, preview_img_url, item_name, review_counts, item_price, review_url):
        '''抓取商品的详细信息'''
        item = AmzonItem()
        item['item_url'] = response.url
        item['item_name'] = item_name
        item['features'] = response.css('div#feature-bullets').css('li span::text').getall()
        item['item_star'] = item_star
        item['preview_img_link'] = preview_img_url
        # item['star'] = sta
        item['review_counts'] = review_counts
        item['item_price'] = item_price
        # item['category'] = category
        item['review_url'] = response.urljoin(review_url)
        item['crawl_time'] = datetime.now()

        yield item