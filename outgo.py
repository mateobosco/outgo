import pymongo
import datetime
import sys
import re
import json


def createOutgoFromJson(json):
	dic = json.loads(json)
	return createOutgoFromDic(dic)

def createOutgoFromDic(dic):
	outgo = Outgo(dic.get("description") , dic.get("cost") , dic.get("date") , dic.get("tags"))
	return outgo


class Outgo(object):

	def __init__(self,desc,cost,date,tags):
		self.desc = desc
		self.cost = cost
		if (date): self.date = date
		else: self.date =  datetime.datetime.utcnow()
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
		return self.db.outgoes.insert(outgo.toDic())

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


	def getTagsFromString(self,string):
		tags = re.split(",| ", string)
		filter(lambda a: a not in [""," ",","], tags)
		return tags


	def getNewOutgoParametersFromArguments(self):
		if "-d" in self.argv and "-c" in self.argv and "-t" in self.argv:
			parameters={}
			index_new_outgo_desc = self.argv.index("-d") + 1
			parameters["desc"] = self.argv[index_new_outgo_desc]
			index_new_outgo_cost = self.argv.index("-c") + 1
			parameters["cost"] = self.argv[index_new_outgo_cost]
			index_new_outgo_tags = self.argv.index("-t") + 1
			string_tags = self.argv[index_new_outgo_tags]
			parameters["tags"] = self.getTagsFromString(string_tags)
			return parameters
		else:
			print "There are some parameters missing."


	def getNewOutgoParametersFromInput(self):
		parameters={}
		parameters["desc"] = raw_input("Description: ")
		parameters["cost"] = input("Cost: ")
		string_tags = raw_input("Tags: ")
		parameters["tags"] = self.getTagsFromString(string_tags)
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
		elif e == 2:
			#DO QUERY
			o = Outgo()
			self.base.findOutgo(o)
		else:
			print "elegi bien forro"



def main():
	program = Program()

	if len(sys.argv) > 1:
		program.parameterDisclaimerFromInput()
		new_outgo_parameters = program.getNewOutgoParameters()

	else:
		program.startInteraction()


# main()