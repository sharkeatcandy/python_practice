# -*- coding: utf-8 -*-
import json
import requests
import datetime
import os
import sys
def search():
	number=1000
	school='健行科技大學'
	print('Search by school: ' + school + ' in the last ' + str(number) + ' post')
	find_status = False
	end_id = ''
	txt = open('./search.txt', 'w+', encoding = 'UTF-8')
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
	count = 0
	for n in range(0,number,100):
		if n:
			url = 'https://www.dcard.tw/_api/posts?limit=100&before=%s&popular=false'%(end_id)
		else:
			url = 'https://www.dcard.tw/_api/posts?limit=100&popular=false'
		dcard = requests.get(url, headers=headers)
		if dcard.status_code == requests.codes.ok:
			dcard_contents = json.loads(dcard.content)
			for i in range(100):
				end_id = str(dcard_contents[i]['id'])
				try:
					if(dcard_contents[i]['school']=="%s"%(school)):
						count += 1
						find_status = True
						txt.write('校名：')
						txt.write(dcard_contents[i]['school'])
						txt.write('\n')
						txt.write('文章ID：')
						txt.write(str(dcard_contents[i]['id']))
						txt.write('\n')
						txt.write('標題：')
						txt.write(dcard_contents[i]['title'])
						txt.write('\n')
						txt.write('內文：')
						txt.write(dcard_contents[i]['excerpt'])
						txt.write('\n')
						txt.write('\n')
					else:
						pass
				except:
					pass

		else:
			txt.write(url)
			txt.write('Get API failed at '+str(datetime.datetime.now()))
			txt.write('\n')
	if not find_status:
		txt.write('Not found any post at '+str(datetime.datetime.now()))
		txt.write('\n')
	txt.close()
	print("找到%d篇%s發的文章，詳細內容請看search.txt"%(count, school))

if __name__ == "__main__":
	search()