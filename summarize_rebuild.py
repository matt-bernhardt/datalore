# This script parses each document in the rebuilt articles collection, counting the number of times that any given field appears

# imports
import json
import bson
from bson.json_util import dumps
import pymongo

def main():

  # Log file
  log = open('logs/summarize_rebuild.txt','w')
  log.write('Begin\n')

  # Connect to database
  client = pymongo.MongoClient('mongodb://localhost:27017')
  db = client.openaccess
  collection = db.rebuild
  log.write('Connection to database\n')

  # output
  output = open('summarize_rebuild.txt','w')

  articles = []
  fields = []
  fieldCounts = []
  i = 0

  j = 0

  for record in collection.find():
    # articles.append(record)
    log.write(str(i) + " " + str(record["dc-identifier-uri"]) + "\n")
    print str(i)

    # Loop over every key in this document
    for thing in record.keys():

      log.write( str(thing) + "\n")

      j = 0
      exists = False
      for found in fields:
        # Loop over what we've already found

        # log.write(str(thing) + " " + str(found) + "\n")

        # compare 
        if found == thing:
          fieldCounts[j] = fieldCounts[j] + 1
          exists = True

        j = j + 1

      if exists == False:
        fields.append(thing)
        fieldCounts.append(1)

      log.write("\n")

    i = i + 1

  output.write(dumps(fields))
  output.write(dumps(fieldCounts))

  print('Finished!')

if __name__ == "__main__":
  main()
