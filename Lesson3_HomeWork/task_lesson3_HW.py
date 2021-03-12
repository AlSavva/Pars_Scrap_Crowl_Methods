# 1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и
# реализовать функцию, записывающую собранные вакансии в созданную БД.
# 2. Написать функцию, которая производит поиск и выводит на экран вакансии с
# заработной платой больше введённой суммы.
# 3. Написать функцию, которая будет добавлять в вашу базу данных только новые
# вакансии с сайта.

from pymongo import MongoClient
import pymongo.errors  # для обработки ошибок
from pprint import pprint
from job_scrap import vacancy_finder  # импортируем наш скрапер

client = MongoClient('localhost', 27017)
db = client.job_offert  # создали бд

# my_data = vacancy_finder('кочегар') # собрали данные для вставки

vacancy = db.vacancy  # создали коллекцию


# vacancy.insert_many(main_data) # первоначально заполнили базу

# создаем уникальный индекс для поля 'vacancy_id' для исключения дубликатов при
# добавлении в базу, предварительно чуть подправил скрапер, что-бы он собирал
# эту информацию

# vacancy.create_index('vacancy_id', unique=True)


# функция поиска работы с заданным уровнем зарплаты

def find_me_job(min_salary=None, collection=db.vacancy):
    if not min_salary:
        min_salary = float(input('Укажите минимальный размер зарплаты: '))
    find_dict = {'$or': [{'min_salary': {'$gte': min_salary}},
                         {'max_salary': {'$gte': min_salary}}]}
    show_dict = {'_id': 0, 'source': 0}
    result = collection.find(find_dict, show_dict)
    print(f'Найдено {collection.count_documents(find_dict)} '
          f'вакансий с зарплатой от {min_salary:.2f}.')
    for n in result:
        pprint(n)


find_me_job()


def add_new_vacancy(job, collection=db.vacancy):
    count = 0  # счетчик уникальных вакансий
    total_count = 0  # счетчик скачаных вакансий
    for _ in vacancy_finder(job):
        # обрабатываем ошибку дубликата индекса
        try:
            collection.insert_one(_)
            count += 1
            total_count += 1
        except pymongo.errors.DuplicateKeyError:
            total_count += 1
            continue
    print(f'Найдено {total_count} вакансий. Добавлено {count} новых вакансий.')


add_new_vacancy('аналитик')

# проверка на уникальность

# m = vacancy.aggregate([
#     {"$group": {"_id": "$link", "count": {"$sum": 1}}},
#     {"$match": {"count": {"$gt": 1}}},
#     {"$sort": {"count": -1}},
#     {"$project": {"link": "$_id", "_id": 0, 'count': '$count'}}]
# )
# for i in m:
#     pprint(i)
