# imports
import json
import pymongo

def main():

  # Log file
  log = open('logs/merge_articles.txt','w')
  log.write('Begin\n')

  # Connect to database
  client = pymongo.MongoClient('mongodb://localhost:27017')
  collection = client.openaccess.hackathon
  log.write('Connection to database\n')


  # File names
  directory = "../articles/"

  for i in range(0,1480):
    filename = "articles_" + str(i) + ".json"

    print "Opening " + filename
    articles = json.loads( open( str(directory) + str(filename) ).read() )

    for entry in articles["articles"]:
      print ""
      print entry
      collection.insert( entry )

  print('Finished!')

if __name__ == "__main__":
  main()
