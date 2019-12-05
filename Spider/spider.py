import re
from threading import Thread

import requests
from BIQuGe.Spider.db_link import MongoClient as MG
from BIQuGe.Spider.db_link import RedisClient as RD
from BIQuGe.Spider.settings import *
from lxml import etree


# from tools import *


class NetError(Exception):
	pass

class ContentError(Exception):
	pass


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
			self.mg = MG(MONGO_DB,self.job[1])


	def chapters(self,title_url):
		'''
		给定书名，获取所有章节名和url，
		检查任务队列中是否存在该书，若有就直接跳过，没有则爬取内容存入任务队列
		:param title_url:
		:return:
		'''
		print('书名：',self.job[1],'\n')
		try:
			item = self.db.get_task ( self.job [1] )
			self.db.put_task ( self.job [1], item )
		except:
			try:
				self.mg.table.find()
			except:
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
						self.db.put_task ( self.job [1], i )




	def content(self,chapter_job):
		index,(title,url,hash_url) = chapter_job
		try:
			response = requests.get ( url, headers=self.headers )
			response.encoding = 'utf-8'
			html = etree.HTML ( response.text )
			contents=html.xpath('//div[@id="content"]/text()')
			content = ''.join([i.strip() for i in contents])
			# re_ = [ len(re.compile(i,re.S).findall(content))   for i in PATTERN]
			if len(contents)<50 and re.compile(PATTERN1,re.S).search(content):
				raise NetError
				# else:
				# 	raise ContentError

			self.mg.table.update({'hash_url':hash_url},{'$set':{'title':title,'index':index,'content':content}},upsert=True)
			print ('%s：%s保存成功'%(self.job[1],title) )
		except NetError:
			print(content)
			print('获取%s无效内容，存入任务列表\n'%title)
			self.db.put_task(self.job[1],chapter_job)
		except Exception:
			print ( '获取%s内容失败，存入任务列表\n' % title )
			self.db.put_task ( self.job [1], chapter_job )
		# except ContentError:
		# 	pass
		# 放入失败的章节

	def books(self,main_url):
		# try:
		# 	item = self.db.get_task('BOOK_LIST')
		# 	self.db.put_task('BOOK_LIST',item)
		# except:
		try:
			response = requests.get(main_url,headers = self.headers)
			res = etree.HTML(response.text)
			books_url = res.xpath('//div[@id="main"]/div/ul/li/a/@href')
			books_title = res.xpath('//div[@id="main"]/div/ul/li/a/text()')
			# print(books_title)
			books = zip(books_url,books_title)
			for i in books:
				if len(i)==2:
					self.db.put_task('BOOK_LIST',i)
		except:
			print('获取章节出现异常')

	def run(self):
		while True:
			try:
				chapter = self.db.get_task(self.job[1])
				self.content(chapter)
			except:
				break
		print('一个线程结束')


if __name__ == '__main__':
	# main_url = 'http://www.xbiquge.la/xiaoshuodaquan/'
	bqg = BiQuGe()
	# bqg.chapters("http://www.xbiquge.la/9/9795/")
	# bqg.content("http://www.xbiquge.la/9/9795/4308760.html")