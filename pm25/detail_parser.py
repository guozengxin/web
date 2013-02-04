#!/usr/bin/env python2.6
#encoding=utf-8

import sys
import StringIO
from lxml import etree
from bs4 import BeautifulSoup
import re

def parse_pm25detail(data):
	citypm25info = {}
	soup = BeautifulSoup(data)

	#分析城市平均pm2.5
	regex = 'jin_value\s+=\s+\"(\d+)\"'
	js = soup.find(text = re.compile(regex))
	if js:
		m = re.search(regex, js.encode('gb18030'))
		if m:
			citypm25info['jin_value'] = m.group(1)

	#分析城市各地区pm2.5
	citypm25info['areainfo'] = []
	div = soup.find(name = 'div', attrs = {'class': 'weilai'})
	if div:
		for tr in div.table:
			if str(tr).find('td') < 0 or str(tr).find('width') >= 0:
				continue
			areainfo = {}
			flag = 0
			regex = '(\d+)'
			for td in [td for td in tr if str(td).find('td') >= 0]:
				value = td.string
				if value:
					value = value.encode('gb18030')
					if flag == 0:
						areainfo['name'] = value.strip()
					elif flag == 1:
						areainfo['aqi'] = value.strip()
					elif flag == 2:
						m = re.search(regex, value.strip())
						if m:
							areainfo['onehour'] = m.group(1)
					elif flag == 3:
						m = re.search(regex, value.strip())
						if m:
							areainfo['twelvehour'] = m.group(1)
					flag += 1
			citypm25info['areainfo'].append(areainfo)
	return citypm25info


	#print js

