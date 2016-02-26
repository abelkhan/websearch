# -*- coding: UTF-8 -*-
# webanalysis
# create at 2016/2/25
# autor: qianqians

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import urllib2
import cookielib
import time
import chardet
from doclex import doclex
from htmlprocess import htmlprocess

collection_url_index = None
collection_url_profile = None

def get_page(url):
    try:
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240',
                   'Connection':'Keep-Alive',
                   'Accept':'text/html, application/xhtml+xml, image/jxr, */*',
                   'Accept-Language':'zh-Hans-CN,zh-Hans;q=0.8,en-US;q=0.5,en;q=0.3',
                   }

        cookie_jar = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar))
        req = urllib2.Request(url = url, headers = headers)
        response = opener.open(req)
        the_page = response.read()
        headers = response.info()

        return the_page, headers
    except:
        import traceback
        traceback.print_exc()

processed_url_list = []

def process_url(urlinfo):
    url = urlinfo['url']

    if url in processed_url_list:
        return "url is be processed"

    processed_url_list.append(url)

    print url,"process url"

    info = get_page(url)
    if info is None:
        print "url, error"
        return

    data, headers = info

    try:
        htmlp = htmlprocess(urlinfo)
        htmlp.feed(data)

        urlinfo = htmlp.urlinfo

        encodingdate = chardet.detect(headers['date'])
        date = unicode(headers['date'], encodingdate['encoding'])

        title = urlinfo['title']
        if title == "":
            if len(urlinfo['titlegen']) > 0:
                title = urlinfo['titlegen']

        profile = urlinfo['profile']['0']
        if profile == "":
            profile = urlinfo['profile']['1']
        if profile == "":
            if len(urlinfo['profile']['2']) > 0:
                profile = urlinfo['profile']['2'][0]

        if title != "" and profile != "":
            encodingdate = chardet.detect(profile)
            profile = unicode(profile, encodingdate['encoding'])
            collection_url_profile.update({'key':url} , {'key':url, 'urlprofile':profile.encode('utf-8'), 'timetmp':time.time(), 'date':date, 'title':title}, True)

        for w in ['1', '2', '3']:
            keywords = urlinfo['keys'][w]

            for key1 in keywords:
                key = doclex.tolower(key1)
                collection_url_index.update({'key':key, 'url':url}, {'$set':{'key':key, 'url':url, 'timetmp':time.time(), 'weight':int(w), 'userchose':0}}, True)

        urlinfolist = htmlp.urllist
        for key, info in urlinfolist.iteritems():
            process_url(info)
            urlinfolist[key] = {}

    except:
            import traceback
            traceback.print_exc()

def seach(urllist):
    processed_url_list = []

    for url in urllist:
        try:
            print url, "root url"
            process_url({'url':url, 'keys':{'1':[], '2':[], '3':[]}, 'title':'', 'titlegen':[], 'profile':{'0':'', '1':'', '2':[]}})

        except:
            import traceback
            traceback.print_exc()