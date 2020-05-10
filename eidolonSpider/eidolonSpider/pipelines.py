# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient


class EidolonspiderPipeline:
    def process_item(self, item, spider):
        return item


# class MongoPipeline:
#     def __init__(self):
#         passwd = "glory1999"  # input("Enter mongoDB password: ")
#         db = MongoClient("mongodb+srv://ayglory:{}@cluster0-jv8w4.gcp.mongodb.net/test?retry"
#                          "Writes=true&w=majority".format(passwd))
#         self.collection = db["eidolonDB"]["questions"]
#
#     def process_item(self, item, spider):
#         good_item = True
#         for value in item:
#             if not value:
#                 good_item = False
#                 break
#         if good_item:
#             self.collection.insert(dict(item))
#             print("[SUCCESS] One item saved successfully")
#
#         return "GOOD RESPONSE"


class MongoPipeline:

    collection_name = 'questions'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        passwd = "glory1999"  # input("Enter mongoDB password: ")
        return cls(
            mongo_uri="mongodb+srv://ayglory:{}@cluster0-jv8w4.gcp.mongodb.net/test?retry"
                      "Writes=true&w=majority".format(passwd),
            mongo_db="eidolonDB"
        )

    def open_spider(self, spider):
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item
