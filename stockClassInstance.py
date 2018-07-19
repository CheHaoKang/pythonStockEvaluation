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
    noMultiThread = ['getInstitutionalInvestors', 'retrieveLowestIndexCurrentIndex', 'getPttStockNewsComments','computeStockSentiment','computeNGramfreq','aggregateGramfreq']

    if len(sys.argv) < 2:
        print("The first parameter must be the function you want to call.")
    else :
        timeout = 10
        parameter = None
        training = False
        if len(sys.argv) >= 3:
            parameter = str(sys.argv[2])

            if len(sys.argv) == 4:
                training = (str(sys.argv[3]) == 'True')

        threadAmount = 5
        stockInstance = stockClass(timeout, threadAmount, training)

        funcDict = {
            'retrieveStockData': stockInstance.retrieveStockData,
            'computeStockKD': stockInstance.computeStockKD,
            'getInstitutionalInvestors': stockInstance.getInstitutionalInvestors,
            'retrieveLowestIndexCurrentIndex': stockInstance.retrieveLowestIndexCurrentIndex,
            'computeStockMA': stockInstance.computeStockMA,
            'getPttStockNewsComments': stockInstance.getPttStockNewsComments,
            'computeStockSentiment': stockInstance.computeStockSentiment,
            'computeNGramfreq': stockInstance.computeNGramfreq,
            'aggregateGramfreq': stockInstance.aggregateGramfreq
        }

        if str(sys.argv[1]) not in funcDict.keys():
            print("The function name doesn't exist. ("+ str(', '.join(funcDict.keys())) +")")
            exit(1)

        functionCall = funcDict[str(sys.argv[1])]

        if str(sys.argv[1]) not in noMultiThread:
            stockCodes = stockInstance.getStockCodes()
            stockCodes = ['1337']
            # stockCodes = ['01001T','01004T','01007T','1213','1220','1225','1235','1305','1307','1312A','1321','1324','1418','1432','1435','1436','1438','1441','1445','1446','1452','1453','1454','1456','1457','1464','1465','1466','1469','1470','1471','1472','1475','1476','1506','1521','1525','1526','1529','1530','1535','1539','1541','1616','1617','1708','1709','1721','1727','1732','1802','1805','1806','1808','1810','1906','2002A','2008','2012','2020','2024','2032','2033','2101','2227','2302','2303','2311','2325','2329','2332','2348','2352','2358','2359','2365','2387','2424','2425','2429','2433','2440','2442','2444','2465','2471','2480','2496','2509','2524','2527','2528','2537','2538','2539','2540','2543','2545','2616','2702','2706','2707','2816','2820','2841','2849','2901','2904','2906','2910','2911','3004','3016','3018','3021','3052','3054','3055','3056','3312','3605','4106','4119','4306','4545','4904','5234','5471','5484','5515','5519','5521','5522','5525','5531','5533','5534','5538','5607','5608','5706','5871','5880','5906','5907','6005','6024','6108','6112','6115','6116','6117','6120','6128','6131','6133','6136','6139','6141','6142','6145','6152','6153','6155','6164','6165','6166','6168','6172','6176','6177','6183','6184','6189','6191','6192','6196','6197','6201','6202','6205','6206','6209','6213','6214','6215','6216','6224','6225','6226','6230','6235','6239','6243','6251','6257','6269','6271','6277','6278','6281','6282','6283','6285','6289','8081','8101','8103','8105','8110','8112','8114','8131','8150','8163','8201','8210','8213','8215','8222','8249','8261','8271','8341','8374','8404','8411','8422','8427','8429','8442','8443','8454','8463','8464','8466','8467','8473','8478','8480','8481','8488','8497','8499','8926','8940','8996','9103','910322','910482','9105','910708','910861','9110','911608','911616','911619','911622','911868','912000','912398','9136','9157','9188','9802','9902','9904','9905','9906','9907','9908','9910','9911','9912','9914','9917','9918','9919','9921','9924','9925','9926','9927','9928','9929','9930','9931','9933','9934','9935','9937','9938','9939','9940','9941','9942','9943','9944','9945','9946','9955','9958']
            stockLength = len(stockCodes)

            codeSpanList = []
            for i in range(threadAmount - 1):
                codeSpanList.append([int(stockLength / threadAmount) * i, int(stockLength / threadAmount) * (i + 1)])
            codeSpanList.append([int(stockLength / threadAmount) * (threadAmount - 1), int(stockLength)])

            threads = []

            offset = 0
            for codeSpan in codeSpanList:
                t = threading.Thread(target=functionCall, args=(stockCodes, codeSpan[0], codeSpan[1], offset, parameter))
                threads.append(t)
                offset += 1

            for t in threads:
                t.start()

            for t in threads:
                t.join()

            print('all end: %s' % ctime())
        else:
            # if str(sys.argv[1])!='getPttStockNewsComments':
            functionCall(parameter)
