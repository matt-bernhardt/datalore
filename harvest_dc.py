# This script takes a list of articles (expressed as handles) and extracts metadata for each 
# via a METS document. For DSpace@MIT, to see the METS record for an article you connect to a 
# URL such as http://dspace.mit.edu/metadata/handle/1721.1/54729/mets.xml
#
# Within this document, there are a number of dim:field elements which contain the catalogued
# metadata about that article. This script scans for those tags and stores each discovered
# value in a Mongo database.
# 
# A prerequisite to running this script is to have that list of article handles already stored
# in Mongo - this script just takes that list and adds the metadata to it.
#
# There is a reference here to a db.hackathon collection in Mongo - this can probably be
# removed by anyone using this in the future. For the hackathon, I had to redo this harvest
# after a failed first attempt.

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
  log = open('logs/harvest_dc.txt','w')

  # Connect to database
  client = pymongo.MongoClient('mongodb://localhost:27017')
  db = client.openaccess
  collection = db.hackathon
  rebuild = db.rebuild

  articles = collection.find()

  i = 0
  for item in articles:

    # Log the item we're working with
    print str(i) + " " + item["handle"]
    log.write(str(i) + " " + item["handle"] + "\n")

    # Build URL to scrape
    # http://dspace.mit.edu/metadata/handle/1721.1/54729/mets.xml
    url = "http://dspace.mit.edu/metadata" + item["handle"] + "/mets.xml"

    # Grab returned document
    r = requests.get(url)

    # Parse returned document into element
    element = ET.fromstring(r.text.encode('ascii','xmlcharrefreplace'))

    # set new item
    newitem = {}

    # Loop over every item in this element
    for child in element.iter():

      # Dublin core metadata is expressed in this HTML using the following attributes:
      # dim:field . mdschema . element . qualifier

      # make sure this item isn't empty/null, and this is a dim:field tag
      if child.text != None and str(child.tag) == "{http://www.dspace.org/xmlns/dspace/dim}field":

        # keys are always going to have mdschema.element
        key = child.attrib['mdschema'] + "-" + child.attrib['element']
        if 'qualifier' in child.attrib:
          key = key + "-" + child.attrib['qualifier']
        log.write("  " + str(key) + "\n")

        # value is pretty straighforward
        value = str(child.text.encode('ascii','xmlcharrefreplace'))
        log.write("    " + str(value) + "\n\n")

        # If we've already found this key, need to convert to a list
        # Otherwise, just store the key/value
        if key in newitem:
          if type(newitem[key]) is str:
            oldvalue = newitem[key]
            newitem[key] = []
            newitem[key].append(oldvalue)
          newitem[key].append(value)
        else:
          newitem[key] = value

    # Store rebuilt item in new collection
    rebuild.insert(newitem)

    # Mark original as rebuilt
    item["rebuilt"] = "true"
    collection.update({"handle":item["handle"]},item,True)

    # Increment counter, wait before grabbing next item
    i = i + 1
    # The sleep timer is necessary so the DSpace@MIT admins don't block access to your scraper
    time.sleep(0.2)

  print('Finished!')


if __name__ == "__main__":
  main()
