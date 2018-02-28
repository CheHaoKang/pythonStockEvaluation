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

if __name__ == "__main__":
	jieba.set_dictionary('jieba/dict.txt.big')
	jieba.load_userdict('jieba/userdict.txt')

	# content = open('jieba/lyric_tw.txt', 'rb').read()
	content = open('jieba/lyric_tw.txt', 'r', encoding="utf-8").read()

	print("Input：", content)

	# words = jieba.cut(content, cut_all=False)
	words = jieba.tokenize(content)

	print("Output 精確模式 Full Mode：")
	for tk in words:
		print("word %s\t\t start: %d \t\t end:%d" % (tk[0],tk[1],tk[2]))
	# for word in words:
	# 	print(word)