import scrapy


class BooksSpider(scrapy.Spider):
    name = "books"
    
    def start_requests(self):
        yield scrapy.Request(url ="https://books.toscrape.com/", callback=self.parse_mainpage)


    def parse_mainpage(self, response):
        category_links = response.css("div.side_categories ul li > a::attr(href)").getall()
        category_names = response.css("div.side_categories ul li > a::text").getall()
        
        for idx, category_link in enumerate(category_links):
            yield scrapy.Request(url = "https://books.toscrape.com/" + category_link, callback=self.parse_maincategory, meta = {"maincategory_name":category_names[idx]})
             

    def parse_maincategory(self, response):
        print("parse_maincategory",response.meta["maincategory_name"])
        item_list = response.css("div ol.row li")
        
        for each_item in item_list:
            int_rating = None
            
            title = each_item.css("h3 > a::text").get()
            price = float(each_item.css("p.price_color::text").get().replace("£",""))
            rating = each_item.css("p.star-rating::attr(class)").get()
            rating_class = int(self.convert_to_rating(rating))
            in_stock_yn = each_item.xpath("//*[@id='default']/div/div/div/div/section/div[2]/ol/li[3]/article/div[2]/p[2]/text()").get()
            image_url = each_item.css("div.image_container > a::attr(href)").get()
            absolute_image_url = response.urljoin(image_url)
            print(title,price,rating_class,absolute_image_url)
            
    # def sub_parse_maincategory(self, response):
    #     pass
        
        
    def convert_to_rating(self, rating):
        if "One" in rating:
            return 1
        elif "Two" in rating:
            return 2
        elif "Three" in rating:
            return 3
        elif "Four" in rating:
            return 4
        elif "Five" in rating:
            return 5 
            
            
         
        pass
 
            
    
