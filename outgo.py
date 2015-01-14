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

def getCertificate():
	f = []
	for line in open("CONFIG.dat"):
		f.append(line)
	return line.split(',')

def main():
	print "arranca"
	user , password = getCertificate()
	url = "mongodb://" + str(user) + ":" + str(password) + "@ds029541.mongolab.com:29541/outgodb"
	print url
	clientDB = pymongo.MongoClient(url)
	db = clientDB.outgodb

	o = Outgo("almuerzo chino", 33, datetime.datetime.utcnow(), ["almuerzo","comida"] )
	dic = o.to_dic()

	outgoes = db.outgoes
	outgoes.insert(dic)

	found_doc = outgoes.find_one(dic)
	print "encontre este documento :" + str(found_doc)
	print "documentos en la base :" + str(outgoes.count())


	print "termina"


main()