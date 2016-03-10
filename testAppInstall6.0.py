#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import commands
import re

dic_stat = {}
dic_str = {}
succ_app = 0
fail_app = 0

def files(rootDir):
	files = []
	for lists in os.listdir(rootDir):
		path = os.path.join(lists)
		files.append(path)
	return files

def finds(b):
	pattern = re.compile("\[(.*?)\]")
	match = pattern.search(b)
	if match:
		return match.group()
	else:
		return "Nothing"
		
def getp(b):
	pattern = re.compile(r"'(.*?)'")
	match = pattern.search(b)
	if match:
		res = match.group()
	else:
		return "Nothing"
	pattern = re.compile(r"\w[A-Z0-9a-z.]*")
	match = pattern.search(res)
	if match:
		return match.group()
	else:
		return "Nothing"

temp = files('./test')

for each in temp:
	path = 'adb install ./test/' + each
	print "Installing " + each + "...",
	a,b = commands.getstatusoutput(path)
	if a != 0:
		dic_stat[each] = 'fail'
		dic_str[each] = finds(b)
		print ", fail"
		fail_app += 1
		continue
	if 'Failure' in b:
		dic_stat[each] = 'fail'
		dic_str[each] = finds(b)
		print ", fail"
		fail_app += 1
		continue
	else:
		dic_stat[each] = 'succ'
		dic_str[each] = ''
		print ", success"
		succ_app += 1
	
	cmd = 'aapt dump badging ./test/' + each
	c,d = commands.getstatusoutput(cmd)
	package = getp(d)
	cmd = 'adb uninstall ' + package
	print 'uninstalling ' + each + ' ...'
	c,d = commands.getstatusoutput(cmd)

f1 = open("stat.log","wb")
f1.write("success : " + str(succ_app) + "\tFailure : " + str(fail_app) + "\n")
for i in dic_stat:
	f1.write(i + " : " + dic_stat[i] + ' : ' + dic_str[i] + '\n')
f1.close()

print "success : " + str(succ_app) + "\tFailure : " + str(fail_app)


