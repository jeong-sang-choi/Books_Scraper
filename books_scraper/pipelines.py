# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

client = MongoClient()

# class BooksScraperPipeline:
#     def process_item(self, item, spider):
#         return item
class BooksScraperPipeline:
    def __init__(self):
        # MongoDB 클라이언트 및 데이터베이스, 컬렉션 설정
        self.client = MongoClient("mongodb://localhost:27017/")  # MongoDB 연결 (로컬 기준)
        self.db = self.client["books_db"]  # 사용할 데이터베이스
        self.collection = self.db["books"]  # 사용할 컬렉션

    def process_item(self, item, spider):
        # 아이템을 MongoDB에 저장
        self.collection.insert_one(ItemAdapter(item).asdict())  # 아이템을 딕셔너리로 변환 후 저장
        return item

    def close_spider(self, spider):
        # 스파이더 종료 시 MongoDB 연결 닫기
        self.client.close()
