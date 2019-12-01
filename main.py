import time

import requests
import threading
import multiprocessing
from multiprocessing import pool
from db_link import RedisClient
from spider import BiQuGe
st = 0
def gogogo(book):
	global st
	st = time.time ()
	print('开启进程%s\n'%str(book[1]))
	spider_list = [BiQuGe(job=book) for i in range(5)]
	for spider in spider_list:
		spider.start()
def log(book):
	global st
	with open('biquge.log','a') as fp:
		fp.write('%s爬完了，用了%f'%(book,time.time()))
		print('%s爬完了，用了%f'%(book,time.time()))



if __name__ == '__main__':
	bqg = BiQuGe() #获取book列表
	p = multiprocessing.Pool(4)
	db = RedisClient()
	i = 1
	while True:
		i+= 1
		try:
			book = db.get_task('BOOK_LIST')
			print(book)
			p.apply_async(func=gogogo,args=(book,),callback=log)
		except:
			break
	p.close()
	print('%s个进程创建完毕'%i)
	p.join()
	print('%s 结束'%(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())))
