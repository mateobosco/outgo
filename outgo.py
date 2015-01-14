import pymongo
import datetime


class Outgo(object):

	def __init__(self,desc,cost,date,tags):
		self.desc = desc
		self.cost = cost
		self.date = date
		self.tags = tags

	def __str__(self):
		return "Gasto de " + str(cost) + "en " + str(desc)

	def add_tag(self,tag):
		self.tags.append(tag)

	def to_dic(self):
		dic = {}
		dic["description"] = self.desc
		dic["cost"] = self.cost
		dic["date"] = self.date
		dic["tags"] = self.tags
		return dic



class Base(object):
	def __init__(self):
		self.user, seflpass = user , password = self.getCertificate()
		self.url = "mongodb://" + str(user) + ":" + str(password) + "@ds029541.mongolab.com:29541/outgodb"
		self.mongo_client = pymongo.MongoClient(self.url)
		self.db = self.mongo_client.outgodb

	def getCertificate(self):
		f = []
		for line in open("CONFIG.dat"):
			f.append(line)
		return line.split(',')

	def add_outgo(self,outgo):
		self.db.outgoes.insert(outgo.to_dic())



def main():
	print "arranca"
	base = Base()

	o = Outgo("almuerzo chino", 33, datetime.datetime.utcnow(), ["almuerzo","comida"] )
	base.add_outgo(o)

	#found_doc = base.db.outgoes.find_one(o.to_dic)
	#print "encontre este documento :" + str(found_doc)
	print "documentos en la base :" + str(base.db.outgoes.count())


	print "termina"


main()