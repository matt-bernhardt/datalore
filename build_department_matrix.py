# This script reads in a list of articles and affiliated departments, in the 
# format of:
#
# Column 0             Column 1
# Article #1 Handle    Department A
# Article #1 Handle    Department B
# Article #2 Handle    Department A
#
# In this case, we are working with a subset of such links dealing only with
# the academic departments at MIT (a messy designation, but needed for now)
# Based on these links, the script builds up a matrix of linkages between 
# departments based on coauthorship.
#
# This network is then rendered in several formats for use in visualizations:
# academic_force.json is used in a force-directed graph
# academic_departments.csv and ...
# academic_matrix.json are used in the chord diagram
# academic_matrix.csv was an earlier attempt that has been abandoned
#
# Please note: the script currently looks at "Sheet 3" in the source 
# spreadsheet, but switching to "Articles-Departments" would generate a more
# complete matrix of all 179 units around MIT that have contributed to the 
# Open Access collection.
#
# This broader dataset is what was used to build the "department_*.*" output
# files.

# imports
import json
import bson
from bson.json_util import dumps
from xlrd import open_workbook

def main():

  # Log file
  log = open('logs/build_department_matrix.txt','w')
  log.write('Begin\n')

  # output
  output_matrix = open('departments/academic_matrix.json','w')
  output_csv = open('departments/academic_matrix.csv','w')
  output_depts = open('departments/academic_departments.csv','w')
  output_force = open('departments/academic_force.json','w')

  # input excel
  wb = open_workbook('departments/Articles-Departments.xlsx')
  sheet = wb.sheet_by_name("Sheet3")

  print 'Sheet: ' + str(sheet.name)

  # Define lists and matrices
  departments = []
  allDepartments = []
  matrix = [[0 for x in range(38)] for x in range(38)]
  article = ""
  lastArticle = ""

  i = 0

  for row in range(1,sheet.nrows):

    # load this row's values
    article = sheet.cell(row,0).value
    tempDepartment = sheet.cell(row,1).value
    # print article
    # log.write(str(i) + "  " + str(article) + " " + str(tempDepartment) + "\n")

    # Have we seen this department before?
    if tempDepartment not in allDepartments:
      allDepartments.append(tempDepartment)

    # compare this article to last - is this a new article?
    if article != lastArticle:
      # This is a new article
      # log.write("\n\nNew Article\n")

      # Dump information about previous article
      print lastArticle
      log.write(lastArticle + "\n")
      log.write(dumps(departments) + "\n")
      log.write("\n")

      # Augment the matrix based on the current array of departments
      for one in departments:
        for two in departments:
          if one != two:
            oneIndex = allDepartments.index(one)
            twoIndex = allDepartments.index(two)
            log.write("  " + str(oneIndex) + "," + str(twoIndex) + "\n")
            matrix[oneIndex][twoIndex] = matrix[oneIndex][twoIndex] + 1
            matrix[twoIndex][oneIndex] = matrix[twoIndex][oneIndex] + 1

      # initialize this new article
      departments = []
      departments.append(tempDepartment)

    else:
      # still same article as before
      departments.append(tempDepartment)


    # for col in range(sheet.ncols):
    #   values.append(sheet.cell(row,col).value)
    # print ','.join(values)

    # store last article for comparison to next row
    lastArticle = article
    i = i + 1

  # Deal with last record
  log.write(lastArticle + "\n")
  log.write(dumps(departments) + "\n")
  for one in departments:
    for two in departments:
      if one != two:
        oneIndex = departments.index(one)
        twoIndex = departments.index(two)
        log.write("  " + str(oneIndex) + "," + str(twoIndex) + "\n")
        matrix[oneIndex][twoIndex] = matrix[oneIndex][twoIndex] + 1
        matrix[twoIndex][oneIndex] = matrix[twoIndex][oneIndex] + 1

  # Export list of departments
  # print allDepartments.length + " departments in total"
  for term in allDepartments:
    output_depts.write("\"" + str(term) + "\"\n")

  # Export matrix
  output_matrix.write(dumps(matrix))

  for outer in matrix:
    for inner in outer:
      output_csv.write(str(inner) + ",")
    output_csv.write("\n")

  # Export force layout object
  force = {}
  forceNodes = []
  forceLinks = []
  
  for term in allDepartments:
    node = {"name":term,"group":1,"papers":2,"tc":3,"cd":3}
    forceNodes.append(node)
  force["nodes"] = forceNodes

  i = 0
  for outer in matrix:
    j = 0
    for inner in outer:
      if inner > 0:
        link = {"source":i,"target":j,"value":inner}
        forceLinks.append(link)
      j = j + 1
    i = i + 1
  force["links"] = forceLinks

  output_force.write(dumps(force))

  print('Finished!')

if __name__ == "__main__":
  main()
