# -*- coding: UTF-8 -*-
# darkforce
# create at 2015/9/28
# autor: qianqians
import sys
sys.path.append('../')
from plask import *
from check import *
from login import *
import globalv

def on_get_check(p):
	num,text = random_check()
	print pysession.session
	csession = pysession.session[p["sid"]]
	csession["login_check"] = num
	return {"check":text}

def on_check(p):
	text = p["checktext"]
	name = p["name"]
	key = p["key"]
	csession = pysession.session[p["sid"]]
	if not check_num(csession["login_check"], int(text)):
		print "checkend", csession["login_check"], text
		return {"checkend":False}

	c = find_user(name)
	if (c == None):
		print "userisnotdefine"
		return {"userisnotdefine":True}

	return {"loginend":longin_user(c, name, key)}

def on_register(p):
	text = p["checktext"]
	name = p["name"]
	key = p["key"]
	csession = pysession.session[p["sid"]]
	print type(csession["login_check"]), type(text)
	if not check_num(csession["login_check"], int(text)):
		return {"checkend":False}
	print "check true", csession["login_check"], text

	regend = register_user(name, key)
	print regend

	return {"registerend":regend}

def titleui(p):
	b = pycontainer('title1', pyhtmlstyle.margin_auto, p)
	b.set_location(1, 1)

	title1 = registerbtn(b)
	evc = uievent(globalv.urlname, title1, pyelement.onclick)
	popreg = rgisterui(p)
	params = jparams()
	onsev = on_server_response()
	sev = server_event("callregister", params, onsev)
	sev.add_onevent(on_get_check)
	onsev.add_call(close_pop())
	onsev.add_call(popreg.client_call())
	evc.add_server_event(sev)
	title1.register_uievent(evc)

	title2 = loginbtn(b)
	evc = uievent(globalv.urlname, title2, pyelement.onclick)
	pop = loginui(p, title1, title2)
	params = jparams()
	onsev = on_server_response()
	sev = server_event("calllogin", params, onsev)
	sev.add_onevent(on_get_check)
	onsev.add_call(close_pop())
	onsev.add_call(pop.client_call())
	evc.add_server_event(sev)
	title2.register_uievent(evc)

def registerbtn(b):
	title1 = pytext("&nbsp;注册", "title3", pyhtmlstyle.float_right, b)
	title1.set_font_color((122,122,152))
	ev = uievent(globalv.urlname, title1, pyelement.onmouseover)
	ev.add_call_ui(title1.client_set_font_color((0,0,250)))
	ev.add_call_ui(title1.client_set_cursor(pyhtmlstyle.pointer))
	title1.register_uievent(ev)
	evo = uievent(globalv.urlname, title1, pyelement.onmouseout)
	evo.add_call_ui(title1.client_set_font_color((122,122,152)))
	evo.add_call_ui(title1.client_set_cursor(pyhtmlstyle.auto))
	title1.register_uievent(evo)

	return title1

def loginbtn(b):
	title2 = pytext("登陆&nbsp;", "title4", pyhtmlstyle.float_right, b)
	title2.set_font_color((122,122,152))
	ev = uievent(globalv.urlname, title2, pyelement.onmouseover)
	ev.add_call_ui(title2.client_set_font_color((0,0,250)))
	ev.add_call_ui(title2.client_set_cursor(pyhtmlstyle.pointer))
	ev.add_call_ui(title2.client_set_font_color((0,0,250)))
	title2.register_uievent(ev)
	evo = uievent(globalv.urlname, title2, pyelement.onmouseout)
	evo.add_call_ui(title2.client_set_font_color((122,122,152)))
	evo.add_call_ui(title2.client_set_cursor(pyhtmlstyle.auto))
	title2.register_uievent(evo)

	return title2

