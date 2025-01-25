import scrapy


class BooksSpider(scrapy.Spider):
    name = "books"
    
    def start_requests(self):
        yield scrapy.Request(url ="https://books.toscrape.com/", callback=self.parse_mainpage)


    def parse_mainpage(self, response):
        category_links = response.css("div.side_categories ul li > a::attr(href)").getall()
        category_names = response.css("div.side_categories ul li > a::text").getall()
        
        for idx, category_link in enumerate(category_links):
            print("https://books.toscrape.com/" + category_link, category_names[idx].strip())

        pass
 
            
    
