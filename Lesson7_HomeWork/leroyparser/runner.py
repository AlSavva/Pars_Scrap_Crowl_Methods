from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from leroyparser.spiders.leroyru import LeroyruSpider
from leroyparser import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    query = list(input(
        'Введите название товарa, или названия товаров через пробел: ').split())
    if not query:
        query = ['обои', 'фанера']
    process.crawl(LeroyruSpider, query=query)

    process.start()
