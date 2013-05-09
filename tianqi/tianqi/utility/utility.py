#!/usr/bin/env python
#coding=utf-8

import time

def myiconv(string, f='utf-8', t='gb18030'):
	return string.decode(f).encode(t)

def datestr(datediff = 0, fmt = '%Y%m%d'):
	now = time.time()
	datestr = time.strftime(fmt, time.localtime(now + datediff * 86400))
	return datestr
