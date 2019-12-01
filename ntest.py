import re
import time
import pandas
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
a = re.compile('(.*?abc.*?)+?(.*?hdd.*?)*?(.*?dfg.*?)*?')
b = 'poppkpoi'
# print(a.findall(b))
try:
	a = 3
	if a<5:
		if a<4:
			print('张三')
			raise R
except R:
	print(a)
except Exception:
	print('异常')
except:
	print('finally')
