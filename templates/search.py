from selenium import webdriver
import urllib.parse
from bs4 import BeautifulSoup
from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbsparta

driver = webdriver.Chrome("C:/Users/SamSung/Downloads/chromedriver_win32/chromedriver")

plusUrl = urllib.parse.quote_plus(input('검색어를 입력하세요'))

url = f'https://search.kyobobook.co.kr/web/search?vPstrKeyWord={plusUrl}&orderClick=LET'

driver.get(url)

req = driver.page_source

soup = BeautifulSoup(req, 'html.parser')

books = soup.select('#search_list > tr')

db.kyobo.drop()

for count, book in enumerate(books):
    image = book.select_one('td.image > div.cover > a > img')['src']
    title = book.select_one('td.detail > div.title > a').text
    author = book.select_one('td.detail > div.author > a').text.strip()
    price = book.select_one('td.price > div.org_price').text

    doc = {
        'image': image,
        'title': title,
        'author': author,
        'price': price,
    }

    db.kyobo.insert_one(doc)
    print('완료!', title)

    if count == 4:
        break
