import redis
import pymongo
from settings import *
class MongoClient:
	def __init__(self,dbname,tablename):
		self.client = pymongo.MongoClient(host=MONGO_HOST,port=MONGO_PORT)
		self.dbname=dbname
		self.tablename = tablename

	@property
	def db(self):
		db = self.client[self.dbname]
		return db

	@property
	def table(self):
		table = self.db[self.tablename]
		return table

class RedisClient:
	def __init__(self):
		self.rd = redis.Redis()

	def put_task(self,set_name,url):
		if not isinstance(set_name,str):
			set_name = str(set_name)
		if not isinstance(url,str):
			url = str(url)
		self.rd.sadd(set_name,url)

	def get_task(self,set_name):
		task = self.rd.spop(set_name)
		# print(task)
		task = task.decode()
		task = eval(task)
		# print(task)
		return task


if __name__ == '__main__':
	pass
	mg = MongoClient()
	mg.save('newdb','newtable','zhangsan','nibababba')