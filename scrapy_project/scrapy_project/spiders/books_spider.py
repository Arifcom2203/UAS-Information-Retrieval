import scrapy


class BooksSpider(scrapy.Spider):
    name = "books"

    allowed_domains = ["books.toscrape.com"]

    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):

        books = response.css("article.product_pod")

        for book in books:

            yield {

                "title": book.css("h3 a::attr(title)").get(),

                "price": book.css("p.price_color::text").get(),

                "availability": book.css(
                    "p.instock.availability::text"
                ).getall()[-1].strip(),

                "rating": book.css("p.star-rating::attr(class)").get().replace(
                    "star-rating ", ""
                ),

            }

        next_page = response.css("li.next a::attr(href)").get()

        if next_page:

            yield response.follow(next_page, callback=self.parse)