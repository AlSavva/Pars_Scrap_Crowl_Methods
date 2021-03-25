from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from otparser.spiders.otru import OtruSpider
from otparser import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    # input('')
    process.crawl(OtruSpider, query='MSI')

    process.start()