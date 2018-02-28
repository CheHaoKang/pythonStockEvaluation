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

if __name__ == "__main__":
	# s = "张三，是１个帅哥。"
	# result = FullToHalf(s)
	# print(result)
	# print('-' * 80)
	# print(s)

	stockNameToCode = {}
	try:
		# Execute the SQL command
		conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='89787198', db='stockevaluation',charset="utf8")
		cursor = conn.cursor()
		cursor.execute("SELECT stockCode,TRIM(TRAILING ';' FROM CONCAT_WS(';',stockName,stockOthername)) AS stockAllnames FROM stocktable")
		# Fetch all the rows in a list of lists.
		results = cursor.fetchall()
		for row in results:
			stockNameToCode[row[0]] = row[0]
			for stockName in row[1].split(';'):
				stockNameToCode[stockName] = row[0]

		print(stockNameToCode)
	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)
	#####################

	jieba.set_dictionary('jieba/dict.txt.big')
	# jieba.load_userdict('jieba/userdict.txt')

	# content = open('jieba/lyric_tw.txt', 'rb').read()
	content = open('jieba/newsComment.txt', 'r', encoding="utf-8").read()

	print("Input：", FullToHalf(content))

	words = jieba.cut(FullToHalf(content), cut_all=False)
	# words = jieba.tokenize(content)

	print("Output 精確模式 Full Mode：")
	# for tk in words:
	# 	print("word %s\t\t start: %d \t\t end:%d" % (tk[0],tk[1],tk[2]))

	# Add phrases to jieba
	for stockName in stockNameToCode:
		jieba.suggest_freq(stockName, True)

	for word in words:
		print(word)

		for stockName in stockNameToCode:
			if stockName in word:
				print(stockName,stockNameToCode[stockName],word)
