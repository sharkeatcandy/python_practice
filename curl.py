import json
import requests
import datetime
import os
import sys
def monitor():
	txt = open('./curl.txt', 'w', encoding = 'UTF-8')
	url = 'https://www.dcard.tw/_api/posts/231398731/comments?after=0&limit=100'
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
	dcard = requests.get(url, headers=headers)
	if dcard.status_code == requests.codes.ok:
		dcard_contents = json.loads(dcard.content)
		txt.write(str(dcard_contents))

if __name__ == "__main__":
	monitor()