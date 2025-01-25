import scrapy


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        books = response.css("ol.row li")
        count_check = 0  # 페이지 내에서 처리한 항목 수를 카운트

        for book in books:
            title = book.css("h3 > a::attr(title)").get()
            price = book.css("p.price_color::text").get().replace("£", "")
            
            # 별점 클래스에서 숫자 변환 처리
            rating_class = book.css("p.star-rating::attr(class)").get()
            if "One" in rating_class:
                int_rating = 1
            elif "Two" in rating_class:
                int_rating = 2
            elif "Three" in rating_class:
                int_rating = 3
            elif "Four" in rating_class:
                int_rating = 4
            elif "Five" in rating_class:
                int_rating = 5
            else:
                int_rating = None

            in_stock = "Y" if "In stock" in book.css("p.instock.availability::text").get() else "N"
            category = response.css("ul.breadcrumb li:nth-child(3) > a::text").get()
            image_url = book.css("img::attr(src)").get()
