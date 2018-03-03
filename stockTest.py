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

if __name__ == "__main__":
    test = dict()
    test['a'] = 2
    test['b'] = 1
    test['c'] = 3
    test['d'] = 10
    chfreqsorted = sorted(test.items(), key=lambda x: x[1], reverse=True)
    test = dict()
    string = ''
    for one in chfreqsorted:
        string += '\'' + str(one[0]) + '\'' + ':' + str(one[1])
    print(string)
    # sentence = '吃葡萄不吐葡萄皮，不吃葡萄倒吐葡萄皮。'
    # chCharacters = ''
    # for n in re.findall('[\u4e00-\u9fff]+', sentence):
    #     chCharacters += n
    #
    # chlist = [ch for ch in chCharacters]
    # print(listToNGram(chlist,2))
    # print(listToNGram(chlist,3))
    #
    # chfreqdict = listToFreqdict(listToNGram(chlist,2))
    # print(chfreqdict)
    # chfreqsorted = sorted(chfreqdict.items(), key=itemgetter(1), reverse=True)
    # print(chfreqsorted)
    # chfreqdict = listToFreqdict(listToNGram(chlist,3))
    # print(chfreqdict)
    #
    # chfreqsorted = sorted(chfreqdict.items(), key=itemgetter(1), reverse=True)
    # print(chfreqsorted)

    # print(chlist)
    # chfreqdict = listToFreqdict(chlist)
    # print(chfreqdict)

    # chfreqsorted = sorted(chfreqdict.items(), key=itemgetter(1), reverse=True)
    # print(chfreqsorted)

    # chbigram = list2bigram(chlist)
    # chtrigram = list2trigram(chlist)
    # print(chbigram)
    # print(chtrigram)
    #
    # bigramfreqdict = bigram2freqdict(chbigram)
    # trigramfreqdict = trigram2freqdict(chtrigram)
    # print(bigramfreqdict)
    # print(trigramfreqdict)

    # s = "张三，是１个帅哥。"
    # result = FullToHalf(s)
    # print(result)
    # print('-' * 80)
    # print(s)

    # stockNameToCode = {}
    # try:
    #     # Execute the SQL command
    #     conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='89787198', db='stockevaluation',charset="utf8")
    #     cursor = conn.cursor()
    #     cursor.execute("SELECT stockCode,TRIM(TRAILING ';' FROM CONCAT_WS(';',stockName,stockOthername)) AS stockAllnames FROM stocktable")
    #     # Fetch all the rows in a list of lists.
    #     results = cursor.fetchall()
    #     for row in results:
    #         stockNameToCode[row[0]] = row[0]
    #         for stockName in row[1].split(';'):
    #             stockNameToCode[stockName] = row[0]
    #
    #     print(stockNameToCode)
    # except Exception as e:
    #     exc_type, exc_obj, exc_tb = sys.exc_info()
    #     fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #     print(exc_type, fname, exc_tb.tb_lineno)
    # #####################
    #
    # jieba.set_dictionary('jieba/dict.txt.big')
    # # jieba.load_userdict('jieba/userdict.txt')
    #
    # # content = open('jieba/lyric_tw.txt', 'rb').read()
    # content = open('jieba/newsComment.txt', 'r', encoding="utf-8").read()
    #
    # print("Input：", FullToHalf(content))
    #
    # words = jieba.cut(FullToHalf(content), cut_all=False)
    # # words = jieba.tokenize(content)
    #
    # print("Output 精確模式 Full Mode：")
    # # for tk in words:
    # # 	print("word %s\t\t start: %d \t\t end:%d" % (tk[0],tk[1],tk[2]))
    #
    # # Add phrases to jieba
    # for stockName in stockNameToCode:
    #     jieba.suggest_freq(stockName, True)
    #
    # for word in words:
    #     print(word)
    #
    #     for stockName in stockNameToCode:
    #         if stockName in word:
    #             print(stockName,stockNameToCode[stockName],word)
