# Написать приложение, которое собирает основные новости с сайтов news.mail.ru,
# lenta.ru, yandex-новости. Для парсинга использовать XPath. Структура данных
# должна содержать:
# название источника;
# наименование новости;
# ссылку на новость;
# дата публикации.

import requests
from lxml import html
import re
import datetime
from pymongo import MongoClient
import pymongo.errors


def _scrap_lenta():
    """
    Вспомогательная функция для скрапа Lenta.ru. Собирает с главной страницы
    новости из главного блока (10 новостей), и из блока 'Главные новости'(там
    размещено от 8 до 10 новостей)

    :return: list of dictionaries
    """
    main_link = 'https://lenta.ru'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 \
        Safari/537.36'}
    response = requests.get(main_link, headers=header)
    if response.ok:
        item = html.fromstring(response.text)
        news = item.xpath('.//div[@class="first-item" or @class="item"]')
        lenta_news = []
        for n in news:
            news_data = {}
            news_data['title'] = n.xpath("./descendant::a/text()")[0].replace(
                u'\xa0', ' ')
            link_text = n.xpath("./a/@href")[0]
            # иногда в главный блок попадают новости с "аффилированных"
            # источников lenta.ru, например moslenta.ru и motor.ru, чтобы не
            # ломался скрапер пришлось обрабатывать условие:
            if 'https' not in link_text:
                news_data['source'] = 'Lenta.ru'
                news_data['link'] = main_link + link_text
                # дату новости можно извлечь из текста ссылки, к сожалению,
                # Mongo не примет datetime.date(только datetime.datetime) сохра
                # няем дату публикации в виде строки формата "YYYY-MM-DD"
                date_list = link_text.strip('/').split('/')[1:4]
                news_data['date'] = '-'.join(date_list[i] for i in range(3))
            else:
                news_data['source'] = link_text.split('/')[2]
                date_list = re.findall(r'\d{2}-\d{2}-\d{4}', link_text)[
                    0].split('-')
                news_data['link'] = link_text
                news_data['date'] = '-'.join(
                    date_list[::-1][i] for i in range(3))
            lenta_news.append(news_data)
        return lenta_news


def _scrap_yanews():
    """
    Вспомогательная функция для скрапа yandex.ru/news, собирает главные новости
     со страницы (блок содержит 5 новостей)

    :return: list of dictionaries
    """
    main_link = 'https://yandex.ru/news'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 \
        Safari/537.36'}
    response = requests.get(main_link, headers=header)
    if response.ok:
        item = html.fromstring(response.text)
        news = item.xpath(
            '//div[contains(@class, "news-top-flexible-stories" )]/div')
        yandex_news = []
        for n in news:
            news_data = {}
            news_data['title'] = n.xpath(".//h2/text()")[0].replace(u'\xa0',
                                                                    ' ')
            news_data['link'] = \
                n.xpath('.//*[contains(@class, "mg-card__")]/a/@href')[0]
            source_time = n.xpath(
                './/div[@class="mg-card-footer__left"]//text()')
            # source_time дает на выходе список из 2 элементов, первый элемент
            # источник, второй - время публикации в формате "чч-мм", если
            # новость вчерашняя, то второй элемент содержит "Вчера", в
            # соответствии с этим извлекаем значения
            news_data['source'] = source_time[0]
            today = datetime.date.today()
            news_data['date'] = today.strftime('%Y-%m-%d') if \
                'Вчера' not in source_time[1] else today.replace(
                day=today.day - 1).strftime('%Y-%m-%d')
            yandex_news.append(news_data)
        return yandex_news


def _scrap_mail():
    """
    Вспомогательная функция для скрапа news.mail.ru, собирает главные новости
    со страницы (блок содержит 5 иллюстрированных новостей, и 6 новостей в виде
    ссылок)

    :return: list of dictionaries
    """
    main_link = 'https://news.mail.ru/'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
    response = requests.get(main_link, headers=header)
    if response.ok:
        item = html.fromstring(response.text)
        # поскольку, для получения источника новости и даты пубикации всё равно
        # придется посылать отдельный запрос на страницу новости, имеет смысл и
        # остальную информацию получать оттуда. Собираем ссылки на новости в
        # множество, поскольку некоторые ссылки дублируются
        news_links = set(item.xpath(
            '//div[@class="js-module" and @data-module="TrackBlocks"]//a/@href'))
        mail_news = []
        # собираем данные для каждой новости отдельным запросом
        for link in news_links:
            inner_response = requests.get(link, headers=header)
            if inner_response.ok:
                new_item = html.fromstring(inner_response.text)
                news = new_item.xpath(
                    '//div[contains(@class, "js-article")]')
                for n in news:
                    news_data = {}
                    news_data['link'] = link
                    news_data['title'] = n.xpath('.//h1/text()')[0].replace(
                        u'\xa0', ' ')
                    news_data['source'] = n.xpath('.//a//text()')[0]
                    news_data['date'] = \
                        n.xpath('.//*/@datetime')[0].split('T')[0]
                    mail_news.append(news_data)
        return mail_news


def news_scrap(lenta=True, yandex=True, mail=True):
    """
    Функция для сбора новостей с Lenta.ru, yandex.ru/news, и news.mail.ru.
    ресурсы для сбора можно выбрать указав булевы значения для аргументов
    функции.

    :param lenta: boolean, default: True
    :param yandex: boolean, default: True
    :param mail: boolean, default: True
    :return: list of dictionaries
    """
    all_news = []
    if lenta:
        all_news.extend(_scrap_lenta())
    if yandex:
        all_news.extend(_scrap_yanews())
    if mail:
        all_news.extend(_scrap_mail())
    return all_news


def add_news(lenta=True, yandex=True, mail=True, base_name=None):
    """
    функция обновляет базу новостей полученных с Lenta.ru, yandex.ru/news, и
    news.mail.ru. По умолчанию установлена база "top_news", базу можно выбрать,
    если выбранной базы не существует, она будет создана.

    :param lenta: boolean, default: True
    :param yandex: boolean, default: True
    :param mail: boolean, default: True
    :param base_name: str, default: None
    :return:
    """
    client = MongoClient('localhost', 27017)
    if not base_name:
        base_name = 'top_news'
    if base_name not in client.list_database_names():
        print(f'Создана база {base_name}!')
    db = client[base_name]
    news = db.news
    news.create_index('title', unique=True)
    print(f'База {base_name} обновлена!')
    count = 0  # счетчик уникальных новостей
    total_count = 0  # счетчик скачаных новостей
    for _ in news_scrap(lenta=lenta, yandex=yandex, mail=mail):
        # обрабатываем ошибку дубликата индекса
        try:
            news.insert_one(_)
            count += 1
            total_count += 1
        except pymongo.errors.DuplicateKeyError:
            total_count += 1
            continue
    print(f'Новостей найдено: {total_count}, новостей добавлено: {count}.')


add_news()
