# -*- coding: UTF-8 -*-
# usesearch
# create at 2015/10/31
# autor: qianqians

import sys
sys.path.append('../')
from pagecache import *
import pymongo
import time
from doclex import doclex
from webget import gethtml

collection_page = None
collection_key = None

def find_page(input, index):
    #print input, type(input)
    keys = doclex.splityspace(input.encode('utf-8', 'ignore'))
    for k in keys:
        collection_key.insert({"key":k})

    def find_page1(keys):
        #print "find_page1"
        page_list = []
        for i in [1, 2, 3]:
            remove_list = []
            #print "keys", keys
            for k in keys:
                #print "key", k, type(k)
                k = doclex.tolower(k)
                #print "key", k
                c = collection_page.find({"key":k, 'weight':i}).limit(10).skip(index*10)
                for i in c:
                    page = {}
                    page['url'] = i['url']
                    page['timetmp'] = i['timetmp']
                    page['key'] = i['key']
                    page_list.append(page)

            for url in page_list:
                c = gethtml.collection_url_profile.find({'key':url['url']})
                if c.count() <= 0:
                    remove_list.append(url)
                    continue
                for i in c:
                    url["profile"] = i['urlprofile']
                    url["date"] = i['date']
                    url["title"] = i['title']

            for url in remove_list:
                page_list.remove(url)

            #print 'page_list', page_list

        return page_list

    page_list = find_page1(keys)

    if len(page_list) == 0:
        keys = doclex.lex(input.encode('utf-8'))
        page_list = find_page1(keys)

    page_list = page_list[0: 10]

    return page_list

def init():
    pass