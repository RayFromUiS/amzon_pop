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

class AmzonPopularSpider(scrapy.Spider):
    name = 'amzon_spider'
    allowed_domains = ['amazon.com']
    start_urls = ['https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_0_amazon-devices_1']
    # collection_name = 'amzon_popular'
    custom_settings = {
        'ITEM_PIPELINES': {'amzon.pipelines.AmzonPipeline': 300}
    }

    # def __init__(self,mongo_uri,mongo_db):
    # #     uri = 'mongodb://localhost:27017'
    # #     conn = pymongo.MongoClient(uri)
    # #     self.db = conn["amzon"]
    # #     self.collection = self.db["amzonPopularItem"]
    #     self.client = pymongo.MongoClient(mongo_uri)
    #     self.db = self.client[mongo_db]
    #     self.collection = self.db[self.collection_name]
    #
    # @classmethod
    # def from_crawler(cls, crawler):
    #     return cls(
    #         mongo_uri=crawler.settings.get('MONGO_URI'),
    #         mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
    #     )

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url,
                                  callback=self.parse_more,
                                  # wait_time=30,
                                  # wait_until=EC.presence_of_element_located((By.ID, 'zg_browseRoot'))
                                  )

    def parse_more(self,response):
        # from scrapy.shell import inspect_response
        # inspect_response(response,self)

        # driver = response.request.meta.get('driver')
        best_categories = response.css('ul#zg_browseRoot>ul>li')
        for best_categorie in best_categories:
            category = best_categorie.css('a::text').get()
            category_url = best_categorie.css('a').attrib.get('href')

        # print(more_button)
            yield scrapy.Request(url=category_url,
                              callback=self.parse_more_pro,
                            # wait_time= 30,
                             # wait_until= EC.presence_of_element_located((By.ID, 'zg-ordered-list')),
                              cb_kwargs={'category':category})

    def parse_more_pro(self,response,category):

        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        # driver = response.request.meta.get('driver')

        items = response.css('ol#zg-ordered-list li')
        for item in items:
            rank = item.css('span.zg-badge-text::text').get() ##seller ranking,such as #1,#2 and so on
            preview_img_link = item.css('span.aok-inline-block').css('img').attrib.get('src') #absolute img path
            item_url = item.css('span.aok-inline-block').css('a::attr(href)').extract_first() #relative url
            title = item.css('span.aok-inline-block').css('div.p13n-sc-truncate-desktop-type2::text').get().strip()
            star = item.css('span.aok-inline-block').css('div.a-icon-row>a>i>span::text').extract_first() #stirng format
            view_times = item.css('span.aok-inline-block').css('div.a-icon-row a.a-size-small::text').get() ##string of numbers
            price = item.css('span.aok-inline-block').css('div.a-row span.a-color-price').get() ## price span tag

            yield scrapy.Request(url=response.urljoin(item_url),
                                  callback=self.parse_item,
                                  # wait_until= EC.presence_of_element_located((By.ID,'feature-bullets')),
                                  cb_kwargs={
                                      'category':category,
                                      'rank':rank,
                                      'preview_img_link':preview_img_link,
                                      'title':title,
                                      'star':star,
                                      'view_times':view_times,
                                      'price':price
                                  })


        #only crawl the first page items,which is 50 items
        # next_page =response.css('ul.a-pagination li.a-last>a').attrib.get('href')
        # if next_page:
        #     yield SeleniumRequest(url=next_page,
        #                           callback=self.parse_more_pro,
        #                           wait_time= 30,
        #                           wait_until=EC.presence_of_element_located((By.ID, 'zg-ordered-list')),
        #                           cb_kwargs={'category':category})

    def parse_item(self,response,rank,preview_img_link,title,star,view_times,price,category):
        # from scrapy.shell import inspect_response
        # inspect_response(response,self)
        driver = response.request.meta.get('driver')
        # element = WebDriverWait(driver, 20).until(
        #     EC.presence_of_element_located((By.ID, 'acrCustomerReviewText'))
        # )
        item = AmzonItem()
        item['url'] =response.url
        item['title'] = title
        item['features'] = response.css('div#feature-bullets').css('li span::text').getall()
        item['rank'] = rank
        item['preview_img_link'] = preview_img_link
        item['star'] = star
        item['view_times'] = view_times
        item['price'] = price
        item['category'] = category
        item['crawl_time'] = datetime.now()

        yield item

        # element = driver.find_element_by_id('acrCustomerReviewLink')
        # driver.execute_script("arguments[0].click();", element)
        # yield SeleniumRequest(url=driver.current_url,
        #                       callback=self.parse_reviews,
        #                       # wait_time= 30,
        #                       # wait_until= EC.presence_of_element_located((By.ID, 'reviewsMedley')),
        #                       cb_kwargs={'item':item})

    # def parse_reviews(self,response,item):
    #
    #     # from scrapy.shell import inspect_response
    #     # inspect_response(response, self)
    #     if item.get('item_views'):
    #         item_reviews=item.get('item_views')
    #     else:
    #         item_reviews = []
    #     # item_reviews = []
    #     reviews = response.css('div#cm-cr-dp-review-list').css('div.review-text-content')
    #
    #     for review in reviews:
    #         item_reviews.append(review.css('span::text').get())
    #     ## click laoding all the views
    #     driver = response.request.meta.get('driver')
    #     load_all_reviews=driver.find_element_by_id('cr-pagination-footer-0')
    #     load_all_review_link = load_all_reviews.find_element_by_tag_name('a')
    #     driver.execute_script("arguments[0].click();", load_all_review_link)
    #
    #     # all_pages = res.css('div#cr-pagination-footer-0').css('a.a-link-emphasis').attrib.get('href')
    #     res = Selector(text=driver.page_source)
    #     next_page = res.css('ul.a-pagination').css('li.a-last a').attrib.get('href')
    #     if next_page:
    #         yield SeleniumRequest(response.urljoin(next_page),
    #                               callback=self.parse_reviews,
    #                               # wait_time=30,
    #                               # wait_until= EC.presence_of_element_located((By.ID, 'cm-cr-dp-review-list')),
    #                               cb_kwargs={'item':item})
    #     item['reviews'] = item_reviews
    #     yield item
    #







