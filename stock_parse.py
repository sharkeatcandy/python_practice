# -*- coding: utf-8 -*-
import json
import requests

price_stores = []
date_store = []

def holiday_mapping(day, month, year=2019):
    holiday = [
        "20190404",
        "20190405",
        "20190406",
        "20190407",
    ]
    if "%d%02d%02d"%(year, month, day) in holiday:
        return 3, 4, 2019
    else:
        return day, month, year

def month_mapping(month_string):
    month = {
        "JAN": 1,
        "FEB": 2,
        "MAR": 3,
        "APR": 4,
        "MAY": 5,
        "JUN": 6,
        "JUL": 7,
        "AUG": 8,
        "SEP": 9,
        "OCT":10,
        "NOV":11,
        "DEC":12
    }
    return month.get(month_string.upper())

def get_stock_price(day, month, year=2019, sid=2330):
    if "%d/%02d"%(year-1911, month) not in str(price_stores):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
        url = 'http://www.twse.com.tw/exchangeReport/STOCK_DAY'
        params = {'date': '%d%02d01' % (year, month), 'stockNo': sid}
        response = requests.get(url, params=params, headers=headers)
        response_contents = json.loads(response.content)
        price_stores.append(response_contents['data'])
        date_store.append(response_contents['date'])

    date_index = date_store.index("%d%02d01"%(year, month))
    for price_store in price_stores[date_index]:
        if "%d/%02d/%02d"%(year-1911, month, day) in price_store:
            # print(price_store[0])
            today_price = float(price_store[-3])
            price_index = price_stores[date_index].index(price_store)
            if price_index > 0:
                # print(price_stores[date_index][price_index-1][0])
                yesterday_price = float(price_stores[date_index][price_index-1][-3])
            elif price_index == 0:
                if "%d/%02d"%(year-1911, month-1) not in str(price_stores):
                    params = {'date': '%d%02d01' % (year, month-1), 'stockNo': sid}
                    response = requests.get(url, params=params, headers=headers)
                    response_contents = json.loads(response.content)
                    price_stores.append(response_contents['data'])
                    date_store.append(response_contents['date'])
                date_index = date_store.index("%d%02d01"%(year, month-1))
                # print(price_stores[date_index][-1][0])
                yesterday_price = float(price_stores[date_index][-1][-3])

    return today_price, yesterday_price

