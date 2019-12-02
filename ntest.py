import re
import time
import pandas
import threading
# [print('a') for i in range(10)]
# # print(a)
#
# a = time.time()
# time.sleep(10)
# b = time.time()
#
# c = b-a
# d = pandas.to_timedelta(str(c)+'s')
#
# print(c)
# # print(c,type(c))
class R(Exception):
	pass
# a = re.compile('(.*?abc.*?)+?(.*?hdd.*?)*?(.*?dfg.*?)*?')
# b = 'poppkpoi'
# print(a.findall(b))
# try:
# 	a = 3
# 	if a<5:
# 		if a<4:
# 			print('张三')
# 			raise R
# except R:
# 	print(a)
# except Exception:
# 	print('异常')
# except:
# 	print('finally')
class t(threading.Thread):
	def __init__(self,tm):
		super().__init__()
		self.t1 = time.time()
		self.tm =tm
	def run(self) -> None:
		time.sleep(self.tm)

	def __del__(self):
		self.t2 = time.time()
		t3 = self.t2-self.t1
		print(t3)
		print(self._name)

if __name__ == '__main__':
	td = t(5)
	td1 = t(8)
	td.start()
	td1.start()

	td.join()
	td1.join()