import scrapy


class BooksSpider(scrapy.Spider):
    name = "books"
    
    def start_requests(self):
        yield scrapy.Request(url ="https://books.toscrape.com/", callback=self.parse_mainpage)


    def parse_mainpage(self, response):
        print("main_parse")
        category_links = response.css("div.side_categories ul li > a::attr(href)").getall()
        category_names = response.css("div.side_categories ul li > a::text").getall()

        
        for idx, category_link in enumerate(category_links):
            print("여기카테고리", category_names[idx])
            if category_names[idx].strip() == "Books":
                continue
            yield scrapy.Request(url = "https://books.toscrape.com/" + category_link, callback=self.parse_maincategory, meta = {"maincategory_name":category_names[idx]})
             

    def parse_maincategory(self, response):
        print("parse_maincategory",response.meta["maincategory_name"])

        item_list = response.css("div ol.row li")
        for each_item in item_list:

        #     title = each_item.css("h3 > a::text").get()
        #     price = float(each_item.css("p.price_color::text").get().replace("£",""))
        #     rating = each_item.css("p.star-rating::attr(class)").get()
        #     rating_class = int(self.convert_to_rating(rating))
        #     in_stock_yn = each_item.xpath("//*[@id='default']/div/div/div/div/section/div[2]/ol/li[3]/article/div[2]/p[2]/text()").get()
            image_url = each_item.css("div.image_container > a::attr(href)").get()
            absolute_image_url = response.urljoin(image_url)
            
            
            yield scrapy.Request(url = absolute_image_url, callback=self.sub_parse_maincategory, meta={"maincategory_name": response.meta["maincategory_name"]})
        next_page = response.css("li.next > a::attr(href)").get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            print(f"다음 페이지로 이동: {next_page_url}")
            
            # 다음 페이지로 이동
            yield scrapy.Request(
                url=next_page_url,
                callback=self.parse_maincategory,
                meta={"maincategory_name": response.meta["maincategory_name"]}
            )
    def sub_parse_maincategory(self, response):
        print("sub_parse_maincategory")
        category = response.meta["maincategory_name"]
        title = response.xpath("//*[@id='content_inner']/article/div[1]/div[2]/h1/text()").get()
        in_stock_yn = response.xpath("//*[@id='content_inner']/article/div[1]/div[2]/p[2]").get()
        if "In stock" in in_stock_yn:
            in_stock_yn = "Y"
        else:
            in_stock_yn = "N"
        rating = response.css("p.star-rating::attr(class)").get().strip()
        rating_class = int(self.convert_to_rating(rating))
        origin_image = response.css("div.thumbnail img::attr(src)").get()
        absolute_image_url = response.urljoin(origin_image).strip()
        print(category,absolute_image_url, rating_class)
        pass
        
        
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
            
            
 
            
    
