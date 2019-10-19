# -*- coding: utf-8 -*-
import json
import requests
def check(number):
    if number.isdigit() and len(number)==4:
        return number
    else:
        print('Please correct stock code')
        exit()
def monitor(stock):
    stock = check(stock)
    url = "http://mis.tse.com.tw/stock/api/getStock.jsp?ch=%s.tw&json=1&+="%(stock)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    response = requests.get(url, headers=headers)
    response_contents = json.loads(response.content)
    try:
        price = response_contents['msgArray'][0]['y']
    except:
        print('Error stock code or api error，please try again')
    return price

if __name__ == "__main__":
    stock=input("股票代碼： ")
    price = monitor(stock)
    print("收盤價：%7s"%price)