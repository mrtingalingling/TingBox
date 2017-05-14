#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Author: Ting
web_text clean up'''
import re 


def visible(element):
	if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
		return False
	elif re.match('<!--.*-->'.encode('utf-8'), element.encode('utf-8')):
		return False
	return True

def text_content_clean(content): 
	if re.match('\n'.encode('utf-8'), content.encode('utf-8')):
		return False
	return True

def printthis(): 
	print 'Import works!!!' 
	