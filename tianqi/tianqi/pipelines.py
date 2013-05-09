# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

import MySQLdb
import MySQLdb.cursors

from twisted.enterprise import adbapi
from scrapy.exceptions import DropItem
from tianqi.items import CityItem, TianqiItem
from scrapy import log
from tianqi.utility.utility import myiconv

class TianqiPipeline(object):
	def __init__(self):
		self.dbpool = adbapi.ConnectionPool('MySQLdb',
				db = 'test',
				user = 'xiaoxin',
				passwd = 'xiaoxin',
				cursorclass=MySQLdb.cursors.DictCursor,
				use_unicode=True
		)

	def process_item(self, item, spider):
		query = self.dbpool.runInteraction(self._item_insert, item)
		query.addErrback(self.handle_error)
		return item

	def _item_insert(self, tx, item):
		if isinstance(item, CityItem):
			#process cityItem
			name= myiconv(item['name'])
			url = myiconv(item['url'])
			sqlstring = 'replace into cityinfo(cityid, url, name, parentcityid) values(%s, %s, %s, %s)'
			tx.execute(sqlstring, [item['cityid'], item['url'], name, item['parentcityid']])
			log.msg("replace cityinfo: (%s, %s, %s, %s)" % (item['cityid'], url, name, item['parentcityid']))
		elif isinstance(item, TianqiItem):
			#process tianqiItem
			if item['iscurrentday']:
				sqlstring = 'replace into tianqiinfo(cityid, date, mintemperature, maxtemperature, weatherstatus, windstatus, c_temperature, c_relativehumidity, c_windpower, lifetips) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
				strs = []
				strs.append(item['cityid'])
				strs.append(item['date'])
				strs.append(myiconv(item['mintemperature']))
				strs.append(myiconv(item['maxtemperature']))
				strs.append(myiconv(item['weatherstatus']))
				strs.append(myiconv(item['windstatus']))
				strs.append(myiconv(item['c_temperature']))
				strs.append(myiconv(item['c_relativehumidity']))
				strs.append(myiconv(item['c_windpower']))
				strs.append(myiconv(item['lifetips']))
				tx.execute(sqlstring, strs)
				log.msg('insert currentday tianqi info cityid %d date %s' % (item['cityid'], item['date']))
			else:
				sqlstring = 'replace into tianqiinfo(cityid, date, mintemperature, maxtemperature, weatherstatus, windstatus) values (%s, %s, %s, %s, %s, %s)'
				strs = []
				strs.append(item['cityid'])
				strs.append(item['date'])
				strs.append(myiconv(item['mintemperature']))
				strs.append(myiconv(item['maxtemperature']))
				strs.append(myiconv(item['weatherstatus']))
				strs.append(myiconv(item['windstatus']))
				tx.execute(sqlstring, strs)
				log.msg('insert future tianqi info cityid %d date %s' % (item['cityid'], item['date']))

	def handle_error(self, e):
		log.err(e)
