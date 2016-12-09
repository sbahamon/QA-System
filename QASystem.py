# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 11:23:12 2016

@author: Steffany
"""
#from nltk.corpus.reader.plaintext import PlaintextCorpusReader
import os, os.path
from whoosh.fields import Schema, ID, TEXT
from whoosh.analysis import StemmingAnalyzer
from whoosh.index import create_in
from whoosh.writing import AsyncWriter
from whoosh.qparser import QueryParser
from whoosh.highlight import ContextFragmenter
from nltk.corpus import stopwords

#Set schema with texts as articles and dates as IDs"""
schema = Schema(date = ID(stored=True),
                articles=TEXT(analyzer = StemmingAnalyzer(),stored=True))

# Create index dir if it does not exists.
if not os.path.exists("index"):
    os.mkdir("index")
 
# Initialize index
index = create_in("index", schema)

#Fill index with BI articles
writer = AsyncWriter(index)
for file in os.listdir("unicode"):
    fileobj = open("unicode/"+file,"rb")
    article = fileobj.read()
    fileobj.close()
    writer.add_document(date=file, articles=article)
writer.commit()

#create a searcher
searcher = index.searcher()
qp = QueryParser("content", schema = index.schema)

#finds answwer to a clearned query
def Answer(queryinput):
    q = qp.parse(queryinput)
    with index.searcher as s:
        Doc = s.search(q, limit = 1)
    return Doc.ContextFragmenter()

#returns cleans a query
def UserInput(writein):
    question = input("What is your question?")
    clean_q = [word for word in question if word not in stopwords.words('english')]
    return clean_q

#unites both functions above
def QASystem(question):
    return Answer(UserInput(question))
