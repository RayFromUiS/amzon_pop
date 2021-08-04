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
import re
from scrapy.http import HtmlResponse
from scrapy_redis.spiders import  RedisSpider

# class AmzonPopularSpider(scrapy.Spider):
#     name = 'amzon_spider'
#     allowed_domains = ['amazon.com']
#     # start_urls = ['https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_0_amazon-devices_1']
#     start_urls = [
#         'https://www.amazon.com/s?k=tesla+accessories&crid=90RZC7XATMXS&sprefix=tesla+accessories%2Caps%2C438&ref=nb_sb_ss_ts-doa-p_1_17']
#     # collection_name = 'amzon_popular'
#     custom_settings = {
#         'ITEM_PIPELINES': {'amzon.pipelines.AmzonPipeline': 300}
#     }
#
#     # def __init__(self,mongo_uri,mongo_db):
#     # #     uri = 'mongodb://localhost:27017'
#     # #     conn = pymongo.MongoClient(uri)
#     # #     self.db = conn["amzon"]
#     # #     self.collection = self.db["amzonPopularItem"]
#     #     self.client = pymongo.MongoClient(mongo_uri)
#     #     self.db = self.client[mongo_db]
#     #     self.collection = self.db[self.collection_name]
#     #
#     # @classmethod
#     # def from_crawler(cls, crawler):
#     #     return cls(
#     #         mongo_uri=crawler.settings.get('MONGO_URI'),
#     #         mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
#     #     )
#
#     def start_requests(self):
#         for url in self.start_urls:
#             yield scrapy.Request(url=url,
#                                  callback=self.parse_more,
#                                  # wait_time=30,
#                                  # wait_until=EC.presence_of_element_located((By.ID, 'zg_browseRoot'))
#                                  )
#
#     def parse_more(self, response):
#         # from scrapy.shell import inspect_response
#         # inspect_response(response,self)
#
#         # driver = response.request.meta.get('driver')
#         best_categories = response.css('ul#zg_browseRoot>ul>li')
#         for best_categorie in best_categories:
#             category = best_categorie.css('a::text').get()
#             category_url = best_categorie.css('a').attrib.get('href')
#
#             # print(more_button)
#             yield scrapy.Request(url=category_url,
#                                  callback=self.parse_more_pro,
#                                  # wait_time= 30,
#                                  # wait_until= EC.presence_of_element_located((By.ID, 'zg-ordered-list')),
#                                  cb_kwargs={'category': category})
#
#     def parse_more_pro(self, response, category):
#
#         # from scrapy.shell import inspect_response
#         # inspect_response(response, self)
#         # driver = response.request.meta.get('driver')
#
#         items = response.css('ol#zg-ordered-list li')
#         for item in items:
#             rank = item.css('span.zg-badge-text::text').get()  ##seller ranking,such as #1,#2 and so on
#             preview_img_link = item.css('span.aok-inline-block').css('img').attrib.get('src')  # absolute img path
#             item_url = item.css('span.aok-inline-block').css('a::attr(href)').extract_first()  # relative url
#             title = item.css('span.aok-inline-block').css('div.p13n-sc-truncate-desktop-type2::text').get().strip()
#             star = item.css('span.aok-inline-block').css(
#                 'div.a-icon-row>a>i>span::text').extract_first()  # stirng format
#             view_times = item.css('span.aok-inline-block').css(
#                 'div.a-icon-row a.a-size-small::text').get()  ##string of numbers
#             price = item.css('span.aok-inline-block').css('div.a-row span.a-color-price').get()  ## price span tag
#
#             yield scrapy.Request(url=response.urljoin(item_url),
#                                  callback=self.parse_item,
#                                  # wait_until= EC.presence_of_element_located((By.ID,'feature-bullets')),
#                                  cb_kwargs={
#                                      'category': category,
#                                      'rank': rank,
#                                      'preview_img_link': preview_img_link,
#                                      'title': title,
#                                      'star': star,
#                                      'view_times': view_times,
#                                      'price': price
#                                  })
#
#         # only crawl the first page items,which is 50 items
#         # next_page =response.css('ul.a-pagination li.a-last>a').attrib.get('href')
#         # if next_page:
#         #     yield SeleniumRequest(url=next_page,
#         #                           callback=self.parse_more_pro,
#         #                           wait_time= 30,
#         #                           wait_until=EC.presence_of_element_located((By.ID, 'zg-ordered-list')),
#         #                           cb_kwargs={'category':category})
#
#     def parse_item(self, response, rank, preview_img_link, title, star, view_times, price, category):
#         # from scrapy.shell import inspect_response
#         # inspect_response(response,self)
#         driver = response.request.meta.get('driver')
#         # element = WebDriverWait(driver, 20).until(
#         #     EC.presence_of_element_located((By.ID, 'acrCustomerReviewText'))
#         # )
#         item = AmzonItem()
#         item['url'] = response.url
#         item['title'] = title
#         item['features'] = response.css('div#feature-bullets').css('li span::text').getall()
#         item['rank'] = rank
#         item['preview_img_link'] = preview_img_link
#         item['star'] = star
#         item['view_times'] = view_times
#         item['price'] = price
#         item['category'] = category
#         item['crawl_time'] = datetime.now()
#
#         yield item
#
#
class AmzonTelsaSpider(scrapy.Spider):
    name = 'tesla_amazon'
    # allowed_domains = ['amazon.com']
    # start_urls = ['https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_0_amazon-devices_1']
    start_urls = [
        'https://www.amazon.com/s?k=tesla+accessories&crid=90RZC7XATMXS&sprefix=tesla+accessories%2Caps%2C438&ref=nb_sb_ss_ts-doa-p_1_17']
    for i in range(2,7):
        req_url = f'https://www.amazon.com/s?k=tesla+accessories&page={i} \
            &crid=90RZC7XATMXS&qid=1626309688&sprefix=\
            tesla+accessories%2Caps%2C438&ref=sr_pg_{i}'
        start_urls.append(req_url)
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

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(url=url,
                                  callback=self.parse_more,
                                  # wait_time=30,
                                  # wait_until=EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.a-pagination')),
                                  # cb_kwargs={'current_page':1}

                                  )

    def parse_more(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response,self)
        '''抓取商品链接及在本页能够获取的其他信息，并传递至下个函数内'''

        # driver = response.request.meta.get('driver')
        items = response.css('div.a-section.a-spacing-medium')
        for item in items:
            preview_img_url = item.css('img.s-image').attrib.get('src')
            item_name = item.css('h2.a-size-mini span::text').get()
            item_url = item.css('h2.a-size-mini a').attrib.get('href')
            item_star = item.css('i.a-star-small-4-5 span::text').get()
            # review_counts = item.css('span.a-size-base::text').get()
            review_url = item.css('a.a-link-normal').attrib.get('href')
            item_price = item.css('span.a-price-whole::text').get()
            # print(more_button)

            yield SeleniumRequest(url=response.urljoin(item_url),
                                  callback=self.parse_item,
                                  cb_kwargs={'preview_img_url': preview_img_url,
                                             'item_name': item_name,
                                             'item_star': item_star,
                                             # 'review_counts': review_counts,
                                             'review_url': review_url,
                                             'item_price': item_price})

    def parse_item(self, response, item_star, preview_img_url, item_name,  item_price, review_url):
        '''抓取商品的详细信息'''
        item = AmzonItem()
        from scrapy.shell import inspect_response
        inspect_response(response,self)
        item['item_url'] = response.url
        item['item_name'] = item_name
        item['features'] = response.css('div#feature-bullets').css('li span::text').getall()
        item['item_star'] = item_star
        item['preview_img_link'] = preview_img_url
        # item['star'] = sta
        reviews = response.css('span#acrCustomerReviewText::text').get()
        if reviews and isinstance(reviews,str):
            reviews = re.sub('[a-z,]','',reviews).strip()
            item['review_counts'] = int(reviews)
        else:
            item['review_counts'] = reviews
        item['item_price'] = item_price
        # item['category'] = category
        item['review_url'] = response.urljoin(review_url)
        item['crawl_time'] = datetime.now()

        yield item