def rgisterui(p):
	pop = pypopup("popreg", 400, p)
	ptitle = pytext("用户注册", "userregister", pyhtmlstyle.float_left, pop)
	ptitle.left = 5
	ptitle.top = 5
	ptitle.bottom = 5
	pclose = pytext("×", "closeui", pyhtmlstyle.float_right, pop)
	pclose.top = 5
	pclose.right = 5
	evunselectclose = uievent(globalv.urlname, pclose, pyelement.onmouseout)
	evunselectclose.add_call_ui(pclose.pop_set_cursor(pyhtmlstyle.auto))
	pclose.register_uievent(evunselectclose)
	evselectclose = uievent(globalv.urlname, pclose, pyelement.onmouseover)
	evselectclose.add_call_ui(pclose.pop_set_cursor(pyhtmlstyle.pointer))
	pclose.register_uievent(evselectclose)
	evclose = uievent(globalv.urlname, pclose, pyelement.onclick)
	evclose.add_call_ui(pop.close_win())
	pclose.register_uievent(evclose)

	pc = pycontainer('regusernamec', pyhtmlstyle.margin_auto, pop)
	pc.set_bottom_border_style(pyhtmlstyle.solid)
	pc.set_border_color((150, 150, 150))
	pc.set_border_size(1)
	pc.set_newline()
	ptusername = pytext("用户名:", "regusername", pyhtmlstyle.float_left, pc)
	ptusername.left = 50
	ptusername.top = 12
	ptusername.set_newline()
	ptusernameinput = pyedit("regusernameinput", pyedit.text, pyhtmlstyle.float_left, pc)
	ptusernameinput.top = 10
	ptusernameinput.bottom = 10

	pckey = pycontainer('regusernamekey', pyhtmlstyle.margin_auto, pop)
	pckey.set_top_border_style(pyhtmlstyle.dashed)
	pckey.set_border_color((150, 150, 150))
	pckey.set_border_size(1)
	pckey.set_newline()
	ptusernamekey = pytext("密码:", "reguserkey", pyhtmlstyle.float_left, pckey)
	ptusernamekey.left = 66
	ptusernamekey.top = 12
	ptusernamekey.set_newline()
	ptusernamekeyinput = pyedit("reguserkeyinput", pyedit.password, pyhtmlstyle.float_left, pckey)
	ptusernamekeyinput.top = 10
	ptusernamekeyinput.bottom = 10

	pcrekey = pycontainer('reusernamekey', pyhtmlstyle.margin_auto, pop)
	pcrekey.set_top_border_style(pyhtmlstyle.dashed)
	pcrekey.set_border_color((150, 150, 150))
	pcrekey.set_border_size(1)
	pcrekey.set_newline()
	ptreusernamekey = pytext("确认密码:", "reuserkey", pyhtmlstyle.float_left, pcrekey)
	ptreusernamekey.left = 34
	ptreusernamekey.top = 12
	ptreusernamekey.set_newline()
	ptusernamekeyinput = pyedit("reuserkeyinput", pyedit.password, pyhtmlstyle.float_left, pcrekey)
	ptusernamekeyinput.top = 10
	ptusernamekeyinput.bottom = 10

	pcmail = pycontainer('remail', pyhtmlstyle.margin_auto, pop)
	pcmail.set_top_border_style(pyhtmlstyle.dashed)
	pcmail.set_border_color((150, 150, 150))
	pcmail.set_border_size(1)
	pcmail.set_newline()
	pmail = pytext("邮箱:", "mail", pyhtmlstyle.float_left, pcmail)
	pmail.left = 66
	pmail.top = 12
	pmail.set_newline()
	pmailinput = pyedit("mailinput", pyedit.text, pyhtmlstyle.float_left, pcmail)
	pmailinput.top = 10
	pmailinput.bottom = 10

	pcaptchac = pycontainer('regcaptchac', pyhtmlstyle.margin_auto, pop)
	pcaptchac.set_top_border_style(pyhtmlstyle.dashed)
	pcaptchac.set_border_color((150, 150, 150))
	pcaptchac.set_border_size(1)
	pcaptchac.set_newline()
	pcaptchat = pytext("验证码:", "regcaptcha", pyhtmlstyle.float_left, pcaptchac)
	pcaptchat.left = 50
	pcaptchat.top = 12
	pcaptchat.set_newline()
	pcaptchainput = pyedit("regcaptchainput", pyedit.text, pyhtmlstyle.float_left, pcaptchac)
	pcaptchainput.top = 10
	pchange = pytext("换一个", "regchange", pyhtmlstyle.float_left, pcaptchac)
	pchange.set_font_size(80)
	pchange.left = 5
	pchange.top = 14
	pchange.bottom = 5
	pchange.set_font_color((100, 100, 200))
	pnotes = pytext("请输入下面繁体数字的阿拉伯字符", "regnotes", pyhtmlstyle.float_left, pcaptchac)
	pnotes.set_font_size(60)
	pnotes.set_font_color((100, 100, 100))
	pnotes.left = 108
	pcheck = pydynamictext("check", "regcheck", pyhtmlstyle.float_left, pcaptchac)
	pcheck.set_font_size(160)
	pcheck.set_font_color((100, 100, 200))
	pcheck.top = 5
	pcheck.left = 108
	pcheck.bottom = 10

	evchange = uievent(globalv.urlname, pchange, pyelement.onclick)
	params = jparams()
	onsev = on_server_response()
	sev = server_event("regchangecheck", params, onsev)
	sev.add_onevent(on_get_check)
	onsev.add_call(pcheck.pop_set_text('check'))
	evchange.add_server_event(sev)
	pchange.register_uievent(evchange)

	evunselectchange = uievent(globalv.urlname, pchange, pyelement.onmouseout)
	evunselectchange.add_call_ui(pchange.pop_set_cursor(pyhtmlstyle.auto))
	evunselectchange.add_call_ui(pchange.pop_set_text_decoration(pyhtmlstyle.NoneDecoration))
	pchange.register_uievent(evunselectchange)
	evselectchange = uievent(globalv.urlname, pchange, pyelement.onmouseover)
	evselectchange.add_call_ui(pchange.pop_set_cursor(pyhtmlstyle.pointer))
	evselectchange.add_call_ui(pchange.pop_set_text_decoration(pyhtmlstyle.UnderlineDecoration))
	pchange.register_uievent(evselectchange)

	pcbtn = pycontainer('reusernamelogin', pyhtmlstyle.margin_auto, pop)
	pcbtn.set_top_border_style(pyhtmlstyle.dashed)
	pcbtn.set_border_color((150, 150, 150))
	pcbtn.set_border_size(1)
	pcbtn.set_newline()
	preg = pybutton("注册", "reloginusername", pyhtmlstyle.margin_auto, pcbtn)
	preg.top = 10
	preg.bottom = 5
	preg.left = 160

	evlogin = uievent(globalv.urlname, preg, pyelement.onclick)
	params = jparams()
	params.append("checktext", pcaptchainput.pop_get_input_text())
	params.append("name", ptusernameinput.pop_get_input_text())
	params.append("key", ptusernamekeyinput.pop_get_input_text())
	params.append("mail", pmailinput.pop_get_input_text())
	onsev = on_server_response()
	sev = server_event("register", params, onsev)
	sev.add_onevent(on_register)
	onsev.add_call_if_true(pop.close_win(), "registerend")

	popnotes = pypopup("popnotes", 400, p)
	pclose = pytext("×", "closeui1", pyhtmlstyle.float_right, popnotes)
	pclose.top = 5
	pclose.right = 5
	evunselectclose = uievent(globalv.urlname, pclose, pyelement.onmouseout)
	evunselectclose.add_call_ui(pclose.pop_set_cursor(pyhtmlstyle.auto))
	pclose.register_uievent(evunselectclose)
	evselectclose = uievent(globalv.urlname, pclose, pyelement.onmouseover)
	evselectclose.add_call_ui(pclose.pop_set_cursor(pyhtmlstyle.pointer))
	pclose.register_uievent(evselectclose)
	evclose = uievent(globalv.urlname, pclose, pyelement.onclick)
	evclose.add_call_ui(popnotes.close_win())
	pclose.register_uievent(evclose)
	ptitle = pytext("用户注册", "userregister1", pyhtmlstyle.float_left, popnotes)
	ptitle.left = 5
	ptitle.top = 5
	ptitle.bottom = 5

	onsev.add_call_if_false(msgbox("校验码错误"), "checkend")
	onsev.add_call_if_false(msgbox("用户已被注册"), "registerend")
	evlogin.add_server_event(sev)
	preg.register_uievent(evlogin)

	return pop

