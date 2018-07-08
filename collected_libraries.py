# -*- coding: UTF-8 -*-

import glob
import re
import pymysql
import os

def getStockCodesByDate(updatedDate, fromStockCode='0'):
    sql = 'SELECT DISTINCT(stockCode) FROM stockData WHERE stockCode>=%s AND stockDate=%s ORDER BY stockCode ASC'

    conn = pymysql.connect(host='192.168.2.55', port=3306, user='root', passwd='89787198', db='stockevaluation', charset="utf8")
    cursor = conn.cursor()
    cursor.execute(sql, (fromStockCode, updatedDate))

    results = cursor.fetchall()
    stockCodes = []
    for i, row in enumerate(results):
        stockCodes.append(row[0])

    cursor.close()
    conn.close()

    return stockCodes

def get_files_in_directory(directory_name, file_name_re=''):
    filenames = []
    for filename in os.listdir(directory_name):
        if file_name_re:
            re_compile = re.compile(file_name_re, re.S | re.UNICODE)
            for file_part in re_compile.findall(filename):
                filenames.append(file_part)
        else:
            filenames.append(filename)

    return filenames

if __name__ == "__main__":
    stockCodes = getStockCodesByDate('2018-07-05', '0')
    filenames = get_files_in_directory('stock_model', r'stock_([\w]+?)_model\.h5')

    print([one_stock for one_stock in stockCodes if one_stock not in filenames])
    exit(1)