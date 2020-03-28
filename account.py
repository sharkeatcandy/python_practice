# -*- coding: UTF-8 -*-
import sys
import os
import json
initialization = open('./account.json', 'a', encoding='utf8')
def create():
    user_name = input('User Name: ')

    if os.stat("./account.json").st_size == 0:
        old_data = []
    else:
        search_status = True
        while search_status:
            search_status = False
            account_json_read = open('./account.json', 'r', encoding='utf8')
            old_data = json.loads(account_json_read.read())
            for entry in old_data:
                if user_name == entry ['ID']:
                    print('ID is used')
                    search_status = True
                    user_name = input('Please enter the other User ID or exit: ')
                    if(user_name=="exit"):
                        sys.exit()

    password = input('Password: ')
    data = {
        'ID':user_name,
        'PW':password
    }
    old_data.append(data)
    account_json = open('./account.json', 'w', encoding='utf8')
    json.dump(old_data, account_json)

def search():
    search_status = False
    account_json_read = open('./account.json', 'r', encoding='utf8')
    user_name = input('User ID: ')
    old_data = json.loads(account_json_read.read())
    while not search_status:
        for entry in old_data:
            if user_name == entry['ID']:
                print('Password: '+entry['PW'])
                search_status = True
                return 0
        user_name = input('Not found user id match %s ,please enter the other User ID or exit: '%user_name)
        if(user_name=="exit"):
            sys.exit()

if __name__ == "__main__":
    work = input('create or search or exit: ')
    while work:
        if(work=="create"):
            create()
            work = input('create or search or exit: ')
        elif(work=="search"):
            search()
            work = input('create or search or exit: ')
        elif(work=="exit"):
            sys.exit()
        else:
            print('Please enter the correct keyword')
            work = input('create or search or exit: ')
    while not work:
        print('No input, exit the program')
        sys.exit()