# -*- coding: UTF-8 -*-

import pickle
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
from keras.models import load_model

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
    sql = 'SELECT stockCode,stockIndex,stockDate FROM stockdata WHERE stockCode="0050" AND stockDate <= \'2003-12-31\' ORDER BY stockDate ASC'

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
            rows = np.arange(i, min(i + batch_size, max_index))
            i += len(rows)

        samples = np.zeros((len(rows), lookback // step, data.shape[-1]))
        targets = np.zeros((len(rows),))
        for j, row in enumerate(rows):
            indices = range(rows[j] - lookback, rows[j], step)
            samples[j] = data[indices]
            # print(samples[j])
            targets[j] = data[rows[j] + delay][0] # 0 means using stockIndex
            # print(targets[j])
        # print(samples)
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
    normalizeStockData = normalizeData(stockData, part_num*train_parts)

    lookback = 5
    delay = 3
    # min_index = 0
    # max_index = len(normalizeStockData)-1
    batch_size = 10
    step = 1
    # generator(stockData, lookback, delay, 0, None, False, batch_size, step)
    train_gen   = generator(normalizeStockData,
                          lookback=lookback,
                          delay=delay,
                          min_index=0,
                          max_index=part_num*train_parts-1,
                          shuffle=False,
                          step=step,
                          batch_size=batch_size)
    val_gen     = generator(normalizeStockData,
                          lookback=lookback,
                          delay=delay,
                          min_index=part_num*train_parts,
                          max_index=part_num*(train_parts+val_parts)-1,
                          shuffle=False,
                          step=step,
                          batch_size=batch_size)
    test_gen    = generator(normalizeStockData,
                            lookback=lookback,
                            delay=delay,
                            min_index=part_num*(train_parts+val_parts),
                            max_index=None,
                            shuffle=False,
                            step=step,
                            batch_size=batch_size)
    val_steps = ( part_num*(train_parts+val_parts) - part_num*train_parts - lookback)
    test_steps = ( len(normalizeStockData) - part_num*(train_parts+val_parts) - lookback)

    steps_per_epoch = int(part_num*train_parts/batch_size)
    model = Sequential()
    model.add(layers.Flatten(input_shape=(lookback // step, normalizeStockData.shape[-1])))
    model.add(layers.Dense(32, activation='relu'))
    model.add(layers.Dense(1))
    model.compile(optimizer=RMSprop(), loss='mae')
    history = model.fit_generator(train_gen,
                                  steps_per_epoch=steps_per_epoch,
                                  epochs=20,
                                  validation_data=val_gen,
                                  validation_steps=val_steps)

    drawEvaluationDiagram(history)

    # with open('trainHistoryDict.pickle', 'wb') as file_pi:
    #     pickle.dump(history.history, file_pi)
    model.save('stock_trained.h5')
    del model
    model = load_model('stock_trained.h5')

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