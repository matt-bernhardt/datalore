# imports
import json
import pymongo
import requests
import time
import xml.etree.ElementTree as ET
import xml.dom

def main():

  # Log file
  log = open('logs/augment_mets.txt','w')

  # Connect to database
  client = pymongo.MongoClient('mongodb://localhost:27017')
  db = client.openaccess
  collection = db.hackathon

  # get list of articles
  articles = collection.find()
  # articles = collection.find({"abstract":{"$exists":False}})
  
  i = 0

  for item in articles:
    print str(i) + " " + item["handle"]
    log.write(str(i) + " " + item["handle"] + "\n")

    # http://dspace.mit.edu/metadata/handle/1721.1/50236/mets.xml
    url = "http://dspace.mit.edu/metadata" + item["handle"] + "/mets.xml"
    log.write("  " + url + "\n")
    r = requests.get(url)

    # element - parsed XML, returns element
    element = ET.fromstring(r.text.encode('ascii','xmlcharrefreplace'))

    subjects = []
    abstract = ""

    for child in element.iter():
      abstract = ""
      # log.write("    " + str(child.tag) + "\n")
      # log.write("      " + str(child.attrib) + "\n")
      # log.write("      " + str(type(child.attrib)) + "\n")
      if child.text != None:
        log.write("      " + str(child.text.encode('ascii','xmlcharrefreplace')) + "\n")

      # if "element" in child.attrib and child.attrib['element'] == 'subject':
      #   log.write("      " + str(child.text.encode('ascii','xmlcharrefreplace')))
      #   subjects.append(str(child.text.encode('ascii','xmlcharrefreplace')))

      if "element" in child.attrib and child.attrib['element'] == 'description' and "qualifier" in child.attrib and child.attrib['qualifier'] == "abstract" and child.text != None:
        log.write("      " + str(child.text.encode('ascii','xmlcharrefreplace')))
        abstract = str(child.text.encode('ascii','xmlcharrefreplace'))

    item["abstract"] = abstract
    # log.write("      Subjects: " + str(subjects) + "\n")

    collection.update({"handle":item["handle"]},item,True)

    log.write("\n")
    i = i + 1

    time.sleep(0.2)

  print('Finished!')

if __name__ == "__main__":
  main()
