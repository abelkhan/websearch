# -*- coding: UTF-8 -*-
# webseach
# create at 2015/10/30
# autor: qianqians

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

sys.path.append('../')

from webget import gethtml
import pymongo
from doclex import doclex
import time
import chardet

collection_key = None

def ingoreurl(url):
    count = 0
    for ch in url:
        if ch == '/':
            count += 1

    return count > 4

def seach(urllist):
    gethtml.process_url_list = []

    def process_keyurl(keyurl):
        if keyurl is not None:
            for key1, urllist in keyurl.iteritems():
                for url in urllist:
                    if url[len(url) - 1] == '/':
                        url = url[0:-1]

                    if ingoreurl(url):
                        continue

                    urlinfo = gethtml.process_url(url)

                    if urlinfo is None:
                        continue

                    if isinstance(urlinfo, str) and urlinfo == "url is be processed":
                        key = ""
                        for c in key1:
                            if c >= 'A' and c <= 'Z':
                                c = c.lower()
                            key += c
                        try:
                            encodingdate = chardet.detect(key)
                            if encodingdate['encoding']:
                                key = unicode(key, encodingdate['encoding'])
                            else:
                                key = unicode(key, 'utf-8')
                            gethtml.collection.update({'key':key, 'url':url}, {'$set':{'key':key, 'url':url, 'timetmp':time.time(), 'weight':3}}, True)
                        except:
                            import traceback
                            traceback.print_exc()
                    else:
                        list, keyurl1 = urlinfo

                        key = ""
                        for c in key1:
                            if c >= 'A' and c <= 'Z':
                                c = c.lower()
                            key += c
                        try:
                            encodingdate = chardet.detect(key)
                            if encodingdate['encoding']:
                                key = unicode(key, encodingdate['encoding'])
                            else:
                                key = unicode(key, 'utf-8')
                            gethtml.collection.update({'key':key, 'url':url}, {'$set':{'key':key, 'url':url, 'timetmp':time.time(), 'weight':3}}, True)
                        except:
                            import traceback
                            traceback.print_exc()


                        if list is not None:
                            process_urllist(list)

                        if keyurl1 is not None:
                            process_keyurl(keyurl1)

    def process_urllist(url_list):
        for url in url_list:
            if url[len(url) - 1] == '/':
                url = url[0:-1]

            if ingoreurl(url):
                continue

            urlinfo = gethtml.process_url(url)

            if urlinfo is None or isinstance(urlinfo, str):
                continue

            list, keyurl = urlinfo

            if list is not None:
                process_urllist(list)

            if keyurl is not None:
                process_keyurl(keyurl)

    for url in urllist:
        print url, "root url"

        urlinfo = gethtml.process_url(url)

        if urlinfo is None or isinstance(urlinfo, str):
            print "error root url",url, urlinfo
            continue

        list, keyurl = urlinfo

        try:
            process_urllist(list)
            process_keyurl(keyurl)

        except:
            import traceback
            traceback.print_exc()

urllist = ["http://www.xitek.com",
           "http://www.zol.com.cn",
           "http://www.weiqiok.com",
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
           "http://www.baidu.com",
           "http://www.jd.com",
           "http://www.google.com",
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