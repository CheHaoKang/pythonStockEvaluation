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
import csv
import re

class stockClass(object):
    """This class is for retrieving stock-related data

    Attributes:
        timeout: webpage-fetching timeout
        threadAmount: thread number
    """

    __metaclass__ = ABCMeta

    # Static variables - Attributes of a class hold for all instances in all cases
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

    def getInstitutionalInvestors(self, date):
        # 自營商買賣超彙總表
        # http://www.twse.com.tw/fund/TWT43U?response=json&date=20180112
        # 投信買賣超彙總表
        # http://www.twse.com.tw/fund/TWT44U?response=json&date=&_=1515943335745
        # 外資及陸資買賣超彙總表
        # http://www.twse.com.tw/fund/TWT38U?response=json&date=20180112

        ua = UserAgent()
        insInvestArray = []

        hyphenDate = datetime.datetime.strptime(date, '%Y%m%d').strftime('%Y-%m-%d')

        # 自營商買賣超彙總表
        succeed = False
        while not succeed:
            header = {'User-Agent': str(ua.random)}
            res = requests.get("http://www.twse.com.tw/fund/TWT43U?response=json&date=" + str(date), headers=header)

            try:
                s = json.loads(res.text)
                if 'data' in s:
                    for data in s['data']:
                        insInvestArray.append((hyphenDate, data[0].strip(), 'dealer', 'dealerSelf', data[2].strip().replace(",", "")))
                        insInvestArray.append((hyphenDate, data[0].strip(), 'dealer', 'dealerSelf', ('' if data[3].strip().replace(",", "") == '0' else '-') + data[3].strip().replace(",", "")))
                        insInvestArray.append((hyphenDate, data[0].strip(), 'dealer', 'dealerHedging', data[5].strip().replace(",", "")))
                        insInvestArray.append((hyphenDate, data[0].strip(), 'dealer', 'dealerHedging', ('' if data[6].strip().replace(",", "") == '0' else '-') + data[6].strip().replace(",", "")))
                        insInvestArray.append((hyphenDate, data[0].strip(), 'dealer', 'dealer', data[8].strip().replace(",", "")))
                        insInvestArray.append((hyphenDate, data[0].strip(), 'dealer', 'dealer', ('' if data[9].strip().replace(",", "") == '0' else '-') + data[9].strip().replace(",", "")))
                    succeed = True
                elif 'stat' in s and '很抱歉' in s['stat']:
                    succeed = True
            except:
                print("Unexpected error:", sys.exc_info())

        time.sleep(1)

        # 投信買賣超彙總表
        succeed = False
        while not succeed:
            header = {'User-Agent': str(ua.random)}
            res = requests.get("http://www.twse.com.tw/fund/TWT44U?response=json&date=" + str(date), headers=header)

            try:
                s = json.loads(res.text)
                if 'data' in s:
                    for data in s['data']:
                        insInvestArray.append((hyphenDate, data[1].strip(), 'investmentTrust', 'investmentTrust', data[3].strip().replace(",", "")))
                        insInvestArray.append((hyphenDate, data[1].strip(), 'investmentTrust', 'investmentTrust', ('' if data[4].strip().replace(",", "") == '0' else '-') + data[4].strip().replace(",", "")))
                    succeed = True
                elif 'stat' in s and '很抱歉' in s['stat']:
                    succeed = True
            except:
                print("Unexpected error:", sys.exc_info())

        time.sleep(1)

        # 外資及陸資買賣超彙總表
        succeed = False
        while not succeed:
            header = {'User-Agent': str(ua.random)}
            res = requests.get("http://www.twse.com.tw/fund/TWT38U?response=json&date=" + str(date), headers=header)

            try:
                s = json.loads(res.text)
                if 'data' in s:
                    for data in s['data']:
                        insInvestArray.append((hyphenDate, data[1].strip(), 'foreignInvestor', 'foreignInvestor', data[9].strip().replace(",", "")))
                        insInvestArray.append((hyphenDate, data[1].strip(), 'foreignInvestor', 'foreignInvestor', ('' if data[10].strip().replace(",", "") == '0' else '-') + data[10].strip().replace(",", "")))
                    succeed = True
                elif 'stat' in s and '很抱歉' in s['stat']:
                    succeed = True
            except:
                print("Unexpected error:", sys.exc_info())

        print(insInvestArray)
        if insInvestArray:  # not empty
            while True:
                try:
                    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='89787198', db='stockevaluation', charset="utf8")
                    cur = conn.cursor()
                    insert = "INSERT INTO stockInstitutionalInvestor (stockDate, stockCode, stockInvestorType, stockInvestorTypeDetail, stockAmount) VALUES (%s, %s, %s, %s, %s)"
                    cur.executemany(insert, insInvestArray)
                    cur.close()
                    conn.commit()
                    conn.close()
                    break
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

                        # fetchSucceed = False
                        # while not fetchSucceed:
                        while True:
                            try:
                                start = time.time()
                                res = requests.get(url_twse, headers=header, proxies=proxies, timeout=self.timeout)
                                end = time.time()

                                # if (end - start) >= self.timeout:
                                #     nowProxy = self.getProxy(offset)
                                #     proxies = {"http": "http://" + nowProxy}

                                print(res.text)
                                s = json.loads(res.text)
                                # fetchSucceed = True

                                if 'data' in s:
                                    self.updateProxyInfo(nowProxy, True, end-start)
                                    succeed = True # this is for this round
                                    break
                                elif 'stat' in s and '很抱歉' in s['stat']:
                                    self.updateProxyInfo(nowProxy, True, end-start)
                                    succeed = True  # this is for this round
                                    finish = True  # this is for this stock
                                    break
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
                        if succeed and 'data' in s:
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
                            # succeed = True

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

                        # if 'stat' in s and '很抱歉' in s['stat']:
                        #     succeed = True
                        #     finish = True
                            # updateStockFinished(stock, 'yes')
                        if not succeed:
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

            sqlSucceed = False
            while not sqlSucceed:
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
                    sqlSucceed = True
                except:
                    print("Error: unable to fecth data")

            if len(stockData) < 9:
                continue

            if fetchDate != "":
                stockData = stockData[::-1] # reverse the list since we only need the current date
                end = 9
            else:
                end = len(stockData)

            print(stockData)

            stockKDList = []
            for j in range(8, end):
                if stockData[j][2]!=0 and stockData[j][3]!=0:   # if computed before, skip it
                    break

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
                    rsv = (float(stockData[j][1]) - float(min(slice, key=lambda x: x[1])[1])) / \
                        (float((max(slice, key=lambda x: x[1]))[1]) - float(min(slice, key=lambda x: x[1])[1])) * 100.0
                else:
                    rsv = 50.0
                curK = 2.0 / 3.0 * preK + 1.0 / 3.0 * rsv
                curD = 2.0 / 3.0 * preD + 1.0 / 3.0 * curK
                print(rsv, preK, preD)
                print((curK, curD, stock, stockData[j][0]))
                stockKDList.append((curK, curD, stock, stockData[j][0]))

            while True:
                try:
                    sql = "UPDATE stockdata SET stockK=%s, stockD=%s WHERE stockCode=%s AND stockDate=%s"
                    cursor.executemany(sql, stockKDList)
                    conn.commit()
                    break
                except:
                    print("Unexpected error:", sys.exc_info())

        cursor.close()
        conn.close()

    def getStockNameInfoStartupdate(self):
        sql = """
        SELECT st.stockCode, st.stockName, st.stockInfo, stStartup.stockdate FROM stocktable AS st
        LEFT JOIN (
        SELECT stockcode, stockdate FROM stockdata GROUP BY stockcode ORDER BY stockdate ASC
        ) stStartup ON st.stockCode=stStartup.stockcode
        """
        try:
            # Execute the SQL command
            conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='89787198', db='stockevaluation', charset="utf8")
            cursor = conn.cursor()
            cursor.execute(sql)
            # Fetch all the rows in a list of lists.
            stockCodeNames = {}
            results = cursor.fetchall()
            for row in results:
                stockCodeNames[row[0]] = [row[1],row[2], str(row[3])]
        except:
            print("Error: unable to fecth data")

        cursor.close()
        conn.commit()
        conn.close()

        return stockCodeNames

    def getStockInfo(self):
        stockCodes = self.getStockCodes()
        # stockCodes = ['9962']

        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='89787198', db='stockevaluation', charset="utf8")
        cur = conn.cursor()
        sql = "UPDATE stocktable SET stockInfo=%s WHERE stockcode=%s"

        for stock in stockCodes:
            url_yahoo = 'https://tw.finance.yahoo.com/d/s/company_' + stock + '.html'
            print(url_yahoo)

            while True:
                nowProxy = self.getProxy(0)
                proxies = {"http": "http://" + nowProxy}
                ua = UserAgent()
                header = {'User-Agent': str(ua.random)}

                try:
                    res = requests.get(url_yahoo, headers=header, proxies=proxies, timeout=self.timeout)
                    res.encoding = 'big5-hkscs'
                    if '奇摩股市' in res.text:
                        print('>>>Found<<<')
                        print(res.text)

                        reGetStockInfo = re.compile(r'td\ width.*?營收比重.*?yui-td-left">(.*?)<\/td>', re.S|re.UNICODE)
                        for stockInfo in reGetStockInfo.findall(res.text):
                            print(stock,stockInfo)
                            while True:
                                try:
                                    cur.execute(sql, (stockInfo.strip(),stock))
                                    conn.commit()
                                    break
                                except:
                                    print("Unexpected error:", sys.exc_info())
                        break
                    elif 'tw.yahoo.com/?err=404' or '奇摩首頁' or '內容目前不可用' in res.text:
                        print('>>>Not Found<<<')
                        print(res.text)
                        break
                except:
                    print("Unexpected error:", sys.exc_info())

        cur.close()
        conn.close()

    def retrieveLowestIndexCurrentIndex(self,date):
        #*** Get lowest indices
        sql = """SELECT sd.stockcode, sd.stockdate, sd.stockindex, sd.stockK, sd.stockD
                FROM (
                SELECT stockcode, MIN(NULLIF(stockindex, 0)) AS minindex
                FROM stockdata
                GROUP BY stockcode
                ) AS mindata INNER JOIN stockdata AS sd ON sd.stockcode=mindata.stockcode AND sd.stockindex=mindata.minindex"""

        while True:
            try:
                # Execute the SQL command
                conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='89787198', db='stockevaluation', charset="utf8")
                cursor = conn.cursor()
                cursor.execute(sql)
                # Fetch all the rows in a list of lists.
                stockCodeDateLowestindex = {}
                results = cursor.fetchall()
                for row in results:
                    stockCodeDateLowestindex[row[0]] = [str(row[1]), row[2], row[3], row[4]]

                print(stockCodeDateLowestindex)
                break
            except:
                print("Error: unable to fecth data")
        #___ Get lowest indices

        #*** Get current indices
        sql = """SELECT * FROM stockdata sd INNER JOIN (
	              SELECT stockCode, MAX(stockDate) AS maxDate FROM stockdata GROUP BY stockCode
                 ) stockMaxDate ON sd.stockCode=stockMaxDate.stockCode AND sd.stockDate=stockMaxDate.maxDate"""

        while True:
            try:
                # Execute the SQL command
                conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='89787198', db='stockevaluation', charset="utf8")
                cursor = conn.cursor()
                cursor.execute(sql)
                # Fetch all the rows in a list of lists.
                stockCodeCurrentindex = {}
                results = cursor.fetchall()
                for row in results:
                    stockCodeCurrentindex[row[1]] = [str(row[2]), row[3], row[4], row[5]]

                print(stockCodeCurrentindex)
                break
            except:
                print("Error: unable to fecth data")
        #___ Get current indices

        #*********** Find potential stocks
        #   1. Select the lowest price of one stock and compare to the current index
        #   2. if the ratio of the absolute value of the difference between the lowest and the current to the lowest is within 10%
        #   3. also pick the KD values these ten days
        #***********
        # sqlGetLastSevenDays = 'SELECT stockcode,stockdate,stockindex,stockK,stockD FROM stockdata WHERE stockcode=%s ORDER BY stockdate DESC LIMIT 7'
        # sqlGetLastSevenDaysInvest = 'SELECT stockcode,stockdate,SUM(stockAmount) FROM stockinstitutionalinvestor WHERE stockcode=%s GROUP BY stockdate ORDER BY stockdate DESC LIMIT 7'
        sqlGetLastSevenDays = """
            SELECT stockindices.stockcode,stockindices.stockdate,stockindices.stockindex,stockindices.stockK,stockindices.stockD,sumSA.sSA FROM
                (SELECT stockcode,stockdate,stockindex,stockK,stockD FROM stockdata WHERE stockcode=%s 
                ORDER BY stockdate DESC LIMIT 7
                ) stockindices LEFT JOIN (
                SELECT stockcode,stockdate,SUM(stockAmount) AS sSA FROM stockinstitutionalinvestor WHERE stockcode=%s 
                GROUP BY stockdate ORDER BY stockdate DESC LIMIT 7) AS sumSA 
            ON stockindices.stockcode=sumSA.stockcode AND stockindices.stockdate=sumSA.stockdate
        """
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='89787198', db='stockevaluation', charset="utf8")
        cursor = conn.cursor()
        stockCodeIndices = {}
        for stock in stockCodeCurrentindex:
            try:
                if abs(float(stockCodeCurrentindex[stock][1])-float(stockCodeDateLowestindex[stock][1]))/float(stockCodeDateLowestindex[stock][1]) < 0.2:
                    while True:
                        try:
                            # Execute the SQL command
                            cursor.execute(sqlGetLastSevenDays, (stock,stock))
                            # Fetch all the rows in a list of lists.
                            results = cursor.fetchall()
                            if results:
                                stockCodeIndices[stock] = []
                                for row in results:
                                    stockCodeIndices[stock].append([str(row[1]), row[2], row[3], row[4], row[5]])
                                stockCodeIndices[stock].append([str(stockCodeDateLowestindex[stock][0]+'(LOWEST)'), stockCodeDateLowestindex[stock][1], stockCodeDateLowestindex[stock][2], stockCodeDateLowestindex[stock][3]])
                            break
                        except:
                            print("Unexpected error:", sys.exc_info())

                    # print(">>>")
                    # print(stock, stockCodeCurrentindex[stock])
                    # print(stock, stockCodeDateLowestindex[stock])
                    # print("<<<")
            except:
                print("Unexpected error:", sys.exc_info())
        print(stockCodeIndices)
        #___ Find potential stocks

        #*** Output to a CSV file
        now = datetime.datetime.now()
        file = open('potentialStocks-'+now.strftime("%Y-%m-%d")+'.csv', 'w', newline='')
        csvCursor = csv.writer(file)

        # write header to csv file
        csvHeader = ['stockCode', 'stockName', 'stockInfo', 'stockDate', 'stockIndex', 'stockK', 'stockD', 'amount']
        csvCursor.writerow(csvHeader)
        line = []
        stockCodeNames = self.getStockNameInfoStartupdate()

        for i in range(len(csvHeader)):
            line.append('----------')
        csvCursor.writerow(line)
        for stock in stockCodeIndices:
            first = True
            print(stock)
            for oneRow in stockCodeIndices[stock]:
                if first and (oneRow[2]>30 or oneRow[3]>30 or re.search('[a-zA-Z]', stock)):
                    break

                oneRow.insert(0, stock)
                oneRow.insert(1, stockCodeNames[stock][0])
                oneRow.insert(2, stockCodeNames[stock][1])
                if first:
                    oneRow.append('https://tw.stock.yahoo.com/q/ta?s=' + stock + '&tech_submit=%ACd+%B8%DF')
                    first = False
                csvCursor.writerow(oneRow)

            if not first:
                csvCursor.writerow([stock, stockCodeNames[stock][0],stockCodeNames[stock][1],str(stockCodeNames[stock][2]) + ' 上市'])
                csvCursor.writerow([])

        file.close()
        #___ Output to a CSV file

        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def make_car_sound():
        print('VRooooommmm!')

    @abstractmethod
    def vehicle_type(self):
        """"Return a string representing the type of vehicle this is."""
        pass