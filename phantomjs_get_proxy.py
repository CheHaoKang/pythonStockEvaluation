# -*- coding: UTF-8 -*-

from selenium import webdriver
import sys
from lxml import etree
import re
import pymysql.cursors

def importProxies(fileName):
	conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='89787198', db='stockevaluation', charset="utf8")
	cur = conn.cursor()

	with open(fileName, 'r', encoding='UTF-8') as file:
		for line in file:
			try:
				insert = "INSERT IGNORE INTO stockproxies (proxyIPPort, proxyFailtimes, proxyReponseperiod) VALUES (%s, 0, '0')"
				cur.execute(insert, line.strip())
			except:
				print("Unexpected error:", sys.exc_info()[0])
				cur.close()
				conn.close()
				raise

	cur.close()
	conn.commit()
	conn.close()

def getProxy(html):
    reGetProxyIPPort = re.compile(r'script>([\d\.]+)</td')
    proxyIPList = []
    proxyPortList = []

    result = html.xpath('//tbody/tr/td[2]')
    for oneItem in result:
        proxyHtml = etree.tostring(oneItem, pretty_print=True)
        for proxy in reGetProxyIPPort.findall(str(proxyHtml)):
            proxyIPList.append(proxy)

    result = html.xpath('//tbody/tr/td[3]')
    for oneItem in result:
        proxyHtml = etree.tostring(oneItem, pretty_print=True)
        for proxy in reGetProxyIPPort.findall(str(proxyHtml)):
            proxyPortList.append(proxy)

    for i in range(len(proxyIPList)):
        proxyIPList[i] = str(proxyIPList[i]) + ':' + str(proxyPortList[i])

    print(proxyIPList)

    try:
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='89787198',
                               db='stockevaluation', charset="utf8")
        cur = conn.cursor()
        insert = "INSERT IGNORE INTO stockproxies (proxyIPPort) VALUES (%s)" # IGNORE - ignore duplicates
        cur.executemany(insert, proxyIPList)
        cur.close()
        conn.commit()
        conn.close()
    except:
        print("Unexpected error:", sys.exc_info())
        cur.close()
        conn.close()

if __name__ == "__main__":
    # driver = webdriver.PhantomJS(service_args=["--remote-debugger-port=9000"])
    driver = webdriver.PhantomJS()
    driver.implicitly_wait(10)
    driver.get("http://www.gatherproxy.com/proxylist/anonymity/?t=Elite")

    # driver.find_element_by_css_selector("#lst-ib").send_keys("google")
    driver.find_element_by_css_selector("input[class='button']").click()
    html = etree.HTML(driver.page_source)
    getProxy(html)

    try:
        i = 1
        while True:
            driver.find_element_by_xpath("//form[@id='psbform']/div[@class='pagenavi']/a[" + str(i) + "]").click()
            html = etree.HTML(driver.page_source)
            getProxy(html)
            i += 1
    except:
        print("Unexpected error:", sys.exc_info())

