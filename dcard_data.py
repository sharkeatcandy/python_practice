# -*- coding: utf-8 -*-
import json
import requests
import datetime
import time


def search(number=100, from_id='', school='', department=''):
    print(f'Search by school: {school} department: {department} in the last {number} post ,from:  {from_id}')
    find_status = False
    api_status = False
    end_id = from_id
    txt = open('./search.txt', 'w+', encoding='UTF-8')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    n = 0
    count = 0
    retry = 0
    while n < number:
        if end_id:
            url = 'https://www.dcard.tw/service/api/v2/forums/whysoserious/posts?limit=100&before=%s&popular=false' % (
                end_id)
        else:
            url = 'https://www.dcard.tw/service/api/v2/forums/whysoserious/posts?limit=100&popular=false'
        dcard = requests.get(url, headers=headers)
        if dcard.status_code == requests.codes.ok:
            retry = 0
            api_status = True
            n += 100
            dcard_contents = json.loads(dcard.content)
            for i in range(100):
                end_id = str(dcard_contents[i]['id'])
                try:
                    if department:
                        if(dcard_contents[i]['school'] == "%s" % (school) and dcard_contents[i]['department'] == "%s" % (department)):
                            find_status = True
                            txt.write('校名：')
                            txt.write(dcard_contents[i]['school'])
                            txt.write('\n')
                            txt.write('系名：')
                            txt.write(dcard_contents[i]['department'])
                            txt.write('\n')
                            txt.write('文章網址：')
                            txt.write("http://dcard.tw/f/whysoserious/p/"+str(dcard_contents[i]['id']))
                            txt.write('\n')
                            txt.write('標題：')
                            txt.write(dcard_contents[i]['title'])
                            txt.write('\n')
                            txt.write('內文：')
                            txt.write(dcard_contents[i]['excerpt'])
                            txt.write('\n')
                            txt.write('\n')
                            count += 1
                    else:
                        if(dcard_contents[i]['school'] == "%s" % (school)):
                            find_status = True
                            txt.write('校名：')
                            txt.write(dcard_contents[i]['school'])
                            txt.write('\n')
                            txt.write('文章網址：')
                            txt.write("http://dcard.tw/f/whysoserious/p/"+str(dcard_contents[i]['id']))
                            txt.write('\n')
                            txt.write('標題：')
                            txt.write(dcard_contents[i]['title'])
                            txt.write('\n')
                            txt.write('內文：')
                            txt.write(dcard_contents[i]['excerpt'])
                            txt.write('\n')
                            txt.write('\n')
                            count += 1
                except:
                    pass

        else:
            txt.write(url)
            txt.write(' ')
            txt.write(f'Get API failed at {str(datetime.datetime.now())}')
            txt.write('\n')
            if api_status:
                api_status = False
                n -= 100
            retry += 1
            print(f'因為 {dcard.status_code} 正在重試第{retry}次')
            time.sleep(10)
    if not find_status:
        print(f'沒有找到任何PO文 {str(datetime.datetime.now())}')
    txt.close()
    print(f"找到{count}篇{school}{department}發的文章，詳細內容請看search.txt")


if __name__ == "__main__":
    number = input('請輸入要在最近幾篇文章內搜尋：\n')
    from_id = input('請輸入要從第幾篇開始往前搜尋(如果從最近開始搜尋直接按enter就好)：\n')
    school = input('請輸入要搜尋的校名(卡稱也可以)：\n')
    department = input('請輸入要搜尋的系名(如果沒有要搜尋系名或是搜尋卡稱就直接按enter)：\n')
    search(number=int(number), from_id=int(from_id) if from_id else from_id, school=school, department=department)
