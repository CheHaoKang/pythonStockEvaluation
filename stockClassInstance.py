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

if __name__ == "__main__":
	# stockInstance = stockClass(5, 5)
	# stockInstance.computeStockMA(['8429'], 0, 1, 0, '20180202')
	# stockInstance.getStockInfo()

	##############################################
	noMultiThread = ['getInstitutionalInvestors', 'retrieveLowestIndexCurrentIndex']

	if len(sys.argv) < 2:
		print("The first parameter must be the function you want to call.")
	else :
		threadAmount = 5
		stockInstance = stockClass(5, threadAmount)

		funcDict = {
			'retrieveStockData': stockInstance.retrieveStockData,
			'computeStockKD': stockInstance.computeStockKD,
			'getInstitutionalInvestors': stockInstance.getInstitutionalInvestors,
			'retrieveLowestIndexCurrentIndex': stockInstance.retrieveLowestIndexCurrentIndex,
			'computeStockMA': stockInstance.computeStockMA
		}

		if str(sys.argv[1]) not in funcDict.keys():
			print("The function name doesn't exist. ("+ str(', '.join(funcDict.keys())) +")")
			exit(1)

		functionCall = funcDict[str(sys.argv[1])]
		fetchDate = ""
		if len(sys.argv)==3:
			fetchDate = str(sys.argv[2])

		if str(sys.argv[1]) not in noMultiThread:
			stockCodes = stockInstance.getStockCodes()
			# stockCodes = stockCodes[stockCodes.index("2405") + 1:] # comment this line
			stockLength = len(stockCodes)

			codeSpanList = []
			for i in range(threadAmount - 1):
				codeSpanList.append([int(stockLength / threadAmount) * i, int(stockLength / threadAmount) * (i + 1)])
			codeSpanList.append([int(stockLength / threadAmount) * (threadAmount - 1), int(stockLength)])

			threads = []

			offset = 0
			for codeSpan in codeSpanList:
				t = threading.Thread(target=functionCall, args=(stockCodes, codeSpan[0], codeSpan[1], offset, fetchDate))
				threads.append(t)
				offset += 1

			for t in threads:
				t.start()

			for t in threads:
				t.join()

			print('all end: %s' % ctime())
		else:
			functionCall(fetchDate)
