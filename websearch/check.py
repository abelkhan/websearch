# -*- coding: UTF-8 -*-
# darkforce
# create at 2015/9/29
# autor: qianqians
import random

def num_to_check(num):
	if num == 0:
		return "零"
	if num == 1:
		return "壹"
	if num == 2:
		return "贰"
	if num == 3:
		return "叁"
	if num == 4:
		return "肆"
	if num == 5:
		return "伍"
	if num == 6:
		return "陆"
	if num == 7:
		return "柒"
	if num == 8:
		return "捌"
	if num == 9:
		return "玖"

def random_check():
	num = random.randint(0, 9999)
	text =  num_to_check(num/1000)
	text += num_to_check((num%1000)/100)
	text += num_to_check((num%100)/10)
	text += num_to_check(num%10)
	return num, text

def check_num(num, numcheck):
	return num == numcheck

def check_text(text, textcheck):
	return text == textcheck