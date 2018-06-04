# -*- coding: UTF-8 -*-

import requests
import pymysql.cursors
import json
import csv
import sys
import datetime
# from fake_useragent import UserAgent
import time
import threading
from time import sleep,ctime
# from openpyxl.styles import Font, Color
from stockClass import *
# from openpyxl import Workbook
from datetime import date
# import jieba
import re
from operator import itemgetter
import glob, os

def FullToHalf(s):
    n = []
    # s = s.decode('utf-8')
    for char in s:
        num = ord(char)
        if num == 0x3000:
            num = 32
        elif 0xFF01 <= num <= 0xFF5E:
            num -= 0xfee0
        num = chr(num)
        n.append(num)
    return ''.join(n)

def listToFreqdict(inputList):
    outputDict=dict()
    print(inputList)
    for i in range(len(inputList)):
        outputDict[tuple(inputList[i])] = outputDict.get(tuple(inputList[i]), 0) + 1
    return outputDict
    # for oneItem in inputList:
    #     print(oneItem)
    #     outputDict[oneItem]=outputDict.get(oneItem,0)+1
    # return outputDict

def listToNGram(inputList,ngram):
    return [inputList[i:i+ngram] for i in range(0,len(inputList)-ngram+1)]

# def bigram2freqdict(mybigram):
#     mydict=dict()
#     for (ch1,ch2) in mybigram:
#         mydict[(ch1,ch2)]=mydict.get((ch1,ch2),0)+1
#     return mydict
#
# def trigram2freqdict(mytrigram):
#     mydict=dict()
#     for (ch1,ch2,ch3) in mytrigram:
#         mydict[(ch1,ch2,ch3)]=mydict.get((ch1,ch2,ch3),0)+1
#     return mydict

def getStockNameInfoStartupdate():
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

def extend_list(val, l=[]):
    print(l)
    l.append(val)
    print(l)
    return l

def test_extend_list():
    # 1
    assert extend_list(1) == [1]
    # 2
    assert extend_list(2, []) == [2]
    # 3
    assert extend_list(3) == [3]

if __name__ == "__main__":
    for f in glob.glob("stockDrawing_*.png"):
        print(f)