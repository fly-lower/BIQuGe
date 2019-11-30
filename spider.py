import requests
import threading
from threading import Thread

from lxml import etree
from db_link import RedisClient as RD
from db_link import MongoClient as MG
from settings import *
from tools import *

class BiQuGe(Thread):
	def __init__(self,chapter_job=None,job=None,):
		self.chapter_job = chapter_job
		self.db  = RD()
		super().__init__()
		self.job=job
		self.headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
		}

		self.books('http://www.xbiquge.la/xiaoshuodaquan/')
		if self.job:
			print('开工了')
			self.chapters(self.job[0])


	def chapters(self,title_url):
		print('章节')
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

				#(0,(title,url))
	def content(self,chapter_job):
		print('内容')
		try:
			index,(title,url,hash_url) = chapter_job
			response = requests.get ( url, headers=self.headers )
			response.encoding = 'utf-8'
			html = etree.HTML ( response.text )
			contents=html.xpath('//div[@id="content"]/text()')
			content = ''.join([i.strip() for i in contents])
			print ( title )
			mg = MG(MONGO_DB,self.job[1])
			mg.table.update({'hash_url':hash_url},{'$set':{'title':title,'index':index,'content':content}},upsert=True)
		except:
			self.db.put_task(self.job[1],chapter_job)
		# print(len(content))

	def books(self,main_url):
		# print('books')
		response = requests.get(main_url,headers = self.headers)
		res = etree.HTML(response.text)
		books_url = res.xpath('//div[@id="main"]/div/ul/li/a/@href')
		books_title = res.xpath('//div[@id="main"]/div/ul/li/a/text()')
		books = zip(books_url,books_title)
		print('书本')
		for i in books:
			if len(i)==2:
				self.db.put_task('BOOK_LIST',i)
		print('-----------------------------------')

	def run(self):
		self.content(self.chapter_job)



if __name__ == '__main__':
	# main_url = 'http://www.xbiquge.la/xiaoshuodaquan/'
	bqg = BiQuGe()
	# bqg.chapters("http://www.xbiquge.la/9/9795/")
	# bqg.content("http://www.xbiquge.la/9/9795/4308760.html")