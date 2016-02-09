# -*- coding: UTF-8 -*-
# darkforce
# create at 2015/10/11
# autor: qianqians

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import urllib2
import cookielib
import HTMLParser
from doclex import doclex
import time
import pymongo
import chardet

collection = None
collection_url_profile = None
collection_url_title = None

def judged_url(url):
    if url is None or url.find('http') != 0:
        return False
    return True

class htmlprocess(HTMLParser.HTMLParser):
    def __init__(self, url):
        self.link = []
        self.data = []
        self.key_url = {}

        self.url = url
        self.link_url = ""

        self.keywords = []
        self.profile = ""

        self.title = ""

        self.current_tag = ""

        self.style = ""

        HTMLParser.HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        self.style = 'None'

        if tag == 'a':
            for name,value in attrs:
                if name == 'href':
                    self.link_url = ""
                    if len(value) == 0:
                        return

                    if not judged_url(value):
                        if self.url[len(self.url) - 1] != '/' and value[0] != '/':
                            value = self.url + '/' + value
                        else:
                            value = self.url + value

                    if value.find('javascript') != -1:
                        return

                    if value.find('javaScript') != -1:
                        return

                    if self.url.find("apple") != -1:
                        if value.find("http://www.apple.com/cn/mac#ac-gn-menustate") !=-1:
                            return

                    if self.url.find("cnblogs") != -1:
                        if value.find("http://msg.cnblogs.com/send?recipient=itwriter") != -1:
                            return
                        elif value.find("http://i.cnblogs.com/EditPosts.aspx?opt=1") != -1:
                            return
                        elif value.find("http://i.cnblogs.com/EditPosts.aspx?postid=1935371") != -1:
                            return
                        elif value.find("http://msg.cnblogs.com/send?recipient=itwriter/") != -1:
                            return
                        elif value.find("http://msg.cnblogs.com/send?recipient=itwriter/GetUsername.aspx") != -1:
                            return
                        elif value.find("/EnterMyBlog.aspx?NewArticle=1") != -1:
                            return
                        elif value.find("GetUsername") != -1:
                            return
                        elif value.find("GetMyPassword") != -1:
                            return
                        elif value.find("http://i.cnblogs.com/EditPosts.aspx?postid=") != -1:
                            return
                        elif value[len(value) - 1] == '#':
                            value = value[0:-1]

                    if self.url.find(value) != -1:
                        return

                    if value[len(value) - 1] == '#':
                        value = value[0:-1]

                    self.link_url = value
                    if self.link_url != self.url:
                        self.link.append(value)

        elif tag == 'meta':
            for name,value in attrs:
                if name == 'name':
                    if value == 'keywords' or value == 'metaKeywords':
                        self.style = 'keywords'
                    elif value == 'description' or value == 'metaDescription':
                        self.style = 'profile'
            for name,value in attrs:
                if name == 'content':
                    if self.style == 'keywords':
                        keywords = doclex.simplesplit(value)
                        for key in keywords:
                            self.keywords.append((key, 1))
                    elif self.style == 'profile':
                        self.profile = value

    def handle_data(self, data):
        if self.current_tag == 'title':
            try:
                data = doclex.delspace(data)
                keys = doclex.lex(data)
                if isinstance(keys, list) and len(keys) > 0:
                    for key in keys:
                        self.keywords.append((key, 2))
                if len(data) > 0:
                    self.title = data
            except:
                import traceback
                traceback.print_exc()
        elif self.current_tag == 'a':
            try:
                data = doclex.delspace(data)
                keys = doclex.simplesplit(data)
                if isinstance(keys, list) and len(keys) > 0:
                    for key in keys:
                        if not self.key_url.has_key(key):
                            self.key_url[key] = []
                        if self.link_url != self.url and judged_url(self.link_url):
                            self.key_url[key].append(self.link_url)
            except:
                import traceback
                traceback.print_exc()
        else:
            if self.current_tag == 'p' or self.current_tag == 'div':
                try:
                    data = doclex.delspace(data)
                    self.data.append(data)
                except:
                    import traceback
                    traceback.print_exc()

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

