# -*- coding: UTF-8 -*-

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

def getStockCodes():
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

def computeStockKD(stockCodes, fromCode, endCode, offset, fetchDate):
    print('#####', fromCode, ctime(), '#####')

    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='89787198', db='stockevaluation', charset="utf8")
    cursor = conn.cursor()

    for i in range(fromCode, endCode):
        # for stock in stockCodes:
        stock = stockCodes[i]
        stockData = []

        fetchSucceed = False
        while not fetchSucceed:
            if fetchDate=="":
                sql = "SELECT * FROM stockdata WHERE stockcode=%s ORDER BY stockDate ASC"
            else:
                sql = "SELECT * FROM stockdata WHERE stockcode=%s ORDER BY stockDate DESC LIMIT 9"

            try:
                cursor.execute(sql, (stock))
                # Fetch all the rows in a list of lists.
                results = cursor.fetchall()
                for row in results:
                    stockData.append([str(row[2]),row[3],row[4],row[5]])
                fetchSucceed = True
            except:
                print("Error: unable to fecth data")

        if len(stockData)<9:
            continue

        if fetchDate!="":
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
            elif stockData[j-1][2]==0.0:
                preK = 50.0
                preD = 50.0
            else:
                preK = stockData[j-1][2]
                preD = stockData[j-1][3]

            slice = stockData[j-8:j+1]
            print(stock,slice)
            print(stockData[j])
            print(max(slice, key=lambda x: x[1]))
            print(min(slice, key=lambda x: x[1]))
            if (float((max(slice, key=lambda x: x[1]))[1])-float(min(slice, key=lambda x: x[1])[1]))!=0:
                rsv = (float(stockData[j][1])-float(min(slice, key=lambda x: x[1])[1]))/(float((max(slice, key=lambda x: x[1]))[1])-float(min(slice, key=lambda x: x[1])[1]))*100.0
            else:
                rsv = 50.0
            curK = 2.0/3.0*preK + 1.0/3.0*rsv
            curD = 2.0/3.0*preD + 1.0/3.0*curK
            print(rsv, preK, preD)
            print((curK,curD,stock,stockData[j][0]))
            stockKDList.append((curK,curD,stock,stockData[j][0]))

        try:
            sql = "UPDATE stockdata SET stockK=%s, stockD=%s WHERE stockCode=%s AND stockDate=%s"
            cursor.executemany(sql, stockKDList)
            conn.commit()
        except:
            print("Unexpected error:", sys.exc_info())

    cursor.close()
    conn.close()

if __name__ == "__main__":
    stockCodes = getStockCodes()
    stockLength = len(stockCodes)

    # Search for a specific date
    fetchDate = ""
    if len(sys.argv) == 2:
        fetchDate = str(sys.argv[1])

    computeStockKD(stockCodes,0,stockLength,0,fetchDate)