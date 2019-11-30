import time

import requests
import threading
import multiprocessing
from multiprocessing import pool
from db_link import RedisClient
from spider import BiQuGe

def gogogo(book):
	"""
	请求内容
	:return:
	"""
	print('开始了')
	while True:
		chapters = db.get_task(book)
		if not chapters:
			break
		spider_list = [BiQuGe(job=book,chapter_job=chapters) for i in range(10)]
		for spider in spider_list:
			spider.start()




if __name__ == '__main__':
	# main_url=''
	# t = threading.Thread(target=BiQuGe.books,args=(main_url,))
	bqg = BiQuGe()
	print('-----')
	p = multiprocessing.Pool(5)
	db = RedisClient()

	i = 1
	while i<25:
		try:
			book = db.get_task('BOOK_LIST')
			# print(book)
			p.apply_async(func=gogogo,args=(book,))
			print('进程')
			i-=1
		except:
			print('故障了')
			i+=1
			time.sleep(5)
	p.close()
		# p.join()
	print('%s 炸了'%(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())))
