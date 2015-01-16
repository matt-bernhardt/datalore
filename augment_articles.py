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
  log = open('logs/augment_articles.txt','w')

  # Connect to database
  client = pymongo.MongoClient('mongodb://localhost:27017')
  db = client.openaccess
  collection = db.articles

  # get list of articles
  articles = collection.find()
  
  i = 0

  for item in articles:
    print str(i) + " " + item["handle"]
    log.write("Handle: " + item["handle"] + "\n")

    # need to transform handle into OAI-PMH call to 
    # http://dspace.mit.edu/oai/request?verb=GetRecord&metadataPrefix=oai_dc&identifier=oai:dspace.mit.edu:1721.1/92321
    # http://dspace.mit.edu/handle/1721.1/92321?show=full
    # http://dspace.mit.edu/handle/1721.1/92321?XML
    oai = "http://dspace.mit.edu/oai/request?verb=GetRecord&metadataPrefix=oai_dc&identifier=oai:dspace.mit.edu:" + item["handle"].replace("/handle/","")
    log.write("  " + oai + "\n")

    # log.write("\n")

    # r - raw response XML
    r = requests.get(oai)
    # log.write("r: " + str(type(r.text)) + "\n")
    # log.write(r.text.encode('ascii','xmlcharrefreplace') + "\n")

    # log.write("\n")

    # element - parsed XML, returns element
    element = ET.fromstring(r.text.encode('ascii','xmlcharrefreplace'))
    # log.write("element: " + str(type(element)) + "\n")
    # log.write(str(element) + "\n")
    # log.write(str(element.attrib) + "\n")

    # log.write(str(list(element.iter())) + "\n")

    # log.write("Iterate through returned elements:\n")

    creator = []
    description = []
    publisher = []
    date = []
    itemType = []
    identifier = []
    source = []
    language = []
    relation = []
    rights = []
    uncaught = []

    for child in element.iter():
      if(str(child.tag) == "{http://purl.org/dc/elements/1.1/}creator" and child.text != None):
        creator.append(str(child.text.encode('ascii','xmlcharrefreplace')))

      elif(str(child.tag) == "{http://purl.org/dc/elements/1.1/}description" and child.text != None):
        description.append(str(child.text.encode('ascii','xmlcharrefreplace')))

      elif(str(child.tag) == "{http://purl.org/dc/elements/1.1/}publisher" and child.text != None):
        publisher.append(str(child.text.encode('ascii','xmlcharrefreplace')))

      elif(str(child.tag) == "{http://purl.org/dc/elements/1.1/}date" and child.text != None):
        date.append(str(child.text.encode('ascii','xmlcharrefreplace')))

      elif(str(child.tag) == "{http://purl.org/dc/elements/1.1/}type" and child.text != None):
        itemType.append(str(child.text.encode('ascii','xmlcharrefreplace')))

      elif(str(child.tag) == "{http://purl.org/dc/elements/1.1/}identifier" and child.text != None):
        identifier.append(str(child.text.encode('ascii','xmlcharrefreplace')))

      elif(str(child.tag) == "{http://purl.org/dc/elements/1.1/}source" and child.text != None):
        source.append(str(child.text.encode('ascii','xmlcharrefreplace')))

      elif(str(child.tag) == "{http://purl.org/dc/elements/1.1/}language" and child.text != None):
        language.append(str(child.text.encode('ascii','xmlcharrefreplace')))

      elif(str(child.tag) == "{http://purl.org/dc/elements/1.1/}relation" and child.text != None):
        relation.append(str(child.text.encode('ascii','xmlcharrefreplace')))

      elif(str(child.tag) == "{http://purl.org/dc/elements/1.1/}rights" and child.text != None):
        rights.append(str(child.text.encode('ascii','xmlcharrefreplace')))

      else:
        uncaught.append(child.tag.encode('ascii','xmlcharrefreplace'))
        # log.write(str(child.tag) + "\n")
        # log.write(str(child.attrib) + "\n")
        # log.write(str(child.text) + "\n")
        # log.write("\n")

    log.write("  Uncaught: " + str(uncaught))

    # log.write(str(rights) + "\n")
    item["creator"] = creator
    item["description"] = description
    item["publisher"] = publisher
    item["date"] = date
    item["type"] = itemType
    item["identifier"] = identifier
    item["source"] = source
    item["language"] = language
    item["relation"] = relation
    item["rights"] = rights

    collection.update({"handle":item["handle"]},item,True)

    # log.write(feeddata)
    # log.write("\n")

    log.write("\n")
    i = i + 1

    time.sleep(1)

  print('Finished!')

if __name__ == "__main__":
  main()
