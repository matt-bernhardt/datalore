# This script parses each document in the rebuilt articles collection, counting
# the number of times that any given field appears. It then dumps the output
# into an extremely inelegant text file that needs to be processed in 

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
  output = open('rebuild/summarize_rebuild.csv','w')

  # initialize entities
  articles = []
  fields = []
  fieldCounts = []
  i = 0
  j = 0

  # Iterate over each record in the collection
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

  # Output results into a quick CSV file.
  # This is a mess.
  i = 0
  for item in fields:
    output.write(str(fields[i]) + "," + str(fieldCounts[i]) + "\n")
    i = i + 1

  print('Finished!')

if __name__ == "__main__":
  main()
