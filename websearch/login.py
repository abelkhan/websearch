# -*- coding: UTF-8 -*-
# darkforce
# create at 2015/9/17
# autor: qianqians

import pymongo
import globalv

def register_user(name, key):
	c = globalv.collection_user.find({"username":name}).count()
	if c > 0:
		return False
	else:
		globalv.collection_user.insert({"username":name, "key":key})
		return True

def find_user(name):
	try:
		print name,globalv.collection_user
		c = globalv.collection_user.find({"username":name})
		print c.count(), name
		return c[0]
	except:
		return None

def longin_user(c, name, key):
	print c["username"], c["key"], "login"
	if name == c["username"]:
		if key == c["key"]:
			print "login"
			return True
	return False