# -*- coding: utf-8 -*-
from selenium import webdriver 
import time
from lxml import etree
import re
import json
import codecs
import random
import requests 
import itertools
import sys 
reload(sys) 
sys.setdefaultencoding( "utf-8" ) 
from fake_useragent import UserAgent
ua = UserAgent()
#存储10个页面链接
url_list = []

info = []
#根据url链接，获取网页源代码，返回网页源码
def get_html(url):
	UA = ua.random
	headers = {'headers':UA}
	html = requests.get(url,headers = headers)
	return html.content
#根据提取到的页面源码，提取详细信息
def get_info(html):
	file = codecs.open("douban250.json",'a',encoding = 'utf-8')
	tree = etree.HTML(html)
	#所有的信息都在class='grid_view'的li标签下。
	lis = tree.xpath("//ol[@class='grid_view']/li")
	#print len(lis)
	for li in lis:
		#电影链接
		link = li.xpath("div/div[2]/div[1]/a/@href")
		#提取电影标题
		titles = li.xpath("div/div[2]/div[1]/a/span/text()")
		s = ' '.join(titles)
		title = s.replace('/','').replace(' ','')
		#电影评分
		grade = li.xpath("div/div[2]/div[2]/div/span[2]/text()")

		#评分人数
		grade_num = li.xpath("div/div[2]/div[2]/div/span[4]/text()")

		#导演#主演
		daoyans = li.xpath("div/div[2]/div[2]/p/text()")
		daoyan = daoyans[0].replace('\t','').replace(' ','').replace('\n','')

		data_country_type = li.xpath("div/div[2]/div[2]/p/text()[2]")
		dct =  data_country_type[0].replace('\t','').replace(' ','').replace('\n','').split('/')
		#上映日期
		data = dct[0].replace(' ','')
		#上映国家
		country = dct[1].replace(' ','')
		#类型
		types = dct[2].replace(' ','')

		dic = {'link':link[0],'title':title,'grade':grade[0],'grade_num':grade_num[0],\
						'daoyan':daoyan,'data':data,'country':country,'type':types}
		i = json.dumps(dict(dic),ensure_ascii=False)
		line = i + '\n'
		file.write(line)			
		info.append(dic)
	return info

#生成10个页面,加入到链接列表
def url_page():
	for i in range(0,226,25):
		url = "https://movie.douban.com/top250?start=" + str(i) +"&filter="
		url_list.append(url)
#主程序
def main():
	url_page()
	#循环遍历列表页，获取详细信息
	for url in url_list:
		html = get_html(url)
		datas = get_info(html)
		print datas
		time.sleep(3)
		
	

if __name__ == '__main__':
	main()

