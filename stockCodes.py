# -*- coding: UTF-8 -*-

import requests
import re
import pymysql
import pymysql.cursors

if __name__ == "__main__":
    url = "http://pchome.megatime.com.tw/js/stock_list.js"
    r = requests.get(url)
    r.encoding = 'utf8'
    # print(r.text)

    pattern = re.compile(r'\(\s*\'(.*?)\'\s*,\s*\'(.*?)\'\s*,\s*\'(.*?)\'\s*,\s*\'(.*?)\'\s*\)')
    # match = pattern.match("['0050', '元大台灣50', '元大台灣50', ',0_00,']")

    stocksArray = []
    stocks = re.findall(r'\[\'(.*?)\'\s*,\s*\'(.*?)\'\s*,\s*\'(.*?)\'\s*,\s*\'(.*?)\'\s*\]', r.text)
    for stock in stocks:
        match = pattern.match(str(stock))
        stocksArray.append((match.group(1),match.group(2),match.group(3),match.group(4)))
        # print(match.group(1))
        # print(match.group(2))
        # print(match.group(3))
        # print(match.group(4))

    print(stocksArray)

    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='89787198', db='stockevaluation', charset="utf8")
    # conn.set_charset('utf8')

    cur = conn.cursor()
    # cur.execute("SELECT * FROM 膠片")
    insert = "INSERT INTO stocktable (stockCode, stockName, stockFullname, stockNote) VALUES (%s, %s, %s, %s)"
    cur.executemany(insert, stocksArray)
    cur.close()
    conn.commit()
    conn.close()

    # print(cur.description)
    # print()
    #
    # for row in cur:
    #     print(row)
    #
    # cur.close()
    # conn.commit()
    # conn.close()