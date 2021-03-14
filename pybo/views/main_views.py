from flask import Blueprint, render_template, request, jsonify, url_for
import requests
from bs4 import BeautifulSoup
from datetime import datetime

from selenium import webdriver

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/clock')
def clock():
    return render_template('clock.html')

@bp.route('/stock', methods=['POST'])
def stock():
    # company_codes = ["005930", "000660", "005380"]
    data = request.get_json()
    code1 = data['code1']
    code2 = data['code2']
    code3 = data['code3']

    company_codes = []
    company_codes.append(code1)
    company_codes.append(code2)
    company_codes.append(code3)

    prices = []
    for item in company_codes:
        now_price = get_price(item)
        prices.append(now_price)

    sise = {
        'code1': prices[0], 'code2': prices[1], 'code3': prices[2]
    }

    return jsonify(result2= "ok", result3= sise, now= datetime.today())

def get_price(company_code):
    bs_obj = get_bsoup(company_code)
    no_today = bs_obj.find("p", {"class": "no_today"})
    blind = no_today.find("span", {"class": "blind"})

    now_price = blind.text
    return now_price

def get_bsoup(company_code):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    url = "https://finance.naver.com/item/main.nhn?code=" + company_code

    result = requests.get(url, headers=headers)
    if result.status_code == 200:
        bs_obj = BeautifulSoup(result.content, "html.parser")
        return bs_obj
    else:
        print(result.status_code)

# daum - ajax
@bp.route('/daum', methods=['POST'])
def daum():
    data = request.get_json()
    code1 = data['code1']
    code2 = data['code2']
    code3 = data['code3']

    company_codes = []
    company_codes.append(code1)
    company_codes.append(code2)
    company_codes.append(code3)

    prices = []
    for item in company_codes:
        now_price = get_daum(item)
        prices.append(now_price)

    sise = {
        'code1': prices[0], 'code2': prices[1], 'code3': prices[2]
    }

    return jsonify(result2= "ok", result3= sise, now= datetime.today())

def get_daum(company_code):
    headers = {
        'Referer': 'http://finance.daum.net',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36 OPR/58.0.3135.127'
    }

    url = 'https://finance.daum.net/api/quotes/A%s?summary=false&changeStatistics=true' %(company_code)

    response = requests.get(url, headers=headers)
    jsonObj = response.json()
    #print(jsonObj)
    #print(jsonObj['name'] + '(' + jsonObj['symbolCode'] + ')')

    now_price = jsonObj['tradePrice']
    return now_price

# itooza - bs4
@bp.route('/itooza_stock', methods=['POST'])
def itooza_stock():
    data = request.get_json()
    code1 = data['code1']
    code2 = data['code2']
    code3 = data['code3']

    company_codes = []
    company_codes.append(code1)
    company_codes.append(code2)
    company_codes.append(code3)

    prices = []
    for item in company_codes:
        now_price = get_itooza(item)
        prices.append(now_price)

    sise = {
        'code1': prices[0], 'code2': prices[1], 'code3': prices[2]
    }

    return jsonify(result2= "ok", result3= sise, now= datetime.today())

def get_itooza(company_code):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    url = 'https://search.itooza.com/search.htm?seName=' + company_code

    result = requests.get(url, headers=headers)
    bs_obj = BeautifulSoup(result.content, "html.parser")
    find_1 = bs_obj.find("h2", {"class": "increase"})
    find_2 = find_1.find("span")

    now_price = find_2.text
    return now_price



