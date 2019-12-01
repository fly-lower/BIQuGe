import requests
import threading
from threading import Thread

from lxml import etree
from db_link import RedisClient as RD
from db_link import MongoClient as MG
from settings import *
from tools import *

class BiQuGe(Thread):
	def __init__(self,chapter_job=None,job=None,kk=None):
		'''

		:param chapter_job:
		:param job: 书名
		:param kk:
		'''
		self.chapter_job = chapter_job
		self.kk=kk
		self.db  = RD()
		super().__init__()
		self.job=job
		self.headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
		}
		if not self.job:
			self.books('http://www.xbiquge.la/xiaoshuodaquan/')
		if self.job:
			# print('开工了')
			self.chapters(self.job[0])


	def chapters(self,title_url):
		print('书名：',self.job[1],'\n')
		response = requests.get(title_url,headers = self.headers)
		response.encoding='utf-8'
		html = etree.HTML(response.text)
		chapter_urls = html.xpath('//div[@id="list"]/dl/dd/a/@href')
		chapter_urls = ['http://www.xbiquge.la'+i for i in chapter_urls]
		hash_urls = [MD5(i) for i in chapter_urls]
		chapter_titles = html.xpath('//div[@id="list"]/dl/dd/a/text()')
		chapters = zip(chapter_titles,chapter_urls,hash_urls)
		for i in enumerate(chapters):
			if len(i)==2:
				self.db.put_task(self.job[1],i)


	def content(self,chapter_job):
		index,(title,url,hash_url) = chapter_job
		try:
			response = requests.get ( url, headers=self.headers )
			response.encoding = 'utf-8'
			html = etree.HTML ( response.text )
			contents=html.xpath('//div[@id="content"]/text()')
			content = ''.join([i.strip() for i in contents])
			print ('%s：%s'%(self.job[1],title) )
			mg = MG(MONGO_DB,self.job[1])
			mg.table.update({'hash_url':hash_url},{'$set':{'title':title,'index':index,'content':content}},upsert=True)
		except:
			print('%s内容失败，存入任务列表'%title)
			self.db.put_task(self.job[1],chapter_job)
		# 放入失败的章节

	def books(self,main_url):
		response = requests.get(main_url,headers = self.headers)
		res = etree.HTML(response.text)
		books_url = res.xpath('//div[@id="main"]/div/ul/li/a/@href')
		books_title = res.xpath('//div[@id="main"]/div/ul/li/a/text()')
		# print(books_title)
		books = zip(books_url,books_title)
		for i in books:
			if len(i)==2:
				self.db.put_task('BOOK_LIST',i)

	def run(self):
		while True:
			chapter = self.db.get_task(self.job[1])
			if not chapter:
				break
			self.content(chapter)
		print('一个线程结束')


if __name__ == '__main__':
	# main_url = 'http://www.xbiquge.la/xiaoshuodaquan/'
	bqg = BiQuGe()
	# bqg.chapters("http://www.xbiquge.la/9/9795/")
	# bqg.content("http://www.xbiquge.la/9/9795/4308760.html")