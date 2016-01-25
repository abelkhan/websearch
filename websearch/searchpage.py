# -*- coding: UTF-8 -*-
# usesearch
# create at 2015/10/31
# autor: qianqians
import sys
sys.path.append('../')
from plask import *
from loginui import *
import pymongo
import usesearch
import globalv
from webget import gethtml

def add_title():
    code = "\nvar board = document.getElementById(\"search_output_1\");\n"
    code += "for(var i in value['urllist']){\n"
    code += "   var url = value['urllist'][i];"
    code += "   var dc = document.createElement(\"div\");\n"
    code += "   dc.style.margin = \"20px 0px 20px 0px\";\n"
    code += "   dc.style.clear = \"both\";\n"
    code += "   var d = document.createElement(\"a\");\n"
    code += "   d.innerHTML = url[\"title\"];"
    code += "   d.href = url[\"url\"];"
    code += "   d.style.fontSize = \"120%\";\n"
    code += "   var dt = document.createElement(\"div\");\n"
    code += "   var textnode=document.createTextNode(url[\"profile\"]);\n"
    code += "   dt.appendChild(textnode);\n"
    code += "   dt.style.fontSize = \"100%\";\n"
    code += "   var dz = document.createElement(\"div\");\n"
    code += "   dz.style.fontSize = \"80%\";\n"
    code += "   dz.style.cssFloat=\"left\";\n"
    code += "   dz.setAttribute(\"url_id\",url[\"url\"]);\n"
    code += "   var textnode=document.createTextNode(url[\"url\"]);\n"
    code += "   dz.appendChild(textnode);\n"
    code += "   var textnode=document.createTextNode('      ');\n"
    code += "   dz.appendChild(textnode);\n"
    code += "   var textnode=document.createTextNode(url[\"date\"]);\n"
    code += "   dz.appendChild(textnode);\n"
    code += "   dc.appendChild(d);\n"
    code += "   dc.appendChild(dt);\n"
    code += "   dc.appendChild(dz);\n"
    code += "   board.appendChild(dc);\n"
    code += "}"

    return code

def add_title1():
    code = "\nvar board = document.getElementById(\"search_output_1\");\n"
    code += "var obj = board.childNodes;\n"
    code += "for(var i = 3; obj.length > 3;){\n"
    code += "   board.removeChild(obj[i]);"
    code += "}\n"
    code += "for(var i in value['urllist']){\n"
    code += "   var url = value['urllist'][i];"
    code += "   var dc = document.createElement(\"div\");\n"
    code += "   dc.style.margin = \"20px 0px 20px 0px\";\n"
    code += "   dc.style.clear = \"both\";\n"
    code += "   var d = document.createElement(\"a\");\n"
    code += "   d.innerHTML = url[\"title\"];"
    code += "   d.href = url[\"url\"];"
    code += "   d.style.fontSize = \"120%\";\n"
    code += "   var dt = document.createElement(\"div\");\n"
    code += "   var textnode=document.createTextNode(url[\"profile\"]);\n"
    code += "   dt.appendChild(textnode);\n"
    code += "   dt.style.fontSize = \"100%\";\n"
    code += "   var dz = document.createElement(\"div\");\n"
    code += "   dz.style.fontSize = \"80%\";\n"
    code += "   dz.style.cssFloat=\"left\";\n"
    code += "   dz.setAttribute(\"url_id\",url[\"url\"]);\n"
    code += "   var textnode=document.createTextNode(url[\"url\"]);\n"
    code += "   dz.appendChild(textnode);\n"
    code += "   var textnode=document.createTextNode('      ');\n"
    code += "   dz.appendChild(textnode);\n"
    code += "   var textnode=document.createTextNode(url[\"date\"]);\n"
    code += "   dz.appendChild(textnode);\n"
    code += "   dc.appendChild(d);\n"
    code += "   dc.appendChild(dt);\n"
    code += "   dc.appendChild(dz);\n"
    code += "   board.appendChild(dc);\n"
    code += "}"

    return code

def on_search(p):
    try:
        return {"urllist":usesearch.find_page(p['input'], p['index'])}
    except:
        return {}

