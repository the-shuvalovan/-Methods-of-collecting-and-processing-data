from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import time
from pprint import pprint
from pymongo import MongoClient
from pymongo import errors

client = MongoClient('127.0.0.1', 27017)
db = client['users0102']
vkusvill = db.vkusvill
vv = []

chrome_options = Options()
chrome_options.add_argument("start-maximized")

#Мак заставил более точный адрес драйвера указать, поэтому стоит перепроверить/исправить перед запуском.
driver = webdriver.Chrome(executable_path='../chromedriver', options=chrome_options)
driver.implicitly_wait(10)

driver.get('https://msk.vkusvill.ru/goods/kulinariya/')

#Все всплывающие окна закрываются сами через 10 секунд, поэтому просто поставим таймер.
time.sleep(12)

pages = 0
while pages < 5:
    wait = WebDriverWait(driver, 10)
    button = driver.find_element(By.CLASS_NAME, 'js-catalog-load-more')
    button.click()
    pages += 1
#После нажантия кнопки всплывает анимация загрузки, ждем пока пропадет.
    time.sleep(3)

goods = driver.find_elements(By.CLASS_NAME, 'ProductCards__item')
for good in goods:
    name = good.find_element(By.CLASS_NAME, 'js-datalayer-catalog-list-name').text
    weight = good.find_element(By.CLASS_NAME, 'ProductCard__weight').text
    price = good.find_element(By.CLASS_NAME, 'Price__value').text
    price2 = f'{price} рублей'

    item = {"_id": name,
            "weight": weight,
            "price": price2,
            "store": 'VkusVill'}

    try:
        vkusvill.insert_one(item)
    except errors.DuplicateKeyError:
        print(f'Товар {item["_id"]} уже существует в базе')

        # vv.append(item)

# pprint(vv)