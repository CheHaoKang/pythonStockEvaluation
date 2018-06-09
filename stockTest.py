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
# from keras.datasets import boston_housing
# from keras.datasets import reuters
# from keras.preprocessing.text import Tokenizer
from keras.models import Sequential
from keras import layers
from keras.optimizers import RMSprop
import matplotlib.pyplot as plt

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

def vectorize_sequences(sequences, dimension=10000):
    results = np.zeros((len(sequences), dimension))
    for i, sequence in enumerate(sequences):
        print(i, sequence)
        results[i, sequence] = 1.
        for j in results[i]:
            print(j,)
        exit(1)
    return results


def drawEvaluationDiagram(history):
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    epochs = range(1, len(loss) + 1)
    plt.figure()
    plt.plot(epochs, loss, 'bo', label='Training loss')
    plt.plot(epochs, val_loss, 'b', label='Validation loss')
    plt.title('Training and validation loss')
    plt.legend()
    plt.show()

def normalizeData(data, train_length):
    mean = data[:train_length].mean(axis=0)
    data -= mean
    std = data[:train_length].std(axis=0)
    data /= std

    return data

def getStockData(stockCode):
    skipColumns = 2  # skip stockCode and stockDate
    # sql = 'SELECT stockCode,stockIndex,stockDate FROM stockdata WHERE stockCode="0050" ORDER BY stockDate ASC'
    sql = 'SELECT stockCode,stockIndex,stockDate FROM stockdata WHERE stockCode="0050" AND stockDate <= \'2003-07-31\' ORDER BY stockDate ASC'

    conn = pymysql.connect(host='192.168.2.55', port=3306, user='root', passwd='89787198', db='stockevaluation', charset="utf8")
    cursor = conn.cursor()
    cursor.execute(sql)

    results = cursor.fetchall()
    stockData = np.zeros( (len(results), len(results[0])-skipColumns) )
    for i,row in enumerate(results):
        # stockData.append([row[0], row[1], str(row[2])])
        stockData[i,:] = [row[1]]

    # print(stockData)
    return stockData

# Deep Learning with Python => Page 211 (234 / 386)
def generator(data, lookback, delay, min_index, max_index, shuffle=False, batch_size=128, step=1):
    if max_index is None:
        max_index = len(data) - delay - 1
    else:
        max_index = max_index - delay

    i = min_index + lookback
    while 1:
        if shuffle:
            rows = np.random.randint(min_index + lookback, max_index, size=batch_size)
        else:
            if i + batch_size >= max_index:
                i = min_index + lookback
            print(i, i + batch_size, min(i + batch_size, max_index))
            rows = np.arange(i, min(i + batch_size, max_index))
            i += len(rows)

        samples = np.zeros((len(rows), lookback // step, data.shape[-1]))
        targets = np.zeros((len(rows),))
        print(rows)
        for j, row in enumerate(rows):
            indices = range(rows[j] - lookback, rows[j], step)
            samples[j] = data[indices]
            # print(samples[j])
            targets[j] = data[rows[j] + delay][0] # 0 means using stockIndex
            # print(rows[j])
            # print(targets[j])
        # print(samples)
        # print(targets)
        # exit(1)
        yield samples, targets
        # return samples, targets

if __name__ == "__main__":
    stockData = getStockData('0050')

    num_parts = 5
    train_parts = 3
    val_parts = 1
    test_parts = 1
    part_num = int(len(stockData)/num_parts)
    # normalizeStockData = normalizeData(stockData, part_num*train_parts)

    lookback = 5
    delay = 10
    # min_index = 0
    # max_index = len(normalizeStockData)-1
    batch_size = 10
    step = 1
    generator(stockData, lookback, delay, 0, 20, False, batch_size, step)
    # for one in generator(normalizeStockData, lookback, delay, min_index, max_index, False, batch_size, step):
    #     print(one)
    #     print('\n')

    #*** 211 (234 / 386)
    # data_dir = '.'
    # fname = os.path.join(data_dir, 'jena_climate_2009_2016.csv')
    # f = open(fname)
    # data = f.read()
    # f.close()
    # lines = data.split('\n')
    # header = lines[0].split(',')
    # lines = lines[1:]
    # # print(lines)
    #
    # float_data = np.zeros((len(lines), len(header) - 1))
    # for i, line in enumerate(lines):
    #     values = [float(x) for x in line.split(',')[1:]]
    #     # print(values)
    #     if len(values)==len(header) - 1:
    #         float_data[i, :] = values
    # float_data = float_data[:-1]
    # print(float_data)
    # print(float_data.shape, float_data.shape[-1])
    #
    # lookback = 5
    # step = 1
    # samples = np.zeros((len(float_data)-lookback, lookback/step, float_data.shape[-1]))
    # for one in samples:
    #     print(one)
    #     print('\n')
    #___ 211 (234 / 386)

    # a = generator()
    # for i in a:
    #     print(i)
    # rows = np.random.randint(0, 10, size=6)
    # print(rows)
    # for j, row in enumerate(rows):
    #     print(j, row)