def layout():
    app = plaskapp('0.0.0.0', 80)

    p = pypage('websearch', globalv.urlname, pyhtmlstyle.margin_auto)
    p.add_page_route('/')

    cb = pycontainer('cb', pyhtmlstyle.float_left, p)
    cb.set_size(1000, 0)
    cb.set_location(0, 0)

    mj = pycontainer('mj', pyhtmlstyle.float_left, p)
    #mj.set_location(1110, 1)
    mj.top = 60
    mj.left = 70
    mj.set_size(400, 0)

    pnotes = pytext("Abelkhan", "notes123", pyhtmlstyle.margin_auto, mj)
    pnotes.set_font_size(200)
    pnotes = pytext("开源网页搜索引擎，致力于为用户提供优秀的搜索体验。", "notes1234", pyhtmlstyle.margin_auto, mj)
    pnotes.top = 3
    pnotes = pytext("项目托管地址:", "notes12345", pyhtmlstyle.margin_auto, mj)
    pnotes.top = 20
    plink = pylink("https://github.com/abelkhan/websearch.git", "https://github.com/abelkhan/websearch.git", "link1", pyhtmlstyle.margin_auto, mj)
    plink.top = 3
    pnotes = pytext("作者: 吴 铭 ", "notes123456", pyhtmlstyle.margin_auto, mj)
    pnotes.top = 20
    pnotes = pytext("手机: 15618972863", "notes1234568", pyhtmlstyle.margin_auto, mj)
    pnotes.top = 3
    pnotes = pytext("QQ: 451517996", "notes1234567", pyhtmlstyle.margin_auto, mj)
    pnotes.top = 3

    titleui(cb)

    b = pycontainer('search_output', pyhtmlstyle.margin_auto, cb)
    b.set_visibility(False)
    b.set_location(10, 10)
    b.set_size(1000, 0)

    c = pycontainer('title_input12', pyhtmlstyle.margin_auto, cb)
    c.set_location(120, 160)
    b.set_newline()

    pnotes = pytext("千度又如何", "notes12", pyhtmlstyle.margin_auto, c)
    pnotes.set_font_size(200)
    #pnotes.set_location(10, 30)
    pnotes.set_font_color((100, 100, 200))
    pnotes.left = 11
    pnotes.bottom = 3
    titletitle = pyedit('title_edit', pyedit.text, pyhtmlstyle.float_left, c)
    titletitle.set_size(300, 24)
    titletitle.set_location(10, 0)
    button = pybutton('千度吧', 'button', pyhtmlstyle.float_left, c)
    button.set_size(80, 30)
    button.set_location(3, 0)
    ev = uievent(globalv.urlname, button, pyelement.onclick)
    params = jparams()
    params.append("input", titletitle.client_get_input_text())
    params.append("index", '0')
    onsev = on_server_response()
    sev = server_event("submit", params, onsev)
    onsev.add_call(c.server_set_visible(False))
    onsev.add_call(b.server_set_visible(True))
    onsev.add_call(add_title())
    sev.add_onevent(on_search)
    ev.add_server_event(sev)
    button.register_uievent(ev)

    pnotes = pytext("千度又如何", "notes1", pyhtmlstyle.float_left, b)
    pnotes.set_font_size(165)
    pnotes.set_font_color((100, 100, 200))
    pnotes.set_size(0, 24)
    pnotes.right = 10
    pnotes.set_visibility(False)
    titletitle = pyedit('title_edit1', pyedit.text, pyhtmlstyle.float_left, b)
    titletitle.set_size(300, 24)
    titletitle.set_visibility(False)
    button = pybutton('千度吧', 'button1', pyhtmlstyle.float_left, b)
    button.set_size(80, 30)
    button.bottom = 40
    button.set_visibility(False)
    ev = uievent(globalv.urlname, button, pyelement.onclick)
    params = jparams()
    params.append("input", titletitle.client_get_input_text())
    params.append("index", '0')
    onsev = on_server_response()
    sev = server_event("submit", params, onsev)
    onsev.add_call(add_title1())
    sev.add_onevent(on_search)
    ev.add_server_event(sev)
    button.register_uievent(ev)

    p.init()

    app.run()


if __name__ == '__main__':
    conn = pymongo.Connection('localhost',27017)
    db = conn.webseach
    usesearch.collection_page = db.webpage
    usesearch.collection_key = db.keys

    globalv.collection_user = db.user
    globalv.collection_file = db.file
    globalv.collection_text = db.text

    print usesearch.collection_page,usesearch.collection_key
    gethtml.collection = db.webpage
    gethtml.collection_url_profile = db.urlprofile
    gethtml.collection_url_title = db.urltitle

    layout()