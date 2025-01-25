# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BooksScraperItem(scrapy.Item):
    category = scrapy.Field()
    title = scrapy.Field()
    rating_class = scrapy.Field()
    image_url = scrapy.Field()
    in_stock_yn = scrapy.Field()
    price = scrapy.Field()
    
    pass
