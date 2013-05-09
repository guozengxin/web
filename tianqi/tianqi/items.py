# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class TianqiItem(Item):
	# define the fields for your item here like:
	# name = Field()
	cityid = Field()
	date = Field()
	iscurrentday = Field()
	mintemperature = Field()
	maxtemperature = Field()
	weatherstatus = Field()
	windstatus = Field()
	c_temperature = Field()
	c_relativehumidity = Field()
	c_windorientation = Field()
	c_windpower = Field()
	lifetips = Field()

class CityItem(Item):
	cityid = Field()
	url = Field()
	name = Field()
	parentcityid = Field()

	def __init__(self):
		Item.__init__(self)
		cityid = 0
		url = ''
		name = ''
		parentcityid = 0

