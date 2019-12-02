import time

import multiprocessing
from Spider.db_link import RedisClient
from Spider.spider import BiQuGe

class Work:
	def __init__(self,book):
		self.st_time=time.time()
		self.book=book
	def gogogo(self):
		print('开启进程%s\n'%str(self.book[1]))
		spider_list = [BiQuGe(job=self.book) for i in range(5)]
		print('开启了线程\n')
		for spider in spider_list:
			spider.start()
		for spider in spider_list:
			spider.join()
		ed_time = time.time ()
		t = ed_time - self.st_time
		return t
	def log(self,t):
		with open ( 'biquge.log', 'a' ) as fp:
			fp.write ( '%s爬完了，用了%f\n' % (self.book, t) )
			print ( '%s爬完了，用了%f' % (self.book, t) )

def startwork():
	p = multiprocessing.Pool(4)
	db = RedisClient()
	i = 1
	while True:
		i+= 1
		try:
			book = db.get_task('BOOK_LIST')
			w = Work(book)
			print('-'*100)
			print(book[1])
			p.apply_async(func=w.gogogo,callback=w.log)
		except:
			break
	p.close()
	print('%s个进程创建完毕\n'%i)
	p.join()
	print('%s 结束'%(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())))


if __name__ == '__main__':
	bqg = BiQuGe ()  # 获取book列表
	startwork()
