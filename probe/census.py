# -*- coding: utf-8 -*-
# author qianqians
# 2014-11-6

#import pymongo
import math

#enum
#0 < 13
#1 13
#2 14
#...as
#n > 25

def agesection(age):
	if age < 13:
		return 0
	elif age > 25:
		return 14

	return age - 12

def census(ip, port):
	result = []
	for i in xrange(14):
		result.append({'data':[]})

	db = pymongo.Connection(ip, port)
	usercensusdb = db.usercensusdb
	usercensus = usercensusdb.usercensus

	userset = usercensus.find()
	for user in userset:
		_agesection = agesection(user['age'])
		result[_agesection]['data'].append(user)

	return result

def censusdata(key, census, weight=lambda e : e):
	if census.has_key(key):
		return census[key]

	data_len = len(census['data'])
	census['data'].sort(key=lambda e : e[key])

	max = census['data'][-1][key]
	min = census['data'][0][key]

	prev = None
	span_list = []
	for i in xrange(data_len):
		if prev is not None:
			span_prev = float((weight(census['data'][i][key]) - prev))/prev
			span_next = float((weight(census['data'][i][key]) - prev))/weight(census['data'][i][key])
			span_list.append(math.sqrt(pow(span_prev,2)+pow(span_next, 2)))
		prev = weight(census['data'][i][key])

	average_diff = 0
	count = 0
	for i in xrange(len(span_list)):
		if span_list[i] > 0:
			average_diff = average_diff + span_list[i]
			count += 1
	average_diff = average_diff/count

	cut_off_point = []
	for i in xrange(len(span_list)):
		if average_diff < span_list[i]:
			cut_off_point.append((census['data'][i][key], census['data'][i+1][key]))
			span_list[i] = None
	cut_off_point.sort(key=lambda e : e[0])

	refer_separation = [{"min":min, "max":cut_off_point[0][0], "data":[]}]
	for i in xrange(len(cut_off_point)-1):
		refer_separation.append({"min":cut_off_point[i][1], "max":cut_off_point[i+1][0], "data":[]})
	refer_separation.append({"min":cut_off_point[-1][1], "max":max, "data":[]})

	for cut in refer_separation:
		for i in xrange(data_len):
			if cut['min'] <= census['data'][i][key] and cut['max'] >= census['data'][i][key]:
				cut['data'].append(census['data'][i])
	census[key] = refer_separation

	return census

censuss = {'data':[{"key":10000}, {"key":9000}, {"key":8000},{"key":8000},{"key":8000},{"key":8000},{"key":8000},{"key":8000},{"key":8000},{"key":8000}, {"key":7000},
					{"key":1000}, {"key":900}, {"key":800},{"key":800},{"key":800},{"key":800},{"key":800},{"key":800},{"key":800},{"key":800}, {"key":700},
				    {"key":300},{"key":300},{"key":300},{"key":300},{"key":300},{"key":300}, {"key":310},{"key":320},{"key":309},{"key":301},{"key":400},{"key":500},
					{"key":100}, {"key":100},{"key":100},{"key":100},{"key":100},{"key":100},{"key":60},{"key":80},{"key":50},{"key":40},{"key":30},
					{"key":3},{"key":3},{"key":3},{"key":3},{"key":3},{"key":3},{"key":3},{"key":3}]}
censusdata('key', censuss)

for e in censuss['key']:
	print e

censusdata('key', censuss['key'][1])

for e in censuss['key'][1]['key']:
	print e
