#!/usr/bin/env python
#encoding=utf8

import sys
import urlparse
from HTMLParser import HTMLParser

class PM25MainHtmlParser(HTMLParser):
	def __init__(self,url):
		self.linklist = []
		self.link = ''
		self.anchortext = ''
		self.url = url
		HTMLParser.__init__(self)

	def handle_starttag(self, tag, attrs):
		HTMLParser.handle_starttag(self, tag, attrs)
		if tag == 'a':
			for name, value in attrs:
				if name == 'href':
					self.link = urlparse.urljoin(self.url, value)

	def handle_data(self, data):
		if len(self.link) > 0:
			self.anchortext += ' ' + data.strip()

	def handle_endtag(self, tag):
		HTMLParser.handle_endtag(self, tag)
		if tag == 'a':
			if self.anchortext:
				self.anchortext = self.anchortext.strip()
			if len(self.anchortext) > 0 and len(self.link) > 0:
				self.linklist.append([self.link, self.anchortext])

			self.link = ''
			self.anchortext = ''

	def get_linklist(self):
		return self.linklist
