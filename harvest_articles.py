# imports
import json
import pymongo
import requests
# need to look at the requests library
import time
import xml.etree.ElementTree as ET
import xml.dom

def main():

  # Log file
  log = open('logs/harvest_articles.txt','w')

  # Connect to database
  client = pymongo.MongoClient('mongodb://localhost:27017')
  db = client.openaccess
  collection = db.hackathon

  # get list of identifiers
  oai = "http://dspace.mit.edu/oai/request?verb=ListIdentifiers&metadataPrefix=oai_dc&set=hdl_1721.1_49433"
  log.write(oai + "\n")
  r = requests.get(oai)

  element = ET.fromstring(r.text.encode('ascii','xmlcharrefreplace'))

  i = 0

  for child in element.iter():
    # log.write(str(child.tag) + ": " + str(child.text) + "\n")
    if(str(child.tag) == "{http://www.openarchives.org/OAI/2.0/}identifier"):
      # oai:dspace.mit.edu:1721.1/49436
      handle = str(child.text.encode('ascii','xmlcharrefreplace').replace("oai:dspace.mit.edu:","/handle/"))
      log.write(str(i) + "  " + str(handle) + "\n")
      collection.insert({"handle":handle})
      i = i + 1

  print('Finished!')

if __name__ == "__main__":
  main()
