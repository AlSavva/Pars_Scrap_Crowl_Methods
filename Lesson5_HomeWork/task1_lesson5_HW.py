# Написать программу, которая собирает входящие письма из своего или тестового
# почтового ящика и сложить данные о письмах в базу данных:
# отправитель,
# дата отправки,
# тема письма,
# текст письма.
# Логин тестового ящика: study.ai_172@mail.ru
# Пароль тестового ящика: NextPassword172
# chrome://version/ 89.0.4389.90

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
import pymongo.errors
import time


def _scrap_mail(email='study.ai_172@mail.ru', password='NextPassword172',
                n_messages=30):
    """
    функция собирает входящие сообщения с почтового ящика mail.ru.
    количество сообщений задается параметром n_messages, если сообщений в
    почтовом ящике меньше, будут собраны все

    :param email: str, default: 'study.ai_172@mail.ru'
    :param password: str, default: 'NextPassword172'
    :param n_messages - количество сообщений для сбора: int, default: 30
    :return: list of dictionaries
    """
    chrome_options = Options()
    chrome_options.add_argument('start-maximized')
    driver = webdriver.Chrome(executable_path='../chromedriver',
                              options=chrome_options)
    driver.get('https://mail.ru/')
    login = driver.find_element_by_name('login')
    login.send_keys(email)
    login.send_keys(Keys.ENTER)
    time.sleep(.5)

    psw = driver.find_element_by_name('password')
    psw.send_keys(password)
    psw.send_keys(Keys.ENTER)
    time.sleep(2)
    all_mails = []

    link_list = [] # в список сложим ссылки на сообщения
    len_chek = 0 #переменная для контроля изменения длинны списка ссылок
    while len(link_list) < n_messages:
        links = driver.find_elements_by_xpath('//a[@data-id]')
        for item in links:
            link = item.get_property('href')
            link_list.append(link)
            link_list = list(set(link_list)) # удалим дубликаты ссылок из списка
            if len(link_list) == n_messages: # закончим, если собрали нужное количество ссылок
                break
        if len_chek == len(link_list): # если не добавилось новых ссылок, значит собрали все сообщения в ящике
            break
        else:
            len_chek = len(link_list)
        chek = driver.find_element_by_xpath(
            f'//a[@href="{link.replace("https://e.mail.ru", "")}"]') # перейдем на последний WebElemrnt
        chek.send_keys(Keys.PAGE_DOWN) # с помощью PAGE_DOWN прокрутим сообщения вниз
    # собираем данные с сообщений, переходя по ссылкам
    for link in link_list:
        driver.get(link)
        time.sleep(2)
        data = {}
        message = driver.find_element_by_xpath(
            '//div[contains(@class, "thread ")]')
        data['message_id'] =link.split(':')[2]
        data['subject'] = message.find_element_by_xpath("//h2").text
        data['sender'] = message.find_element_by_xpath(
            "//div[@class='letter__author']/*").get_attribute('title')
        data['sender_name'] = message.find_element_by_xpath(
            "//div[@class='letter__author']/span").text
        data['date'] = message.find_element_by_xpath(
            "//div[@class='letter__date']").text
        data['body'] = message.find_element_by_xpath(
            "//div[@class='letter__body']").text
        all_mails.append(data)
        time.sleep(0.9)
    return all_mails


def add_messages(email='study.ai_172@mail.ru', password='NextPassword172',
                 n_messages=30, base_name='mail_inbox'):
    """
    функция обновляет базу входящих сообщений почтовика mail.ru. По умолчанию
    установлена база "mail_inbox", базу можно выбрать,
    если выбранной базы не существует, она будет создана.

    :param email: str, default: 'study.ai_172@mail.ru'
    :param password: str, default: 'NextPassword172'
    :param n_messages: int, default: 30
    :param base_name: str, default: 'm_video_hits'
    :return:
    """
    client = MongoClient('localhost', 27017)
    if base_name not in client.list_database_names():
        print(f'Создана база {base_name}!')
    db = client[base_name]
    inbox = db.inbox
    inbox.create_index("message_id", unique=True)
    print(f'База {base_name} обновлена!')
    count = 0  # счетчик уникальных сообщений
    total_count = 0  # счетчик скачаных сообщений
    for _ in _scrap_mail(email=email, password=password,
                         n_messages=n_messages):
        # обрабатываем ошибку дубликата индекса
        try:
            inbox.insert_one(_)
            count += 1
            total_count += 1
        except pymongo.errors.DuplicateKeyError:
            total_count += 1
            continue
    print(
        f'Сообщений найдено: {total_count}, новых сообщений добавлено: {count}.')


add_messages()

# print(all_mails)
# driver.quit()


# print(len(all_mails))

# time.sleep(3)
# back=driver.find_element_by_xpath('//span[contains(@class,"button2") and @title="Вернуться"]')
# back.click()
# driver.send_keys(Keys.PAGE_DOWN)
# for link in set(link_lst):
# driver.get(link)
# if len(set(link_list))<50:
#     driver.get(link_list[-1])
#     time.sleep(2)
#     back = driver.find_element_by_xpath(
#          '//span[contains(@class,"button2") and @title="Вернуться"]')
#     back.click()
#     #links[-1].send_keys(Keys.PAGE_DOWN)
#     link_list=list(set(link_list))
