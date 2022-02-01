from pprint import pprint
from lxml import html
import requests
from pymongo import MongoClient
from pymongo import errors

client = MongoClient('127.0.0.1', 27017)
db = client['users0102']
lentaru = db.lentaru

url = 'https://lenta.ru/'
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 '
                         'Safari/537.36'}

response = requests.get(url, headers=headers)

dom = html.fromstring(response.text)
items = dom.xpath("//a[@class='card-mini _topnews']")
articles = []

for item in items:
    article = {}
    topic = item.xpath(".//span[@class='card-mini__title']/text()")
    link = item.xpath("@href")
    date = item.xpath(".//div[@class='card-mini__info']//text()")

    article['topic'] = topic
    article['link'] = link
    article['date'] = date
    article['source'] = 'Lenta.ru'

    article = {"_id": link,
               "topic": topic,
               "date": date,
               "source": 'Lenta.ru'}

    articles.append(article)

    try:
        lentaru.insert_one(article)
    except errors.DuplicateKeyError:
        print(f'Документ с полем {article["_id"]} уже существует в базе')

pprint(articles)



