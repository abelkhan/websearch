# -*- coding: UTF-8 -*-
# webseach
# create at 2015/10/30
# autor: qianqians

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

sys.path.append('../')

import pymongo
import time
from doclex import doclex
from webanalysis import webanalysis

collection_key = None

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
    webanalysis.collection_url_index = db.webpage
    webanalysis.collection_url_profile = db.urlprofile
    collection_key = db.keys

    t = 0
    while True:
        timetmp = time.time()-t
        if timetmp > 86400:
            refkeywords()
            t = time.time()
        webanalysis.seach(urllist)