import scrapy
from scrapy.http import HtmlResponse
from otparser.items import OtparserItem
from scrapy.loader import ItemLoader

class OtruSpider(scrapy.Spider):
    name = 'otru'
    allowed_domains = ['onlinetrade.ru']

    def __init__(self, query):
        super(OtruSpider, self).__init__()

        self.start_urls = [f'https://www.onlinetrade.ru/sitesearch.html?query={query}']

    def parse(self, response:HtmlResponse):
        goods_links = response.xpath("//a[@class='indexGoods__item__name']")
        for link in goods_links:
            yield response.follow(link, callback=self.parse_good)


    def parse_good(self, response:HtmlResponse):
        loader = ItemLoader(item=OtparserItem(), response=response)
        loader.add_css('name', "h1::text")
        loader.add_xpath('photos', "//img[@class='displayedItem__images__thumbImage']/@src")
        loader.add_value('url', response.url)
        # loader.add_css()
        yield loader.load_item()


        # name = response.xpath("//h1/text()").extract_first()
        # photos = response.xpath("//img[@class='displayedItem__images__thumbImage']/@src").extract()
        # yield OtparserItem(name=name, photos=photos)