import pymongo
import datetime
import sys


class Outgo(object):

	def __init__(self,desc,cost,date,tags):
		self.desc = desc
		self.cost = cost
		self.date = date
		self.tags = tags

	def __str__(self):
		return "Gasto de " + str(self.cost) + " en " + str(self.desc)

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

	def find_outgo(self,outgo):
		return self.db.outgoes.find_one(outgo.to_dic())



class Program(object):

	def __init__(self):
		self.base = Base()
		self.argv = sys.argv



	def parameter_disclaimer(self):
		if "new" in self.argv:
			parameters = self.get_new_outgo_parameters()
			o = Outgo(parameters["desc"], parameters["cost"], datetime.datetime.utcnow(), parameters["tags"])
			print str(o)
			self.base.add_outgo(o)
		
		if "query" in self.argv:
			#OBTENER LOS PARAMETROS DESDE ARGV
			o = Outgo()
			self.base.find_outgo(o)



	def get_new_outgo_parameters(self):
		if "-d" in self.argv and "-c" in self.argv and "-t" in self.argv:
			parameters={}
			index_new_outgo_desc = self.argv.index("-d") + 1
			parameters["desc"] = self.argv[index_new_outgo_desc]
			index_new_outgo_cost = self.argv.index("-c") + 1
			parameters["cost"] = self.argv[index_new_outgo_cost]
			index_new_outgo_tags = self.argv.index("-t") + 1
			string_tags = self.argv[index_new_outgo_tags]
			parameters["tags"] = string_tags.split(",")
			return parameters
		else:
			print "There are some parameters missing."




def main():
	print "arranca"
	program = Program()
	print sys.argv

	if len(sys.argv) > 1:
		program.parameter_disclaimer()
		new_outgo_parameters = program.get_new_outgo_parameters()
		print new_outgo_parameters


	print "termina"


main()