# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo

# class AmzonPipeline:
#
#     collection_name = 'amzon_popular'
#
#     def __init__(self, mongo_uri, mongo_db):
#         self.mongo_uri = mongo_uri
#         self.mongo_db = mongo_db
#     #
#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(
#             mongo_uri=crawler.settings.get('MONGO_URI'),
#             mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
#         )
#     #
#     def open_spider(self, spider):
#         self.client = pymongo.MongoClient(self.mongo_uri)
#         self.db = self.client[self.mongo_db]
#
#     def close_spider(self, spider):
#         self.client.close()
#
#     def process_item(self, item, spider):
#
#         if not self.db[self.collection_name].find_one({'url': item.get('url')}):
#             self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
#         return item


class AmazonTelsaPipeline:

    # collection_name = 'amzon_popular'

    # def __init__(self, mongo_uri, mongo_db):
    #     self.mongo_uri = mongo_uri
    #     self.mongo_db = mongo_db
    #
    # @classmethod
    # def from_crawler(cls, crawler):
    #     return cls(
    #         mongo_uri=crawler.settings.get('MONGO_URI'),
    #         mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
    #     )
    #
    # def open_spider(self, spider):
    #     # self.client = p
    #     self.db = spider.client[spider.mongo_db]

    def process_item(self, item, spider):
    #
    #     if not spider.db[spider.collection].find_one({'item_url': item.get('item_url')}):
        spider.db[spider.collection].insert_one(ItemAdapter(item).asdict())
        return item