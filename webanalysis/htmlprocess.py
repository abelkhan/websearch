# -*- coding: UTF-8 -*-
# htmlprocess
# create at 2016/2/25
# autor: qianqians

import HTMLParser
import chardet
from doclex import doclex

def judged_url(url):
    if url is None or url.find('http') != 0:
        return False
    return True

def ingoreurl(url):
    count = 0
    for ch in url:
        if ch == '/':
            count += 1

    return count > 4

class htmlprocess(HTMLParser.HTMLParser):
    def __init__(self, urlinfo):
        HTMLParser.HTMLParser.__init__(self)

        self.urllist = {}
        self.sub_url = ""

        self.urlinfo = urlinfo
        self.current_url = urlinfo['url']

        keywords = doclex.simplesplit(self.current_url)
        for key in keywords:
            self.urlinfo['keys']['1'].append(key)

        self.current_tag = ""
        self.style = ""

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        self.style = 'None'
        self.sub_url = ""

        if tag == 'meta':
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
                        if isinstance(keywords, list):
                            for key in keywords:
                                self.urlinfo['keys']['1'].append(key)
                    elif self.style == 'profile':
                        self.urlinfo['profile']['0'] = value

                    encodingdate = chardet.detect(value)
                    if encodingdate['encoding']:
                        udata = unicode(value, encodingdate['encoding'])
                        tlen = 16
                        if len(udata) < 16:
                            tlen = len(udata)
                        self.urlinfo['titlegen'].append(udata[0:tlen].encode('utf-8'))
                    else:
                        self.urlinfo['titlegen'].append(value)

        if tag == 'a':
            self.sub_url = ""
            for name,value in attrs:
                if name == 'href':
                    if len(value) == 0:
                        return

                    if not judged_url(value):
                        if self.current_url[len(self.current_url) - 1] != '/' and value[0] != '/':
                            value = self.current_url + '/' + value
                        else:
                            value = self.current_url + value

                    if value.find('javascript') != -1:
                        return

                    if value.find('javaScript') != -1:
                        return

                    if self.current_url.find("apple") != -1:
                        if value.find("http://www.apple.com/cn/mac#ac-gn-menustate") !=-1:
                            return

                    if self.current_url.find("cnblogs") != -1:
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

                    if self.current_url.find(value) != -1:
                        return

                    if value[len(value) - 1] == '#':
                        value = value[0:-1]

                    if value != self.current_url and len(value) < 64 and not ingoreurl(value):
                        self.urllist[value] = {'url':value, 'keys':{'1':[], '2':[], '3':[]}, 'title':'', 'titlegen':[], 'profile':{'0':'', '1':'', '2':[]}}
                        self.sub_url = value

    def handle_data(self, data):
        if self.current_tag == 'title':
            try:
                data = doclex.delspace(data)
                keys = doclex.lex(data)
                if isinstance(keys, list) and len(keys) > 0:
                    for key in keys:
                        self.urlinfo['keys']['2'].append(key)
                if len(data) > 0:
                    self.urlinfo['title'] = data
            except:
                import traceback
                traceback.print_exc()

        elif self.current_tag == 'a':
            try:
                if self.sub_url != "":
                    keys = doclex.simplesplit(data)
                    if isinstance(keys, list) and len(keys) > 0:
                        for key in keys:
                            if key in self.urllist[self.sub_url]['keys']['3']:
                                self.urllist[self.sub_url]['keys']['3'].remove(key)
                            if key not in self.urllist[self.sub_url]['keys']['1'] and key not in self.urllist[self.sub_url]['keys']['2']:
                                self.urllist[self.sub_url]['keys']['2'].append(key)

                    encodingdate = chardet.detect(data)
                    if encodingdate['encoding']:
                        udata = unicode(data, encodingdate['encoding'])
                        tlen = 16
                        if len(udata) < 16:
                            tlen = len(udata)
                        self.urllist[self.sub_url]['titlegen'].append(udata[0:tlen].encode('utf-8'))
                        if len(udata) > 16:
                            self.urllist[self.sub_url]['profile']['1'] = udata[0:32].encode('utf-8')

            except:
                import traceback
                traceback.print_exc()
        else:
            if self.current_tag == 'p' or self.current_tag == 'div':
                try:
                    if not doclex.invialddata(data):
                        data = doclex.delspace(data)

                        encodingdate = chardet.detect(data)
                        udata = unicode(data, encodingdate['encoding'])
                        tlen = 16
                        if len(udata) < 16:
                            tlen = len(udata)
                        self.urlinfo['titlegen'].append(udata[0:tlen].encode('utf-8'))

                        if len(udata) > 32:
                            self.urlinfo['profile']['2'].append((udata[0:32] + u"...").encode('utf-8'))

                        keys1 = doclex.lex(data)
                        for key in keys1:
                            self.urlinfo['keys']['3'].append(key)

                except:
                    import traceback
                    traceback.print_exc()