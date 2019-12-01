# i = [1,2,3,4,5]
# print(enumerate(i))
import time

import redis
import threading
import multiprocessing

# rd = redis.Redis()
#
# rd.sadd('lll','kaskd')
class A(threading.Thread):
	def __init__(self):
		super().__init__()
		print('init%s'%self.name)
	def p(self):
		time.sleep(1)
		print(self.name)
		# time.sleep(1)
		print('done')
	def run(self) -> None:
		self.p()

def pp(i):
	k = [A() for i in range(2)]
	for i in k:
		i.start()

if __name__ == '__main__':
	p = multiprocessing.Pool ( 5 )
	i=0
	while i<2:
		i+=1
		# print(i)
		p.apply_async(func=pp,args=(i,))
	p.close()
	p.join()

