# -*- coding: UTF-8 -*-
import sys
import os
import csv
# initialization = open('./account.json', 'a')
def parse_csv():
    for i in range(0, 240, 8):
        is_first_line = True
        with open('./DJ_day_market_cap.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile)
            for row in spamreader:
                if not is_first_line:
                    date = row[0+i]
                    px_open = row[1+i]
                    px_high = row[2+i]
                    px_low = row[3+i]
                    px_last = row[4+i]
                    px_volume = row[5+i]
                    cur_mkt_cap = row[6+i]
                    with open('./DJ_data/%s.csv'%stock_name, 'a', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow([date, px_open, px_high, px_low, px_last, px_volume, cur_mkt_cap])
                else:
                    stock_name = row[0+i]
                    is_first_line = False
                    isExists=os.path.exists("./DJ_data")
                    if not isExists:
                        os.makedirs("./DJ_data")
                    with open('./DJ_data/%s.csv'%stock_name, 'w', newline='') as csvfile:
                        initialization = csv.writer(csvfile)

if __name__ == "__main__":
    parse_csv()