def loginui(p, title1, title2):
	pop = pypopup("pop", 400, p)
	ptitle = pytext("用户登陆", "userlogin", pyhtmlstyle.float_left, pop)
	ptitle.left = 5
	ptitle.top = 5
	ptitle.bottom = 5
	pclose = pytext("×", "close", pyhtmlstyle.float_right, pop)
	pclose.top = 5
	pclose.right = 5
	evunselectclose = uievent(globalv.urlname, pclose, pyelement.onmouseout)
	evunselectclose.add_call_ui(pclose.pop_set_cursor(pyhtmlstyle.auto))
	pclose.register_uievent(evunselectclose)
	evselectclose = uievent(globalv.urlname, pclose, pyelement.onmouseover)
	evselectclose.add_call_ui(pclose.pop_set_cursor(pyhtmlstyle.pointer))
	pclose.register_uievent(evselectclose)
	evclose = uievent(globalv.urlname, pclose, pyelement.onclick)
	evclose.add_call_ui(pop.close_win())
	pclose.register_uievent(evclose)
	pc = pycontainer('usernamec', pyhtmlstyle.margin_auto, pop)
	pc.set_bottom_border_style(pyhtmlstyle.solid)
	pc.set_border_color((150, 150, 150))
	pc.set_border_size(1)
	pc.set_newline()
	ptusername = pytext("用户名:", "username", pyhtmlstyle.float_left, pc)
	ptusername.left = 50
	ptusername.top = 12
	ptusername.set_newline()
	ptusernameinput = pyedit("usernameinput", pyedit.text, pyhtmlstyle.float_left, pc)
	ptusernameinput.top = 10
	pregister = pytext("注册", "usernameregister", pyhtmlstyle.float_left, pc)
	pregister.set_font_size(80)
	pregister.left = 5
	pregister.top = 14
	pregister.bottom = 10
	pregister.set_font_color((100, 100, 200))
	evunselectreg = uievent(globalv.urlname, pregister, pyelement.onmouseout)
	evunselectreg.add_call_ui(pregister.pop_set_cursor(pyhtmlstyle.auto))
	evunselectreg.add_call_ui(pregister.pop_set_text_decoration(pyhtmlstyle.NoneDecoration))
	pregister.register_uievent(evunselectreg)
	evselectreg = uievent(globalv.urlname, pregister, pyelement.onmouseover)
	evselectreg.add_call_ui(pregister.pop_set_cursor(pyhtmlstyle.pointer))
	evselectreg.add_call_ui(pregister.pop_set_text_decoration(pyhtmlstyle.UnderlineDecoration))
	pregister.register_uievent(evselectreg)
	pckey = pycontainer('usernamekey', pyhtmlstyle.margin_auto, pop)
	pckey.set_top_border_style(pyhtmlstyle.dashed)
	pckey.set_border_color((150, 150, 150))
	pckey.set_border_size(1)
	pckey.set_newline()
	ptusernamekey = pytext("密码:", "userkey", pyhtmlstyle.float_left, pckey)
	ptusernamekey.left = 66
	ptusernamekey.top = 12
	ptusernamekey.set_newline()
	ptusernamekeyinput = pyedit("userkeyinput", pyedit.password, pyhtmlstyle.float_left, pckey)
	ptusernamekeyinput.top = 10
	pfind = pytext("找回密码", "findusername", pyhtmlstyle.float_left, pckey)
	pfind.set_font_size(80)
	pfind.left = 5
	pfind.top = 14
	pfind.bottom = 10
	pfind.set_font_color((100, 100, 200))
	evunselectfind = uievent(globalv.urlname, pfind, pyelement.onmouseout)
	evunselectfind.add_call_ui(pfind.pop_set_cursor(pyhtmlstyle.auto))
	evunselectfind.add_call_ui(pfind.pop_set_text_decoration(pyhtmlstyle.NoneDecoration))
	pfind.register_uievent(evunselectfind)
	evselectfind = uievent(globalv.urlname, pfind, pyelement.onmouseover)
	evselectfind.add_call_ui(pfind.pop_set_text_decoration(pyhtmlstyle.UnderlineDecoration))
	evselectfind.add_call_ui(pfind.pop_set_cursor(pyhtmlstyle.pointer))
	pfind.register_uievent(evselectfind)

	pcaptchac = pycontainer('captchac', pyhtmlstyle.margin_auto, pop)
	pcaptchac.set_top_border_style(pyhtmlstyle.dashed)
	pcaptchac.set_border_color((150, 150, 150))
	pcaptchac.set_border_size(1)
	pcaptchac.set_newline()
	pcaptchat = pytext("验证码:", "captcha", pyhtmlstyle.float_left, pcaptchac)
	pcaptchat.left = 50
	pcaptchat.top = 12
	pcaptchat.set_newline()
	pcaptchainput = pyedit("captchainput", pyedit.password, pyhtmlstyle.float_left, pcaptchac)
	pcaptchainput.top = 10
	pchange = pytext("换一个", "change", pyhtmlstyle.float_left, pcaptchac)
	pchange.set_font_size(80)
	pchange.left = 5
	pchange.top = 14
	pchange.bottom = 5
	pchange.set_font_color((100, 100, 200))
	pnotes = pytext("请输入下面繁体数字的阿拉伯字符", "notes", pyhtmlstyle.float_left, pcaptchac)
	pnotes.set_font_size(60)
	pnotes.set_font_color((100, 100, 100))
	pnotes.left = 108
	pcheck = pydynamictext("check", "check", pyhtmlstyle.float_left, pcaptchac)
	pcheck.set_font_size(160)
	pcheck.set_font_color((100, 100, 200))
	pcheck.top = 5
	pcheck.left = 108
	pcheck.bottom = 10

	evchange = uievent(globalv.urlname, pchange, pyelement.onclick)
	params = jparams()
	onsev = on_server_response()
	sev = server_event("changecheck", params, onsev)
	sev.add_onevent(on_get_check)
	onsev.add_call(pcheck.pop_set_text('check'))
	evchange.add_server_event(sev)
	pchange.register_uievent(evchange)

	evunselectchange = uievent(globalv.urlname, pchange, pyelement.onmouseout)
	evunselectchange.add_call_ui(pchange.pop_set_cursor(pyhtmlstyle.auto))
	evunselectchange.add_call_ui(pchange.pop_set_text_decoration(pyhtmlstyle.NoneDecoration))
	pchange.register_uievent(evunselectchange)
	evselectchange = uievent(globalv.urlname, pchange, pyelement.onmouseover)
	evselectchange.add_call_ui(pchange.pop_set_cursor(pyhtmlstyle.pointer))
	evselectchange.add_call_ui(pchange.pop_set_text_decoration(pyhtmlstyle.UnderlineDecoration))
	pchange.register_uievent(evselectchange)

	pcbtn = pycontainer('usernamelogin', pyhtmlstyle.margin_auto, pop)
	pcbtn.set_top_border_style(pyhtmlstyle.dashed)
	pcbtn.set_border_color((150, 150, 150))
	pcbtn.set_border_size(1)
	pcbtn.set_newline()
	plogin = pybutton("登录", "loginusername", pyhtmlstyle.margin_auto, pcbtn)
	plogin.top = 10
	plogin.bottom = 5
	plogin.left = 160

	evlogin = uievent(globalv.urlname, plogin, pyelement.onclick)
	params = jparams()
	params.append("checktext", pcaptchainput.pop_get_input_text())
	params.append("name", ptusernameinput.pop_get_input_text())
	params.append("key", ptusernamekeyinput.pop_get_input_text())
	onsev = on_server_response()
	sev = server_event("login", params, onsev)
	sev.add_onevent(on_check)
	onsev.add_call_if_true(pop.close_win(), "loginend")
	onsev.add_call_if_true(title1.server_set_visible(False), "loginend")
	onsev.add_call_if_true(title2.server_set_visible(False), "loginend")
	onsev.add_call_if_false(msgbox("校验码错误"), "checkend")
	onsev.add_call_if_true(msgbox("不存在的用户"), "userisnotdefine")
	onsev.add_call_if_false(msgbox("密码错误"), "loginend")
	evlogin.add_server_event(sev)
	plogin.register_uievent(evlogin)

	return pop