def tsmc():
    global price_stores
    global date_store
    price_stores = []
    date_store = []
    with open('./Stock.json') as json_file:  
        data = json.load(json_file)
        articles = data['articles']
        previous_search_day = 0
        count_push = 0
        count_booo = 0
        first_day = True
        for article in articles:
            if '台積電' in article['content']:
                date = article['date'].split()
                if len(date) > 0:
                    if first_day:
                        previous_search_day = int(date[2])
                        first_day = False
                        previous_day = date[0]
                        search_month = month_mapping(date[1])
                        search_year = int(date[4])
                    search_day = int(date[2])

                    if search_day == previous_search_day:
                        messages = article['messages']
                        for message in messages:
                            if message['push_tag']=='推':
                                count_push+=1
                            elif message['push_tag']=='噓':
                                count_booo+=1
                    else:
                        print("日期：%d%02d%02d"%(search_year, search_month, previous_search_day))
                        if previous_day == 'Sat':
                            previous_search_day = previous_search_day-1
                        elif previous_day == 'Sun':
                            previous_search_day = previous_search_day-2
                        previous_search_day, search_month, search_year = holiday_mapping(previous_search_day, search_month, search_year)

                        today_price, yesterday_price = get_stock_price(day = previous_search_day, month = search_month, year = search_year, sid = 2330)

                        print("台積電最近收盤價：%7.2f"%today_price)
                        print("台積電今日推文數：%7d"%count_push)
                        print("台積電今日噓文數：%7d"%count_booo)

                        previous_search_day = search_day
                        previous_day = date[0]

                        count_push = 0
                        count_booo = 0
                        messages = article['messages']
                        for message in messages:
                            if message['push_tag']=='推':
                                count_push+=1
                            elif message['push_tag']=='噓':
                                count_booo+=1

                    search_month = month_mapping(date[1])
                    search_year = int(date[4])

        if search_day == previous_search_day:
            print("日期：%d%02d%02d"%(search_year, search_month, previous_search_day))
            if previous_day == 'Sat':
                previous_search_day = previous_search_day-1
            elif previous_day == 'Sun':
                previous_search_day = previous_search_day-2
                previous_search_day, search_month, search_year = holiday_mapping(previous_search_day, search_month, search_year)
            today_price, yesterday_price = get_stock_price(day = previous_search_day, month = search_month, year = search_year, sid = 2330)
            print("台積電最近收盤價：%7.2f"%today_price)
            print("台積電今日推文數：%7d"%count_push)
            print("台積電今日噓文數：%7d"%count_booo)
        else:
            print("日期：%d%02d%02d"%(search_year, search_month, search_day))
            if previous_day == 'Sat':
                previous_search_day = previous_search_day-1
            elif previous_day == 'Sun':
                previous_search_day = previous_search_day-2
                previous_search_day, search_month, search_year = holiday_mapping(previous_search_day, search_month, search_year)
            today_price, yesterday_price = get_stock_price(day = search_day, month = search_month, year = search_year, sid = 2330)
            print("台積電最近收盤價：%7.2f"%today_price)
            print("台積電今日推文數：%7d"%count_push)
            print("台積電今日噓文數：%7d"%count_booo)

def ssfc():
    global price_stores
    global date_store
    price_stores = []
    date_store = []
    with open('./Stock.json') as json_file:  
        data = json.load(json_file)
        articles = data['articles']
        previous_search_day = 0
        increase_count = 0
        decrease_count = 0
        increase_count_duplicate = 0
        decrease_count_duplicate = 0
        disappear_count = 0
        for article in articles:
            if '台積電' in article['content']:
                if '三星' in article['content']:
                    disappear_count +=1
                    date = article['date'].split()
                    if len(date) > 0:
                        search_day = int(date[2])
                        search_month = month_mapping(date[1])
                        search_year = int(date[4])

                        if search_day == previous_search_day:
                            if date[0] == 'Sat':
                                search_day = int(date[2])-1
                            elif date[0] == 'Sun':
                                search_day = int(date[2])-2
                            search_day, search_month, search_year = holiday_mapping(search_day, search_month, search_year)

                            today_price, yesterday_price = get_stock_price(day = search_day, month = search_month, year = search_year, sid = 5007)
                            if today_price > yesterday_price:
                                increase_count_duplicate +=1
                            elif yesterday_price > today_price:
                                decrease_count_duplicate +=1
                        else:
                            previous_search_day = search_day
                            
                            if date[0] == 'Sat':
                                search_day = int(date[2])-1
                            elif date[0] == 'Sun':
                                search_day = int(date[2])-2
                            search_day, search_month, search_year = holiday_mapping(search_day, search_month, search_year)

                            today_price, yesterday_price = get_stock_price(day = search_day, month = search_month, year = search_year, sid = 5007)

                            if today_price > yesterday_price:
                                increase_count +=1
                            elif yesterday_price > today_price:
                                decrease_count +=1
        print("三星和台積電共同出現在內文中共%d篇"%disappear_count)
        print("出現後和昨日對比漲%3d次"%increase_count)
        print("出現後和昨日對比跌%3d次"%decrease_count)
        print("若不過濾同日多篇同時出現的文章")
        print("出現後和昨日對比漲%3d次"%(increase_count+increase_count_duplicate))
        print("出現後和昨日對比跌%3d次"%(decrease_count+decrease_count_duplicate))
                    
if __name__ == "__main__":
        tsmc()
        print("===========================================================")
        ssfc()