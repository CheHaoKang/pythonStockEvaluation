# -*- coding: UTF-8 -*-

import requests
import pymysql.cursors
import json
import csv
import sys
import datetime
from fake_useragent import UserAgent
import time

def getStockCodes():
    sql = "SELECT stockCode FROM stocktable"

    try:
        # Execute the SQL command
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='89787198', db='stockevaluation', charset="utf8")
        cursor = conn.cursor()
        cursor.execute(sql)
        # Fetch all the rows in a list of lists.
        stockCodes = []
        results = cursor.fetchall()
        for row in results:
            stockCodes.append(row[0])
    except:
        print("Error: unable to fecth data")

    cursor.close()
    conn.close()

    return stockCodes

def getProxy():
    while True:
        try:
            conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='89787198', db='stockevaluation',
                                   charset="utf8")
            cur = conn.cursor()
            sql = """SELECT proxyIPPort FROM (
                SELECT proxyIPPort, proxyAvgReponseperiod, proxyFailtimes*proxyAvgReponseperiod AS formula FROM stockproxies) AS proxyFormula 
                WHERE proxyAvgReponseperiod<5 ORDER BY formula ASC LIMIT 1"""
            cur.execute(sql)
            proxy = cur.fetchone()

            cur.close()
            conn.commit()
            conn.close()

            return proxy[0]
        except:
            print("Unexpected error:", sys.exc_info())
            cur.close()
            conn.close()

def updateProxyInfo(proxy, succeedOrFail, executionTime):
    while True:
        try:
            conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='89787198', db='stockevaluation', charset="utf8")
            cur = conn.cursor()
            sql = """UPDATE stockproxies
                SET proxyAvgReponseperiod=(proxyAvgReponseperiod*proxyUsedTimes+%s)/(proxyUsedTimes+1),
	                proxyUsedTimes=proxyUsedTimes+1,
	                proxyFailtimes=proxyFailtimes+%s
                WHERE proxyIPPort=%s"""
            cur.execute(sql, (executionTime if succeedOrFail else (executionTime+10), 0 if succeedOrFail else 1, proxy)) # 10 is for penalty when failing

            cur.close()
            conn.commit()
            conn.close()

            return
        except:
            print("Unexpected error:", sys.exc_info())
            cur.close()
            conn.close()


if __name__ == "__main__":
    stockCodes = getStockCodes()
    stockCodes = stockCodes[stockCodes.index("1310") + 1:]

    nowProxy = getProxy()
    proxies = {"http": "http://" + nowProxy}
    now = datetime.datetime.now()
    for stock in stockCodes:
        finish = False
        for year in range(now.year, 1998, -1):
            if finish:
                break

            fromMonth = 12
            if year==now.year:
                fromMonth = now.month

            for month in range(fromMonth, 0, -1):
                if finish:
                    break

                date = str(year) + str(month).zfill(2) + '01'

                url_twse = 'http://www.twse.com.tw/exchangeReport/STOCK_DAY_AVG?response=json&date=' + date + '&stockNo=' + stock
                # url_twse = 'http://www.twse.com.tw/exchangeReport/STOCK_DAY_AVG?response=json&date=20180101&stockNo=' + stock
                print(url_twse)

                succeed = False
                while not succeed:
                    ua = UserAgent()
                    header = {'User-Agent': str(ua.random)}

                    fetchSucceed = False
                    while not fetchSucceed:
                        try:
                            start = time.time()
                            res = requests.get(url_twse, headers=header, proxies=proxies)
                            end = time.time()
                            updateProxyInfo(nowProxy, True, end-start)

                            if (end-start)>=5:
                                nowProxy = getProxy()
                                proxies = {"http": "http://" + nowProxy}

                            print(res.text)
                            s = json.loads(res.text)
                            fetchSucceed = True
                        except:
                            print("Unexpected error:", sys.exc_info())
                            updateProxyInfo(nowProxy, False, 0)
                            nowProxy = getProxy()
                            proxies = {"http": "http://" + nowProxy}

                    stockDataArray = []
                    if 'data' in s:
                        for data in (s['data']):
                            if '月' not in data[0]:
                                splitDate = data[0].split('/')
                                splitDate[0] = str(int(splitDate[0]) + 1911)
                                splitDate = '-'.join(splitDate)

                                if not (data[1].isdigit() or data[1].replace('.', '', 1).isdigit()):
                                    continue

                                stockDataArray.append((stock, splitDate, data[1]))

                        print(stockDataArray)
                        succeed = True

                        try:
                            conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='89787198', db='stockevaluation', charset="utf8")
                            cur = conn.cursor()
                            insert = "INSERT INTO stockdata (stockCode, stockDate, stockIndex) VALUES (%s, %s, %s)"
                            cur.executemany(insert, stockDataArray)
                            cur.close()
                            conn.commit()
                            conn.close()
                        except:
                            print("Unexpected error:", sys.exc_info())
                            cur.close()
                            conn.close()

                    if '很抱歉' in s['stat']:
                        succeed = True
                        finish = True
                    elif not succeed:
                        print("Fail: " + url_twse + " . Trying...")

                    time.sleep(1)