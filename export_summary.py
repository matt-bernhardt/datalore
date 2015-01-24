# imports
import json
import bson
from bson.json_util import dumps
import pymongo

def main():

  # Log file
  log = open('logs/export_summary.txt','w')
  log.write('Begin\n')

  # Connect to database
  client = pymongo.MongoClient('mongodb://libdb-1.mit.edu:27017')
  db = client.oastats
  collection = db.summary
  log.write('Connection to database\n')

  # output
  output = open('export_summary.json','w')

  articles = []

  for record in collection.find({"type":"dlc"}):
    articles.append(record)
    log.write(str(type(record)) + "\n")

  output.write(dumps(articles))

  print('Finished!')

if __name__ == "__main__":
  main()
