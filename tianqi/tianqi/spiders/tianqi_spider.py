#!/usr/bin/env python
#coding=utf-8

import MySQLdb

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.shell import inspect_response
from tianqi.items import TianqiItem, CityItem
from tianqi.utility import utility

BASE_URL = 'http://www.tianqi.com/chinacity.html'

class TianqiSpiderSpider(CrawlSpider):
	name = 'tianqi_spider'
	allowed_domains = ['tianqi.com']
	start_urls = [BASE_URL]

	rules = (
		#Rule(SgmlLinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
	)

	def __init__(self):
		CrawlSpider.__init__(self)
		self.db = MySQLdb.connect(host = 'localhost', user = 'xiaoxin', passwd = 'xiaoxin', db = "test")
		self.cursor = self.db.cursor()

	def parse(self, response):
		'''parse tianqi.com
		'''
		url = response.url
		hxs = HtmlXPathSelector(response)
		citys = hxs.select('//ul[@class="bcity"]/li/a')
		i = 1
		requests = []
		for city in citys:
			item = CityItem()
			item['url'], item['name'], item['cityid'], item['parentcityid'] = '', '', i, 0
			cityurl = city.select('./@href').extract()[0].encode('utf-8')
			if cityurl != '#':
				item['url'] = cityurl
				item['name'] = city.select('./text()').extract()[0].encode('utf-8')
				request = Request(url = cityurl, meta = {'cityid': i}, callback = self.parse_item)
				requests.append(request)
				yield item
				i += 1
		for request in requests:
			yield request
		#return items

	def parse_item(self, response):
		'''parse tianqi.com item
		'''
		url = response.url
		cityid = response.meta['cityid']
		hxs = HtmlXPathSelector(response)
		#当天天气情况
		todaynode = hxs.select('//div[@class="today_data"]')
		if todaynode:
			item = TianqiItem()
			item['iscurrentday'] = True
			item['cityid'] = cityid
			item['date'] = utility.datestr()
			#气温，阴晴，风
			node = todaynode.select('./div[@class="today_data_w"]')
			if node:
				temp = node.select('.//ul/li/span[@id="t_temp"]/font[2]/text()').extract()[0]
				item['mintemperature'] = temp[:-1].encode('utf-8')
				temp = node.select('.//ul/li/span[@id="t_temp"]/font[1]/text()').extract()[0]
				item['maxtemperature'] = temp[:-1].encode('utf-8')
				item['weatherstatus'] = node.select('(.//ul/li)[last()-1]/text()').extract()[0].encode('utf-8')
				#print item['weatherstatus'].decode('utf-8').encode('gb18030')
				item['windstatus'] = node.select('(.//ul/li)[last()]/text()').extract()[0].encode('utf-8')
				#print item['windstatus'].decode('utf-8').encode('gb18030')
			#当前温度，风向，风力
			node = todaynode.select('./div[@class="today_data_m"]')
			if node:
				temp = node.select('.//div[@id="rettemp"]/strong/text()').extract()[0]
				item['c_temperature'] = temp[:-1].encode('utf-8')
				item['c_relativehumidity'] = node.select('.//div[@id="rettemp"]/span/text()').extract()[0].encode('utf-8')
				#print item['c_relativehumidity'].decode('utf-8').encode('gb18030')
				item['c_windpower'] = node.select('.//div[@id="retwind"]/strong/text()').extract()[0].encode('utf-8')
				#print item['c_windpower'].decode('utf-8').encode('gb18030')
				item['c_windorientation'] = node.select('.//div[@id="retwind"]/span/text()').extract()[0].encode('utf-8')
				#print item['c_windorientation'].decode('utf-8').encode('gb18030')
			node = todaynode.select('./div[@class="today_data_r01"]')
			if node:
				strs = []
				nodes = node.select('./ul/li')
				for n in nodes:
					str1 = n.select('./text()').extract()[0].encode('utf-8')
					str2 = n.select('./span/text()').extract()[0].encode('utf-8')
					strs.append(str1 + str2)
				item['lifetips'] = '\n'.join(strs)
				#print '\n'.join(strs).decode('utf-8').encode('gb18030')
			yield item
		#未来几天天气情况
		daynodes = hxs.select('//div[@id="detail"]/div[@class="tqshow1"]')
		for daynode in daynodes[1:]:
			item = TianqiItem()
			item['iscurrentday'] = False
			item['cityid'] = cityid
			item['date'] = utility.datestr(daynodes.index(daynode))
			temp = daynode.select('.//ul/li[2]/font[1]/text()').extract()[0]
			item['maxtemperature'] = temp[:-1].encode('utf-8')
			temp = daynode.select('.//ul/li[2]/font[2]/text()').extract()[0]
			item['mintemperature'] = temp[:-1].encode('utf-8')
			item['weatherstatus'] = daynode.select('.//ul/li[3]/text()').extract()[0].encode('utf-8')
			item['windstatus'] = daynode.select('.//ul/li[4]/text()').extract()[0].encode('utf-8')
			yield item
