# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod
import requests
import pymysql.cursors
import json
import csv
import sys
import datetime
from fake_useragent import UserAgent
import time
import threading
from time import sleep,ctime

class stockClass(object):
    """This class is for retrieving stock-related data

    Attributes:
        timeout: webpage-fetching timeout
        threadAmount: thread number
    """

    __metaclass__ = ABCMeta

	# globalTimeout = 5
	# globalThreadAmount = 5

    def __init__(self, timeout, threadAmount):
        self.timeout = timeout
        self.threadAmount = threadAmount

    def getStockCodes(self):
        sql = "SELECT stockCode FROM stocktable WHERE stockFinished='no'"
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
            print(">>>>>Not Finished>>>>>")
            print(stockCodes)
            print("<<<<<Not Finished<<<<<")

            cursor.execute("UPDATE stocktable SET stockFinished='no'")

            cursor.execute(sql)
            # Fetch all the rows in a list of lists.
            stockCodes = []
            results = cursor.fetchall()
            for row in results:
                stockCodes.append(row[0])
        except:
            print("Error: unable to fecth data")

        cursor.close()
        conn.commit()
        conn.close()

        return stockCodes

    def getProxy(self, offset):
        # global globalTimeout

        while True:
            try:
                conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='89787198', db='stockevaluation', charset="utf8")
                cur = conn.cursor()
                sql = """SELECT proxyIPPort FROM (
                    SELECT sid, proxyIPPort, proxyAvgReponseperiod, proxyFailtimes*proxyAvgReponseperiod AS formula FROM stockproxies) AS proxyFormula
                    WHERE proxyAvgReponseperiod<%s ORDER BY formula ASC, sid ASC LIMIT 1 OFFSET %s"""
                # sql = """SELECT proxyIPPort FROM (
                #     SELECT sid, proxyIPPort, proxyAvgReponseperiod, proxyFailtimes*proxyAvgReponseperiod AS formula FROM stockproxies) AS proxyFormula
                #     ORDER BY formula ASC, sid ASC LIMIT 1"""
                cur.execute(sql, (self.timeout, offset))
                proxy = cur.fetchone()

                cur.close()
                conn.commit()
                conn.close()

                return proxy[0]
            except:
                print("Unexpected error:", sys.exc_info())
                cur.close()
                conn.close()

    def updateProxyInfo(self, proxy, succeedOrFail, executionTime):
        while True:
            try:
                conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='89787198', db='stockevaluation', charset="utf8")
                cur = conn.cursor()
                sql = """UPDATE stockproxies
                    SET proxyAvgReponseperiod=(proxyAvgReponseperiod*proxyUsedTimes+%s)/(proxyUsedTimes+1),
    	                proxyUsedTimes=proxyUsedTimes+1,
    	                proxyFailtimes=proxyFailtimes+%s
                    WHERE proxyIPPort=%s"""
                cur.execute(sql, (executionTime if succeedOrFail else (executionTime + 10), 0 if succeedOrFail else 1, proxy))  # 10 is for penalty when failing

                cur.close()
                conn.commit()
                conn.close()

                return
            except:
                print("Unexpected error:", sys.exc_info())
                cur.close()
                conn.close()

    def updateStockFinished(self, stock, status):
        while True:
            try:
                conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='89787198', db='stockevaluation', charset="utf8")
                cur = conn.cursor()
                sql = """UPDATE stocktable SET stockFinished=%s WHERE stockcode=%s"""
                cur.execute(sql, (status, stock))

                cur.close()
                conn.commit()
                conn.close()

                return
            except:
                print("Unexpected error:", sys.exc_info())
                cur.close()
                conn.close()

    def retrieveStockData(self, stockCodes, fromCode, endCode, offset, fetchDate):
        # global globalTimeout

        print('>>>>>', fromCode, ctime(), '<<<<<')

        nowProxy = self.getProxy(offset)
        proxies = {"http": "http://" + nowProxy}
        now = datetime.datetime.now()

        if fetchDate != "":
            fromYear = int(fetchDate[0:4])
            endYear = int(fetchDate[0:4]) - 1
            fromMonth = int(fetchDate[4:6])
            endMonth = int(fetchDate[4:6]) - 1
        else:
            fromYear = now.year
            endYear = 1998
            fromMonth = now.month
            endMonth = 0

        for i in range(fromCode, endCode):
            # for stock in stockCodes:
            stock = stockCodes[i]
            self.updateStockFinished(stock, 'ing')
            finish = False
            # for year in range(now.year, 1998, -1):
            for year in range(fromYear, endYear, -1):
                if finish:
                    break

                if fetchDate == "":
                    fromMonth = 12
                    if year == now.year:
                        fromMonth = now.month

                for month in range(fromMonth, endMonth, -1):
                    if finish:
                        break

                    date = str(year) + str(month).zfill(2) + '01'

                    url_twse = 'http://www.twse.com.tw/exchangeReport/STOCK_DAY_AVG?response=json&date=' + date + '&stockNo=' + stock
                    print(url_twse)

                    succeed = False
                    while not succeed:
                        ua = UserAgent()
                        header = {'User-Agent': str(ua.random)}

                        fetchSucceed = False
                        while not fetchSucceed:
                            try:
                                start = time.time()
                                res = requests.get(url_twse, headers=header, proxies=proxies, timeout=self.timeout)
                                end = time.time()

                                if (end - start) >= self.timeout:
                                    nowProxy = self.getProxy(offset)
                                    proxies = {"http": "http://" + nowProxy}

                                print(res.text)
                                s = json.loads(res.text)
                                fetchSucceed = True

                                if 'data' in s or ('stat' in s and '很抱歉' in s['stat']):
                                    self.updateProxyInfo(nowProxy, True, end - start)
                                else:
                                    self.updateProxyInfo(nowProxy, False, 0)
                                    nowProxy = self.getProxy(offset)
                                    proxies = {"http": "http://" + nowProxy}
                            except:
                                print("Unexpected error:", sys.exc_info())
                                self.updateProxyInfo(nowProxy, False, 0)
                                nowProxy = self.getProxy(offset)
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

                                    if fetchDate != "" and splitDate.replace('-', '') == fetchDate:
                                        stockDataArray.append((stock, splitDate, data[1]))
                                    elif fetchDate == "":
                                        stockDataArray.append((stock, splitDate, data[1]))

                            print(stockDataArray)
                            succeed = True

                            if stockDataArray:  # not empty
                                try:
                                    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='89787198', db='stockevaluation', charset="utf8")
                                    cur = conn.cursor()
                                    insert = "INSERT IGNORE INTO stockdata (stockCode, stockDate, stockIndex) VALUES (%s, %s, %s)"
                                    cur.executemany(insert, stockDataArray)
                                    cur.close()
                                    conn.commit()
                                    conn.close()
                                except:
                                    print("Unexpected error:", sys.exc_info())
                                    cur.close()
                                    conn.close()

                        if 'stat' in s and '很抱歉' in s['stat']:
                            succeed = True
                            finish = True
                            # updateStockFinished(stock, 'yes')
                        elif not succeed:
                            print("Fail: " + url_twse + " . Trying...")

                        time.sleep(1)

            self.updateStockFinished(stock, 'yes')

    def computeStockKD(self, stockCodes, fromCode, endCode, offset, fetchDate):
        print('#####', fromCode, ctime(), '#####')

        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='89787198', db='stockevaluation', charset="utf8")
        cursor = conn.cursor()

        for i in range(fromCode, endCode):
            # for stock in stockCodes:
            stock = stockCodes[i]
            stockData = []

            fetchSucceed = False
            while not fetchSucceed:
                if fetchDate == "":
                    sql = "SELECT * FROM stockdata WHERE stockcode=%s ORDER BY stockDate ASC"
                else:
                    sql = "SELECT * FROM stockdata WHERE stockcode=%s ORDER BY stockDate DESC LIMIT 9"

                try:
                    cursor.execute(sql, (stock))
                    # Fetch all the rows in a list of lists.
                    results = cursor.fetchall()
                    for row in results:
                        stockData.append([str(row[2]), row[3], row[4], row[5]])
                    fetchSucceed = True
                except:
                    print("Error: unable to fecth data")

            if len(stockData) < 9:
                continue

            if fetchDate != "":
                stockData = stockData[::-1]
                end = 9
            else:
                end = len(stockData)

            print(stockData)

            stockKDList = []
            for j in range(8, end):
                if 'curK' in locals():
                    preK = curK
                    preD = curD
                elif stockData[j - 1][2] == 0.0:
                    preK = 50.0
                    preD = 50.0
                else:
                    preK = stockData[j - 1][2]
                    preD = stockData[j - 1][3]

                slice = stockData[j - 8:j + 1]
                print(stock, slice)
                print(stockData[j])
                print(max(slice, key=lambda x: x[1]))
                print(min(slice, key=lambda x: x[1]))
                if (float((max(slice, key=lambda x: x[1]))[1]) - float(min(slice, key=lambda x: x[1])[1])) != 0:
                    rsv = (float(stockData[j][1]) - float(min(slice, key=lambda x: x[1])[1])) / (
                    float((max(slice, key=lambda x: x[1]))[1]) - float(min(slice, key=lambda x: x[1])[1])) * 100.0
                else:
                    rsv = 50.0
                curK = 2.0 / 3.0 * preK + 1.0 / 3.0 * rsv
                curD = 2.0 / 3.0 * preD + 1.0 / 3.0 * curK
                print(rsv, preK, preD)
                print((curK, curD, stock, stockData[j][0]))
                stockKDList.append((curK, curD, stock, stockData[j][0]))

            try:
                sql = "UPDATE stockdata SET stockK=%s, stockD=%s WHERE stockCode=%s AND stockDate=%s"
                cursor.executemany(sql, stockKDList)
                conn.commit()
            except:
                print("Unexpected error:", sys.exc_info())

        cursor.close()
        conn.close()

    @abstractmethod
    def vehicle_type(self):
        """"Return a string representing the type of vehicle this is."""
        pass