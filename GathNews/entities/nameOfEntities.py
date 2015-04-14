import nltk
import re
from nltk.tag import *
from pymongo import MongoClient	
from storageTools.mongo_tools import *


def list_of_entities():
	client = MongoConnection()
	db = client.eadw
	news = db.news

	file = open("./res/output.txt", "r").readlines()
	entities = []
	for line in file:
		entities.append(line.strip())

	cursor = news.find() #get all news from mongo
	print "checking..."
	for article in cursor:
		allThePeople = []
		print "checking..."
		for sentence in nltk.sent_tokenize(article["document"]):
			for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sentence))):
				if hasattr(chunk, "label"):
					if chunk.label() == "PERSON":
						people = " ".join(c[0] for c in chunk.leaves())
						if people in entities:
							if people not in allThePeople:
								allThePeople.append(people)
						else: continue

		insert_new_collections(allThePeople,article)

	print "DONE!"

def insert_new_collections(allPersons, oldArticle):
	client = MongoConnection()
	db = client.eadw
	peps = db.namesOfPersons

	newArticle = oldArticle
	newArticle['entities'] = allPersons
	peps.update({"link":newArticle['link']}, newArticle, True);

def retrieve_entities(link):
	client = MongoConnection()
	db = client.eadw
	peps = db.namesOfPersons

	report = peps.find_one({"link" : link})

	if report['entities']:
		return report['entities']
	else: return ["No entities found."]







