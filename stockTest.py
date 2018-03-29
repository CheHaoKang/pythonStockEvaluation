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
from openpyxl.styles import Font, Color
from stockClass import *
from openpyxl import Workbook
from datetime import date
import jieba
import re
from operator import itemgetter

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

if __name__ == "__main__":
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='89787198', db='stockevaluation', charset="utf8")
    cursor = conn.cursor()

    stockCodeNames = getStockNameInfoStartupdate()
    # *** Draw diagrams
    days = 14
    x = []
    for i in range(1, days + 1):
        x.append(i)
    x = np.asarray(x)  # since zip doesn't accept list

    first = True
    qualifiedStocks = ['0050']
    for stock in qualifiedStocks:
        plt.rcParams["figure.figsize"] = [12,
                                          6]  # set figure size to enlarge the plot. Remember to do >>> \includegraphics[width=1.0\textwidth] <<<
        fig, (subplot1, subplot2) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [5, 1]})  # )
        subplot1.set_title(stock + '_' + stockCodeNames[stock][0] + '(' + stockCodeNames[stock][1][:70] + ')')

        stockInfoDict = {}
        stockInfoDict['date'] = []
        stockInfoDict['index'] = []
        stockInfoDict['ma18'] = []
        stockInfoDict['ma50'] = []
        stockInfoDict['k'] = []
        stockInfoDict['d'] = []
        stockInfoDict['amount'] = []
        for oneRow in stockCodeIndices[stock]:
            stockInfoDict['date'].append(oneRow[0])
            stockInfoDict['index'].append(oneRow[1])
            stockInfoDict['ma18'].append(oneRow[2])
            stockInfoDict['ma50'].append(oneRow[3])
            stockInfoDict['k'].append(oneRow[4])
            stockInfoDict['d'].append(oneRow[5])
            try:
                stockInfoDict['amount'].append(oneRow[6]) if oneRow[6] else stockInfoDict['amount'].append(0)
            except:
                print("Unexpected error:", sys.exc_info())

        print(stockInfoDict)

        xtickLabels = stockInfoDict['date'][::-1][1:]  # remove the lowest info
        lowestIndex = stockInfoDict['index'][-1]
        stockInfoDict['index'] = stockInfoDict['index'][::-1][1:]  # remove the lowest info
        stockInfoDict['ma18'] = stockInfoDict['ma18'][::-1][1:]  # remove the lowest info
        stockInfoDict['ma50'] = stockInfoDict['ma50'][::-1][1:]  # remove the lowest info
        stockInfoDict['k'] = stockInfoDict['k'][::-1][1:]  # remove the lowest info
        stockInfoDict['d'] = stockInfoDict['d'][::-1][1:]  # remove the lowest info
        stockInfoDict['amount'] = stockInfoDict['amount'][::-1]

        print(stockInfoDict)

        plt.setp(subplot1, xticks=x, xticklabels=xtickLabels, xlim=[0, days + 1])  # , ylabel='score')
        # plt.xticks(rotation=10)
        for tick in subplot1.get_xticklabels():
            tick.set_rotation(20)
        pL11 = subplot1.plot(x, stockInfoDict['index'], '', label='stockIndex', zorder=10)
        for xCor, yCor in zip(x, stockInfoDict['index']):
            subplot1.text(xCor, yCor, str(yCor), weight='bold')
            # subplot1.text(xCor-0.2, yCor-0.06, str(yCor), weight='bold')
        pL12 = subplot1.plot(x, stockInfoDict['ma18'], '', label='stockMA18', zorder=10)
        # for xCor, yCor in zip(x, y2):
        #     subplot1.text(xCor, yCor+0.05, str(yCor), weight='bold')
        pL13 = subplot1.plot(x, stockInfoDict['ma50'], '', label='stockMA50', zorder=10)
        # for xCor, yCor in zip(x, y3):
        #     subplot1.text(xCor, yCor-0.05, str(yCor), weight='bold')
        subplot1.plot(0.1, lowestIndex, 'ro')
        subplot1.text(0.1, lowestIndex, str(lowestIndex), weight='bold')

        amountColor = []
        for amIndex in range(len(stockInfoDict['amount'])):
            if int(stockInfoDict['amount'][amIndex]) < 0:
                amountColor.append('green')
                stockInfoDict['amount'][amIndex] = -float(stockInfoDict['amount'][amIndex])
            else:
                amountColor.append('red')

        print(stockInfoDict['amount'])

        width = 0.5
        pLBar = subplot1.twinx()
        if max(stockInfoDict['amount']) * 1.1 != 0:
            maxAmount = max(stockInfoDict['amount']) * 1.1
        else:
            maxAmount = 10000
        plt.setp(pLBar, xticks=x, xticklabels=xtickLabels, xlim=[0, days + 1], ylim=[0, maxAmount])

        pLBar.bar(x, stockInfoDict['amount'], width, alpha=0.2, label='amount', color=amountColor, zorder=1)
        for xCor, yCor in zip(x - width / 2, stockInfoDict['amount']):
            pLBar.text(xCor, yCor, str(int(yCor)))

        # 'best'         : 0, (only implemented for axis legends)
        # 'upper right'  : 1,
        # 'upper left'   : 2,
        # 'lower left'   : 3,
        # 'lower right'  : 4,
        # 'right'        : 5,
        # 'center left'  : 6,
        # 'center right' : 7,
        # 'lower center' : 8,
        # 'upper center' : 9,
        # 'center'       : 10,

        h1, l1 = subplot1.get_legend_handles_labels()
        lgd = subplot1.legend(h1, l1, loc=8, fancybox=False, shadow=False,
                              ncol=1)  # http://matplotlib.org/users/legend_guide.html

        # subplot2
        plt.setp(subplot2, xticks=x, xticklabels='')  # , ylabel='score')
        pL21 = subplot2.plot(x, stockInfoDict['k'], '', label='stockK', zorder=10)
        # for xCor, yCor in zip(x, y21):
        #     subplot2.text(xCor-0.08, yCor+1, str("%.2f" % (yCor)), weight='bold')
        pL22 = subplot2.plot(x, stockInfoDict['d'], '', label='stockD', zorder=10)
        # for xCor, yCor in zip(x, y22):
        #     subplot2.text(xCor-0.08, yCor-10, str("%.2f" % (yCor)), weight='bold')
        subplot2.axhline(y=20, color='g', linestyle='--')
        subplot2.axhline(y=80, color='r', linestyle='-.')

        h2, l2 = subplot2.get_legend_handles_labels()
        lgd2 = subplot2.legend(h2, l2, loc=3, fancybox=False, shadow=False,
                               ncol=1)  # http://matplotlib.org/users/legend_guide.html

        fig.tight_layout()
        fig.savefig('stockDrawing_' + stock + '_' + stockCodeNames[stock][0] + '.png', bbox_inches='tight')
        plt.close(fig)
    # ___ Draw diagrams

    conn.commit()
    cursor.close()
    conn.close()