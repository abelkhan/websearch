# -*- coding: UTF-8 -*-
# webseach
# create at 2015/10/30
# autor: qianqians

import sys
reload(sys)
sys.setdefaultencoding('utf8')

sys.path.append('../')

from webget import gethtml
import pymongo
from doclex import doclex
import time

collection_key = None

def seach(urllist):
    gethtml.process_url_list = []

    def process_keyurl(keyurl):
        if keyurl is not None:
            for key1, urllist in keyurl.iteritems():
                for url in urllist:
                    #print url
                    if url[len(url) - 1] == '/':
                        url = url[0:-1]
                        #print url

                    #print url

                    urlinfo = gethtml.process_url(url)

                    if urlinfo is None:
                        continue

                    if isinstance(urlinfo, str) and urlinfo == "url is be processed":
                        key = ""
                        for c in key1:
                            if c >= 'A' and c <= 'Z':
                                c = c.lower()
                            key += c
                        gethtml.collection.update({'key':key, 'url':url}, {'$set':{'key':key, 'url':url, 'timetmp':time.time()}}, True)
                    else:
                        list, keyurl1 = urlinfo

                        key = ""
                        for c in key1:
                            if c >= 'A' and c <= 'Z':
                                c = c.lower()
                            key += c
                        gethtml.collection.update({'key':key, 'url':url}, {'$set':{'key':key, 'url':url, 'timetmp':time.time()}}, True)

                        if keyurl1 is not None:
                            process_keyurl(keyurl1)

    def process_urllist(url_list):
        for url in url_list:
            #print url
            if url[len(url) - 1] == '/':
                url = url[0:-1]
                #print url

            #print url

            urlinfo = gethtml.process_url(url)

            if urlinfo is None or isinstance(urlinfo, str):
                continue

            list, keyurl = urlinfo

            if list is not None:
                process_urllist(list)

            if keyurl is not None:
                process_keyurl(keyurl)

            time.sleep(0.1)

    for url in urllist:
        print url, "root url"

        urlinfo = gethtml.process_url(url)

        if urlinfo is None or isinstance(urlinfo, str):
            print "error root url",url
            continue

        list, keyurl = urlinfo

        #print list
        #print keyurl

        try:
            process_urllist(list)
            process_keyurl(keyurl)

        except:
            import traceback
            traceback.print_exc()

urllist = ["http://www.baidu.com",
           "http://www.google.com",
           "http://www.xitek.com/",
           "http://www.zol.com.cn/",
           "http://www.weiqiok.com/",
           "http://www.cnblogs.com",
           "http://www.csdn.net",
           "http://www.cppblog.com",
           "http://codingnow.com",
           'http://www.jobbole.com',
           'http://www.w3school.com.cn',
           "http://sina.com.cn",
           "http://www.tom.com",
           "http://www.qq.com",
           "http://www.qidian.com/Default.aspx",
           "http://www.zongheng.com",
           "http://chuangshi.qq.com",
           "http://www.jjwxc.net",
           "https://www.hao123.com",
           "http://www.163.com",
           "http://jj.hbtv.com.cn",
           "https://www.taobao.com",
           "http://www.jd.com",
           "http://www.suning.com",
           "http://jiadian.gome.com.cn"]

def refkeywords():
    c = collection_key.find()
    keywords = []
    for it in c:
        keywords.append(it["key"])
    doclex.keykorks = keywords

if __name__ == '__main__':
    conn = pymongo.Connection('localhost',27017)
    db = conn.webseach
    gethtml.collection = db.webpage
    gethtml.collection_url_profile = db.urlprofile
    gethtml.collection_url_title = db.urltitle
    collection_key = db.keys

    t = 0
    while True:
        timetmp = time.time()-t
        if timetmp > 86400:
            refkeywords()
            t = time.time()
        #urllist = seach(urllist)
        seach(urllist)