# imports
import json
import bson
from bson.json_util import dumps
import pymongo

def main():

  # Log file
  log = open('logs/export_articles.txt','w')
  log.write('Begin\n')

  # Connect to database
  client = pymongo.MongoClient('mongodb://localhost:27017')
  db = client.openaccess
  collection = db.rebuild
  log.write('Connection to database\n')

  # output
  output = open('exports/export_rebuild.json','w')

  articles = []

  for record in collection.find():
    articles.append(record)
    log.write(str(type(record)) + "\n")

  output.write(dumps(articles))

  print('Finished!')

if __name__ == "__main__":
  main()
