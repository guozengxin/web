#!/usr/bin/env python
#encoding=utf8

import urllib2
import sys
import ConfigParser
import MySQLdb as mdb
import time
from urllib2 import HTTPError, URLError

import detail_parser
from html_parser import PM25MainHtmlParser

#global
g_cp = ConfigParser.ConfigParser()

def http_get(url):
	'''get html file from web'''
	data = None
	try:
		request = urllib2.Request(url)
		request.add_header("User-agent", "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6")
		response = urllib2.urlopen(request, timeout=20)
		data = response.read()
	except HTTPError, e:
		pass
	except URLError, e:
		pass
	except IOError, e:
		pass
	except:
		pass
	return data

def list_get(listfile):
	'''get list from file'''
	fp = open(listfile)
	return [line.strip() for line in fp.readlines()]

def parse_main_pm25():
	'''parse pm2.5 main page, return the city-url-list'''
	global g_cp
	main_pm25_url = g_cp.get("address", "mainurl")
	cityfile = g_cp.get("address","cityfile")
	data = http_get(main_pm25_url)
	data = data.decode("utf8", "replace").encode("gb18030")
	mainparser = PM25MainHtmlParser(main_pm25_url)
	mainparser.feed(data)
	linklist = mainparser.get_linklist()
	cl = list_get(cityfile)
	return [ll for ll in linklist if ll[-1] in cl]

def parse_detail_pm25(cu):
	url = cu[0]
	city = cu[-1]
	print url
	data = http_get(url)
	cityinfo = detail_parser.parse_pm25detail(data.decode('utf8', 'replace'))
	cityinfo['name'] = city
	return cityinfo

def insert_into_mysql(cu):
	db = None
	try:
		db = mdb.Connect("", "", "", "")
		cursor = db.cursor()
		for ai in cu['areainfo']:
			city = cu['name']
			area = ai['name']
			aqi = ai['aqi']
			FORMAT = "%Y%m%d%H"
			ymdh = time.strftime(FORMAT, time.localtime(time.time()))
			print ymdh
			sqlstr = "insert into area_city_info (time, area, city, aqi, pm2d5_1hour, pm2d5_12hour) values('%s', '%s', '%s', %d, %d, %d);"%\
					(ymdh, area, city, int(aqi), int(ai['onehour']), int(ai['twelvehour']))
			cursor.execute(sqlstr)
	finally:
		if db:
			db.close()

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print >> sys.stderr, "ERROR need configuration file"
		sys.exit(-1)
	cfg = sys.argv[1]
	g_cp.read(cfg)
	parse_main_pm25()
	cityurllist = parse_main_pm25()
	for cu in cityurllist:
		cityinfo = parse_detail_pm25(cu)
		insert_into_mysql(cityinfo)
