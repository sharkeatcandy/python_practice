# -*- coding: utf-8 -*-
import json
import requests
import datetime
import os
import sys
import time
token = "LBcZJqQ4k5nofIiS7JXYrQuYp5PzyxHqLhWuOzuVVty"

# line API document: https://notify-bot.line.me/doc/en/
def lineNotify(token, msg):

    url = "https://notify-api.line.me/api/notify"
    headers = {
        "Authorization": "Bearer " + token, 
        "Content-Type" : "application/x-www-form-urlencoded"
    }
    
    payload = {'message': msg}
    r = requests.post(url, headers = headers, params = payload)
    return r.status_code

def monitor():
	find_status = False
	pic_status = False
	txt = open('./test.txt', 'a', encoding = 'UTF-8')
	url = 'https://www.dcard.tw/_api/forums/whysoserious/posts?limit=100&popular=false'
	image_url = "附圖："
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
	dcard = requests.get(url, headers=headers)
	# os.system("echo 'd *' | mail")
	if dcard.status_code == requests.codes.ok:
		dcard_contents = json.loads(dcard.content)
		for i in range(100):
			try:
				if(dcard_contents[i]['school']==u'銘傳大學' and dcard_contents[i]['department']==u'資訊工程學系'):
					find_status = True
					txt_read = open('./test.txt', 'r', encoding = 'UTF-8')
					if "文章ID：%s"%(str(dcard_contents[i]['id'])) not in txt_read.read():
						txt.write('\n')
						txt.write('校名：')
						txt.write(dcard_contents[i]['school'])
						txt.write('\n')
						txt.write('系名：')
						txt.write(dcard_contents[i]['department'])
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
						if dcard_contents[i]['mediaMeta'] != []:
							pic_status = True
							txt.write('附圖：')
							txt.write('\n')
							for item in dcard_contents[i]['mediaMeta']:
								if str(item['url']).split('com/')[1].split('.')[0] not in image_url:
									image_url += "\n%s"%(str(item['url']))
									txt.write(item['url'])
									txt.write('\n')
						txt.write('現在時間：')
						txt.write(str(datetime.datetime.now()))
						txt.write('\n')
						txt.write('\n')
						if pic_status:
							msg = "\n校名："+dcard_contents[i]['school']+"\n系名："+dcard_contents[i]['department']+"\n文章網址："+"http://dcard.tw/f/whysoserious/p/"+str(dcard_contents[i]['id'])+"\n標題："+dcard_contents[i]['title']+"\n內文："+dcard_contents[i]['excerpt']+"\n"+image_url
						else:
							msg = "\n校名："+dcard_contents[i]['school']+"\n系名："+dcard_contents[i]['department']+"\n文章網址："+"http://dcard.tw/f/whysoserious/p/"+str(dcard_contents[i]['id'])+"\n標題："+dcard_contents[i]['title']+"\n內文："+dcard_contents[i]['excerpt']
						lineNotify(token, msg)
					else:
						txt.write('No new post '+str(datetime.datetime.now()))
						txt.write('\n')
				else:
					pass
			except:
				pass
	else:
		txt.write('Get API failed at '+str(datetime.datetime.now()))
		txt.write('\n')

	if not find_status:
		txt.write('No post at '+str(datetime.datetime.now()))
		txt.write('\n')

	txt.close()

def search(number=100, from_id='', school='銘傳大學', department='資訊工程學系'):
	print('Search by school: ' + school + ' department: '+ department + ' in the last ' + str(number) + ' post' + ', from:' + from_id)
	find_status = False
	api_status = True
	end_id = from_id
	txt = open('./test.txt', 'w+', encoding = 'UTF-8')
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
	n = 0
	while n < number:
		if end_id:
			url = 'https://www.dcard.tw/_api/forums/whysoserious/posts?limit=100&before=%s&popular=false'%(end_id)
		else:
			url = 'https://www.dcard.tw/_api/forums/whysoserious/posts?limit=100&popular=false'
		dcard = requests.get(url, headers=headers)
		if dcard.status_code == requests.codes.ok:
			api_status = True
			n += 100
			dcard_contents = json.loads(dcard.content)
			for i in range(100):
				end_id = str(dcard_contents[i]['id'])
				try:
					if(dcard_contents[i]['school']=="%s"%(school) and dcard_contents[i]['department']=="%s"%(department)):
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
					else:
						pass
				except:
					pass

		else:
			txt.write(url)
			txt.write(' ')
			txt.write('Get API failed at '+str(datetime.datetime.now()))
			txt.write('\n')
			if api_status:
				n -= 100
			print('Because %d retrying'%dcard.status_code)
			time.sleep(10)
	if not find_status:
		print('Not found any post at '+str(datetime.datetime.now()))
	txt.close()

if __name__ == "__main__":
	if(len(sys.argv)==1):
		monitor()
	elif(sys.argv[1]=="search"):
		if len(sys.argv)==3:
			search(number=int(sys.argv[2]))
		elif len(sys.argv)==5:
			search(number=int(sys.argv[2]), school=sys.argv[3], department=sys.argv[4])
		elif len(sys.argv)==6:
			search(number=int(sys.argv[2]), from_id=sys.argv[3], school=sys.argv[4], department=sys.argv[5])
		else:
			search(number=100)
	elif(sys.argv[1]=="help"):
		print('Usage: python dcard.py search $number $from(optional) $school $department')