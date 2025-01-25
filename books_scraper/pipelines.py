
from itemadapter import ItemAdapter
from pymongo import MongoClient


class BooksScraperPipeline:
    def __init__(self):

        self.client = MongoClient("mongodb://localhost:27017/")  
        self.db = self.client["books_db"]  
        self.collection = self.db["books"]  

    def process_item(self, item, spider):
        # 아이템을 MongoDB에 저장
        self.collection.insert_one(ItemAdapter(item).asdict()) 
        return item

    def close_spider(self, spider):
        self.client.close()
