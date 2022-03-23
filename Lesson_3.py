import requests
from bs4 import BeautifulSoup
import re

from pymongo import MongoClient
from pymongo import errors
from pprint import pprint


client = MongoClient('127.0.0.1', 27017)
db = client['users2601']
headhunter = db.headhunter

url = 'https://hh.ru'
params = {'search_field': 'name',
          'text': 'Водитель',
          'page': ''}

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}

response = requests.get(url + '/search/vacancy', params=params, headers=headers)

dom = BeautifulSoup(response.text, 'html.parser')

#Находим номер последней страницы. При запросе "ветеринар", последняя страница 29, хотя на сайте 40 по-умолчанию.
#По факту это число может меняться и быть до 40, в зависимости от кол-ва вакансий.
last_page = int((dom.find('a', {'data-qa': 'pager-next'}).previous_sibling.getText())[3:])

for page in range(0, last_page):
    params['page'] = page

    vacancies_list = dom.find_all('div', {'class': 'vacancy-serp-item'})

    vacancies = []

    for vacancy in vacancies_list:

        info = vacancy.find('a', {'class': 'bloko-link'})
        name = info.getText()
        link = info.get('href')

#Находим зарплату и разбиваем на значения "от", "до" и "валюта".
        compensation = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})

        if not compensation:
            compensation_min = None
            compensation_max = None
            compensation_currency = None
        else:
            compensation = compensation.getText().replace(u' ', u'@')

            compensation = re.split(r'@', compensation)

            if compensation[0] == 'до':
                compensation_min = None
                compensation_max = int(compensation[1]).replace('\u202f', '')
                compensation_currency = compensation[2]
            elif compensation[0] == 'от':
                compensation_min = int((compensation[1]).replace('\u202f', ''))
                compensation_max = None
                compensation_currency = compensation[2]
            else:
                compensation_min = int((compensation[0]).replace('\u202f', ''))
                compensation_max = int((compensation[2]).replace('\u202f', ''))
                compensation_currency = compensation[3]

        vacancy_data = {"_id": link,
                   "name": name,
                   "salary_min": compensation_min,
                   "salary_max": compensation_max,
                   "salary_currency": compensation_currency,
                   "source": 'HH'}

#Задание 1
        try:
            headhunter.insert_one(vacancy_data)
        except errors.DuplicateKeyError:
            pass
            #print(f'Документ с полем {vacancy_data["_id"]} уже существует в базе')

#Задание 2. Надем вакансии с зарплатой от 100 до 175 тыс.

for name in headhunter.find({'salary_min': {'$gte': 100000}, 'salary_max': {'$lte': 175000}}):
    pprint(name)