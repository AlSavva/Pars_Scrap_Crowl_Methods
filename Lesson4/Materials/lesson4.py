import requests
from lxml import html
from pprint import pprint

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}

main_url = 'https://ru.ebay.com/'
response = requests.get(main_url + 'b/Fishing-Equipment-Supplies/1492/bn_1851047', headers=header)

dom = html.fromstring(response.text)

items = dom.xpath('//li[contains(@class,"s-item")]')

fishing = []
for item in items:
    fishing_item = {}
    name = item.xpath('.//h3[@class="s-item__title"]/text()')
    price = item.xpath('.//span[@class="s-item__price"]//text()')
    image = item.xpath('.//img[@class="s-item__image-img"]/@src')
    add_info = item.xpath('.//span[contains(@class,"s-item__hotness")]/span/text()')

    fishing_item['name'] = name
    fishing_item['price'] = price
    fishing_item['image'] = image
    fishing_item['add_info'] = add_info

    fishing.append(fishing_item)

pprint(fishing)

print(len(add_info))
pprint(add_info)
