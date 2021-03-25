# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst

def process_url(value):
    if value:
        value = value.replace('/s/', '/b/')
    return value

def FirstWord(value):
    return value.split()[0]

class OtparserItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(process_url))
    url = scrapy.Field()
    someString = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(FirstWord()))

    # someString = 'shdbfakhs asdhasdf a aidbasidua a'