process_url_list = []

def process_url(url):
    if url in process_url_list:
        return "url is be processed"

    process_url_list.append(url)

    print url,"process url"

    info = get_page(url)
    if info is None:
        print "url, error"
        return

    data, headers = info

    pageinfo = process_page(url, data)

    if pageinfo is None:
        print "url, process_page error"
        return

    link_list, url_profile, keywords, profile, key_url, title = pageinfo

    try:
        encodingdate = chardet.detect(headers['date'])
        date = unicode(headers['date'], encodingdate['encoding'])

        try:
            if doclex.isinviald(profile):
                profile = url_profile
                if not doclex.isinviald(profile):
                    encoding = chardet.detect(profile)
                    if encoding['encoding'] is None:
                        try:
                            profile = unicode(profile, "utf-8")
                        except:
                            profile = unicode(profile, "ascii")
                        finally:
                            import traceback
                            traceback.print_exc()
                    else:
                        profile = unicode(profile, encoding['encoding'])
            if doclex.isinviald(title):
                lent = 10
                if len(profile) < 10:
                    lent = len(profile)
                title = profile[0: lent] + "..."
            encodingdate = chardet.detect(title)
            if encodingdate['encoding']:
                title = unicode(title, encodingdate['encoding'])
            else:
                title = unicode(title, 'utf-8')

            title = title.encode('utf-8', 'ignore')
            profile = profile.encode('utf-8', 'ignore')

            title = doclex.delspace(title)
            profile = doclex.delspace(profile)

            if not doclex.isinviald(profile):
                collection_url_profile.update({'key':url} , {'key':url, 'urlprofile':profile, 'timetmp':time.time(), 'date':date, 'title':title}, True)
            else:
                if not doclex.isinviald(title):
                    collection_url_profile.update({'key':url} , {'key':url, 'urlprofile':title, 'timetmp':time.time(), 'date':date, 'title':title}, True)
        except:
            import traceback
            traceback.print_exc()

        for key1 in keywords:
            key = ""
            for c in key1[0]:
                if c >= 'A' and c <= 'Z':
                    c = c.lower()
                key += c
            try:
                if isinstance(key, str):
                    encodingdate = chardet.detect(key)
                    if encodingdate['encoding']:
                        key = unicode(key, encodingdate['encoding'])
                    else:
                        key = unicode(key, 'utf-8')
                elif isinstance(key, unicode):
                    key = key.encode("utf-8")
                collection.update({'key':key, 'url':url}, {'$set':{'key':key, 'url':url, 'timetmp':time.time(), 'weight':key1[1]}}, True)
            except:
                import traceback
                traceback.print_exc()
    except:
        import traceback
        traceback.print_exc()

    return link_list, key_url

def process_page(url, data):
    if data is None:
        return

    try:
        keywords = []
        key_url = {}
        url_profile = ""

        htmlp = htmlprocess(url)
        htmlp.feed(data)

        keywords.extend(htmlp.keywords)
        key_url.update(htmlp.key_url)

        if len(key_url) > 0:
            for key, value in key_url.iteritems():
                if len(value) > 0:
                    urllist = []
                    urllist = [url for url in value if urllist.count(url) == 0]
                    if url not in key_url[key]:
                        key_url[key] = urllist

        for data in htmlp.data:
            data = doclex.delspace(data)
            if len(data) < 32:
                url_profile += data
                keys = doclex.simplesplit(data)
                if isinstance(keys, list) and len(keys) > 0:
                    for key in keys:
                        keywords.append((key, 3))
            else:
                if len(data) > 100:
                    url_profile += data[0:len(data) if len(data) < 100 else 100] + "..."
                keys1 = doclex.lex(data)
                for key in keys1:
                    keywords.append((key, 3))

        keys = doclex.simplesplit(url)
        if isinstance(keys, list) and len(keys) > 0:
            for key in keys:
                keywords.append((key, 1))

        return htmlp.link, url_profile, keywords, htmlp.profile, key_url, htmlp.title

    except:
        import traceback
        traceback.print_exc()

