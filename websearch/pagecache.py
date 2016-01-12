# -*- coding: UTF-8 -*-
# webseach
# create at 2015/11/5
# autor: qianqians

key_page = {}
cache_page = {}

def ref_cache_page():
    for key,value in cache_page.iteritems():
        if value['timetmp'] > 24*60*60:
            del cache_page[key]

    for key,value in key_page.iteritems():
        if value['timetmp'] > 24*60*60:
            del key_page[key]

