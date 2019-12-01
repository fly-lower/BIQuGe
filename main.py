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
	# """
	# print('开始了')
	# print(book)
	print('开始爬%s'%book)
	st = time.time()
	spider_list = [BiQuGe(job=book) for i in range(5)]
	for spider in spider_list:
		spider.start()
		# spider.joi
	with open('biguge.log','a') as fp:
		fp.write('%s爬完了，用了%f\n' % (book,time.time()-st))
	print ( '%s爬完了，用了%f' % book,time.time()-st )




if __name__ == '__main__':
	bqg = BiQuGe()
	p = multiprocessing.Pool(4)
	db = RedisClient()
	book = db.get_task ( 'BOOK_LIST' ) # 传入书名
	gogogo(book)
	i = 1
	while True:
		i+= 1
		try:
			book = db.get_task('BOOK_LIST')
		except:
			break
		p.apply_async(func=gogogo,args=(book[0],))
	# 	except Exception as p:
	# # 		# print(p)
	# 		print('故障了')
	# 		i+=1
	# 		time.sleep(5)
	p.close()
	print('%s个进程创建完毕'%i)
	print()
	print('%s 结束'%(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())))
	p.join()
