import scrapy
from scrapy.http import HtmlResponse
from leroyparser.items import LeroyparserItem
from scrapy.loader import ItemLoader


class LeroyruSpider(scrapy.Spider):
    name = 'leroyru'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, query):
        super(LeroyruSpider, self).__init__()

        self.start_urls = []
        self.query = query
        for good in query:
            self.start_urls.append(f'https://leroymerlin.ru/search/?q={good}')

    def parse(self, response: HtmlResponse):
        links = response.xpath('//product-card/@data-product-url')
        for link in links:
            yield response.follow(link, callback=self.parse_item)
        next_page = response.xpath(
            '//div[@class="service-duplicate-panel-wrapper"]//div[@class="next-paginator-button-wrapper"]/a/@href').extract_first()  # т.к. результат response - SelectorList, используем extract_first()
        print()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_item(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroyparserItem(), response=response)
        loader.add_value('main', response.request.headers['Referer'])
        loader.add_value('general', response.xpath(
            '//div[@data-rel="js-detail-product-page"]').attrib)  # .attrib
        loader.add_xpath('characteristic',
                         '//div[@class="def-list__group"]//*/text()')  # .extract()
        loader.add_xpath('photos',
                         '//uc-pdp-media-carousel//source[contains(@media, "(min-width: 1024px)")]/@data-origin')
        loader.add_value('url', response.url)  # .extract()
        yield loader.load_item()
