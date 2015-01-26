# This script takes a spreadsheet downloaded from the NIH detailing funded researchers at MIT.
# Because this list covers multiple lines, the same researcher can be listed multiple times.
# This script was meant to generates a file, nih_authors.csv, with each author listed only once.
# However, due to time pressure it only reads out the spreadsheet - unaltered - to a CSV file.
# The actual work of collapsing the data was instead done in a MySQL table.
#
# A second step of the process was to take the list of unique authors (stored in authors[]), and
# attempt to look up the number of open access papers in the collection based on their names.
# This isn't an ideal workflow because the slightest name variatins ("Jane M. Doe" and "Jane M Doe"
# won't match) result in lost connections. As it is, however, this script returned more than 100
# researchers out of a pool of 300+ funding recipients.

# imports
import pymongo
from xlrd import open_workbook

def main():

  # Log file
  log = open('logs/harvest_nih_authors.txt','w')

  # connect to mongo database
  client = pymongo.MongoClient('mongodb://localhost:27017')
  db = client.openaccess
  collection = db.rebuild
  log.write("Mongo connection made\n")

  # input excel
  wb = open_workbook('nih/NIH-Funding-Recipients.xlsx')
  sheet = wb.sheet_by_name("Funding")
  log.write("Sheet opened: " + str(sheet.name) + "\n")

  # output
  output_authors = open('nih/nih_authors.csv','w')

  authors = []
  authorsSearch = []
  authorRecords = []

  # Assemble the final list
  for row in range(1,sheet.nrows):

    # Load this row
    name = sheet.cell(row,0).value
    awards = sheet.cell(row,1).value
    funding = sheet.cell(row,2).value
    year = sheet.cell(row,3).value
    nameSearch = sheet.cell(row,4).value  

    # Write out row as CSV (yes, this is horrendous)
    output_authors.write("\"" + str(name) + "\"," + str(awards) + "," + str(funding) + "," + str(year) + "\n")

    # Summarize list into one author per line
    if name not in authors:
      authors.append(name)
      authorsSearch.append(nameSearch)
      record = {"Name":name,"Awards":awards,"Funding":funding,"NameSearch":nameSearch,"Years":[year]}
      authorRecords.append(record)
    else:
      # Need to update values
      a = 0

  # Work with assembled final list
  authors.sort()

  # Look up authors in OA dataset
  for name in authors:
    articleCount = collection.find({"dc-contributor-mitauthor":name}).count()
    log.write("\"" + str(name) + "\"," + str(articleCount) + "\n")
    # output_authors.write(str(name) + "\n")

  print('Finished!')

if __name__ == "__main__":
  main()
