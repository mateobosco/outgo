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

	def addTag(self,tag):
		self.tags.append(tag)

	def toDic(self):
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

	def addOutgo(self,outgo):
		self.db.outgoes.insert(outgo.toDic())

	def findOutgo(self,outgo):
		return self.db.outgoes.find_one(outgo.toDic())



class Program(object):

	def __init__(self):
		self.base = Base()
		self.argv = sys.argv

	def parameterDisclaimerFromInput(self):
		if "new" in self.argv:
			parameters = self.getNewOutgoParameters()
			self.addOutgoFromParameters(parameters)
		
		if "query" in self.argv:
			#OBTENER LOS PARAMETROS DESDE ARGV
			o = Outgo()
			self.base.findOutgo(o)


	def getNewOutgoParametersFromArguments(self):
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

	def getNewOutgoParametersFromInput(self):
		parameters={}
		parameters["desc"] = raw_input("Description: ")
		parameters["cost"] = input("Cost: ")
		string_tags = raw_input("Tags (separated by comma): ")
		parameters["tags"] = string_tags.split(",")
		return parameters

	def addOutgoFromParameters(self,parameters):
		o = Outgo(parameters["desc"], parameters["cost"], datetime.datetime.utcnow(), parameters["tags"])
		print str(o)
		self.base.addOutgo(o)

	def startInteraction(self):
		e = input("Options: \n 1 - Add a new outgo \n 2 - Query \n")
		if e == 1:
			parameters = self.getNewOutgoParametersFromInput()
			self.addOutgoFromParameters(parameters)
		if e == 2:
			#DO QUERY
			o = Outgo()
			self.base.findOutgo(o)
		else:
			print "elegi bien forro"



def main():
	print "arranca"
	program = Program()
	print sys.argv

	if len(sys.argv) > 1:
		program.parameterDisclaimerFromInput()
		new_outgo_parameters = program.getNewOutgoParameters()
		print new_outgo_parameters

	else:
		program.startInteraction()


	print "termina"


main()