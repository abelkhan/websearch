# -*- coding: UTF-8 -*-
# darkforce
# create at 2015/9/17
# autor: qianqians

import pymongo
import globalv

def unregister_mail(mail):
	c = globalv.collection_user.find({"mail":mail}).count()
	if c > 0:
		return False
	return True

def register_user(name, key, mail):
	c = globalv.collection_user.find({"username":name}).count()
	if c > 0:
		return False
	else:
		globalv.collection_user.insert({"username":name, "key":key, "mail":mail})
		return True

def find_user(name):
	try:
		c = globalv.collection_user.find({"username":name})
		return c[0]
	except:
		return None

def longin_user(c, name, key):
	if name == c["username"]:
		if key == c["key"]:
			return True
	return False