#-*- coding=utf-8 -*-
import requests
import re
import os
#����

jwgl_url = "http://jwgl.hunnu.edu.cn/"
user = 'user'
password = 'pd'
year = '2016-2017'
term='1'

def vs(text):
	'''ץȡ��½ҳ���viewstateֵ��post������ϸ�ֵ��������������֤'''
	viewstate = re.findall(r'<input[^>]*name=\"__VIEWSTATE\"[^>]*value=\"([^"]*)\"[^>]*>',text)
	return viewstate[0]

def getscore(url, text, year, term):
	'''url�����½ҳ��ģ������滻���¹����ѯ��url'''
	mlink = re.findall(r'xscj_gc.aspx\?xh=\d+&xm=[^&]+&gnmkdm=N121605',text)
	path = re.findall(r'http://[^/]+/\([^)]+\)/', url)
	fdurl = path[0] + mlink[0]
	header = {'Host': 'jwgl.hunnu.edu.cn',
	'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.34 Safari/537.36",
	'Referer': url}
	r = requests.get(fdurl,headers=header)
	#��ת����ѯҳ�棬׼���ύ��ѯ����
	postData = {'__VIEWSTATE': vs(r.text), 'ddlXN':year,'ddlXQ':term,'Button1':'%B0%B4%D1%A7%C6%DA%B2%E9%D1%AF'}
	r2 = requests.post(r.url, data=postData ,headers=header)
	r2.encoding = "gbk"
	tables = re.findall(r'<table.*?</table>',r2.text,re.S)
	return tables
	#tables�ֱ��ǳɼ����������Ͳ����ɼ�

def printscore(table, column):
	info = re.findall(r'<td>(.*?)</td>',table)
	first,least = 0,column
	while least <= len(info):
		print (info[first:least])
		print ()
		first = least
		least = least+column

r = requests.get(jwgl_url)
#ץȡ��½ҳ���viewstateֵ��post������ϸ�ֵ
postData = {'__VIEWSTATE': vs(r.text), 'TextBox1': user,'TextBox2': password, 'TextBox3':'','RadioButtonList1':'%D1%A7%C9%FA','Button1':'','lbLanguage':''}
header = {'Host': 'jwgl.hunnu.edu.cn',
'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.34 Safari/537.36",
'Referer': r.url}
r2 = requests.post(r.url, data=postData ,headers=header)
#���첢��post
tables = getscore(r2.url, r2.text, year, term)
print ("�ɼ�")
printscore (tables[0],15)
print "����"��
printscore (tables[2],5)