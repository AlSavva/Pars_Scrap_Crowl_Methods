# Pars_Scrap_Crowl_Methods
### <center>Практические задания по курсу "Методы сбора и обработки данных при помощи Python" Geekbrains
Лекции разнесены по дирректориям, каждая содержит поддиректории "Materials" - с материалами лекций и "HomeWork" с выполненными заданиями.
### Lesson1. Основы клиент-серверного взаимодействия. Парсинг API  
#### Lesson1 task:
1.   Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя, сохранить JSON-вывод в файле *.json.
1.   Изучить список открытых API (https://www.programmableweb.com/category/all/apis). Найти среди них любое, требующее авторизацию (любого типа). Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.  

*Если нет желания заморачиваться с поиском, возьмите API вконтакте (https://vk.com/dev/first_guide). Сделайте запрос, чтобы получить список всех сообществ на которые вы подписаны.*

### Lesson2. Парсинг HTML. BeautifulSoup, MongoDB  
#### Lesson2 task:
* <ins>Вариант 1</ins>
Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы) с сайтов Superjob и HH. Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы). Получившийся список должен содержать в себе минимум:  
  * Наименование вакансии.
  * Предлагаемую зарплату (отдельно минимальную и максимальную).
  * Ссылку на саму вакансию.
  * Сайт, откуда собрана вакансия.     

*По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение). Структура должна быть одинаковая для вакансий с обоих сайтов. Общий результат можно вывести с помощью dataFrame через pandas.*  

* <ins>Вариант 2</ins>
Необходимо собрать информацию по продуктам питания с сайтов:  
[Роскачество официальный сайт. Исследование качества продуктов питания | Рейтинг товаров.](https://rskrf.ru/ratings/produkty-pitaniya/)    
[Список протестированных продуктов на сайте Росконтроль.рф](https://roscontrol.com/category/produkti/#)  
Получившийся список должен содержать:
  * Наименование продукта.
  * Категорию продукта (например «Бакалея»).
  * Подкатегорию продукта (например «Рис круглозерный»).
  * Параметр «Безопасность».
  * Параметр «Качество».
  * Общий балл.
  * Сайт, откуда получена информация.     

*Структура должна быть одинаковая для продуктов с обоих сайтов. Общий результат можно вывести с помощью dataFrame через Pandas.*
