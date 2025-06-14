import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class CrawlingSpider(CrawlSpider):
    name = "mycrawler"
    allowed_domains = ["toscrape.com"]
    start_urls = ["http://books.toscrape.com/"]

    rules = (
        Rule(LinkExtractor(allow=["catalogue/category"]), follow=True),
        Rule(LinkExtractor(allow=["catalogue"], deny=["category"]), callback="parse_item")
    )

    def parse_item(self, response):
        # Parse the item from the response
        yield {
            "title": response.css(".product_main h1::text").get(),
            "price": response.css(".price_color::text").get(),
            "availability": response.css(".availability::text").re_first(r'\n\s*(\w.*)\n').strip()
        }

# Run the spider using: scrapy runspider <script_name>.py
