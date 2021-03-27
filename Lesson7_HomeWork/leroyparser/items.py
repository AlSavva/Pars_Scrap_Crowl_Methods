# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst, Compose
import urllib


def get_general(dictionary):
    dictionary = dictionary[0]
    general = {'name': dictionary['data-product-name'],
               'article': int(dictionary['data-product-id']),
               'price': float(dictionary['data-product-price'])
               }
    return general


def get_charakteristics(selector):
    characteristic = {}
    for key, value in zip(selector[::2], selector[1::2]):
        a = key.strip()
        try:
            b = float(value.strip())
        except ValueError:
            b = value.strip()

        characteristic.update({a: b})
        print()
    return characteristic


def get_main(link):
    link = link[0].decode('utf-8')
    if '&' in link:
        link = link.split('&')[0]
    link = link.split('=')[-1]
    main = urllib.parse.unquote(link)
    return main


class LeroyparserItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    _id = scrapy.Field()
    article = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field(
        output_processor=TakeFirst())  # т.к. получили список, выберем первое значение
    characteristic = scrapy.Field(
        output_processor=Compose(
            get_charakteristics))  # преобразуем полученный список в словарь
    photos = scrapy.Field()
    general = scrapy.Field(output_processor=TakeFirst(),
                           input_processor=Compose(
                               get_general))  # из полученного словаря выберем необходимые ключи
    main = scrapy.Field(output_processor=Compose(
        get_main))  # поле необходимо для создания структуры каталога фото
