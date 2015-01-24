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

  # get list of identifiers
  # http://dspace.mit.edu/handle/1721.1/53727?show=full
  # //*[@id="aspect_artifactbrowser_ItemViewer_div_item-view"]/table
  # Keys: //*[@id="aspect_artifactbrowser_ItemViewer_div_item-view"]/table/tbody/tr[1]/td[1]
  # Values: //*[@id="aspect_artifactbrowser_ItemViewer_div_item-view"]/table/tbody/tr[1]/td[2]

  # http://dspace.mit.edu/metadata/handle/1721.1/54729/mets.xml
  # dim:field . mdschema . element . qualifier

  # articles = collection.find({"rebuilt":{"$exists":False}}).limit(5)
  articles = collection.find()

  i = 0
  for item in articles:

    # Log the item we're working with
    print "!!!" + str(i) + " " + item["handle"]
    log.write(str(i) + " " + item["handle"] + "\n")

    # Build URL to scrape
    # http://dspace.mit.edu/metadata/handle/1721.1/54729/mets.xml
    url = "http://dspace.mit.edu/metadata" + item["handle"] + "/mets.xml"
    # log.write("  " + str(url) + "\n")

    # Grab returned document
    r = requests.get(url)

    # Parse returned document into element
    element = ET.fromstring(r.text.encode('ascii','xmlcharrefreplace'))

    # set new item
    newitem = {}

    # Loop over every item in this element
    for child in element.iter():
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
    # print str(newitem)
    rebuild.insert(newitem)

    # Mark original as rebuilt
    item["rebuilt"] = "true"
    collection.update({"handle":item["handle"]},item,True)

    # Increment counter, wait before grabbing next item
    i = i + 1
    time.sleep(0.2)

  print('Finished!')


if __name__ == "__main__":
  main()
