# mouser@donationcoder.com
# 12/18/20
# solver for soduko hex like puzzles


import json
import copy
import random
import array as arr

# global
globalIterationCount = 0
globalDebugFrequency = 10000
globalRandomizeSearch = True


def main():
  print("Starting sodsolve.. v1.0 - 12/18/20")
  data = readDataFile("eqdata.json")
  beginSolving(data)




def readDataFile(fname):
  with open(fname) as f:
    data = json.load(f)
    
    # convert rowdata for faster processing
    data["rowData"] = convertJsonRowData(data["rowData"])
    
    print(data)
    return data



def makeInitialNumberList(min, max):
  numberList = arr.array("i", range(min, max+1))
  return numberList

def makeInitialAssignmentList():
  blankAssignmentList = {}
  return blankAssignmentList



def convertJsonRowData(rowDataRaw):
  # convert json data to fast int arrays
  rowDataInts = []
  for row in rowDataRaw:
    oneRowDataInts = arr.array("i")
    for i in row:
      oneRowDataInts.append(int(i))
    rowDataInts.append(oneRowDataInts)
  return rowDataInts



def beginSolving(data):
  rowTotal = data["rowTotal"]

  # create initial number array
  numbersAvailable = makeInitialNumberList(data["min"], data["max"])
  # create assignment list
  assignmentList = makeInitialAssignmentList()


  print("Solving for totals of: ",rowTotal)
  print("Numbers available: ",numbersAvailable)

  # start recursive solve
  retv = recursiveSolve(0,0, data["rowData"], numbersAvailable, assignmentList, rowTotal)
  
  global globalIterationCount
  if retv:
    print("Found solution after ", globalIterationCount," iterations:")
    print(assignmentList)
  else:
    print("No solution found after ", globalIterationCount," iterations.")




def calculateLastValueOfRow(row, assignmentList, rowTotal):
  rowlen = len(row)
  rowTotalSoFar = calcRowPartialTotal(row, assignmentList, rowlen-1)
  return rowTotal-rowTotalSoFar


def calcRowPartialTotal(row, assignmentList, ItemIndex):
  totalSoFar = 0
  for i in range(0,ItemIndex):
    varIndex = row[i]
    val = assignmentList[varIndex]
    totalSoFar = totalSoFar + val
  return totalSoFar
  
 
def deepReplaceArray(dest, src):
  del dest[:]
  for v in src:
    dest.append(v)

def deepReplaceList(dest, src):
  dest.clear()
  for v in src:
    dest[v]=src[v]


def recursiveSolve(rowIndex, itemIndex, rowData, numbersAvailable, assignmentList, rowTotal):
  global globalIterationCount, globalDebugFrequency
  globalIterationCount = globalIterationCount + 1

  # row info
  row = rowData[rowIndex]
  rowlen = len(row)
  varIndex = row[itemIndex]

  if (globalIterationCount % globalDebugFrequency == 0):
    doDebugPrint = True
  else:
    doDebugPrint = False
  

  if doDebugPrint:
    print("In recursiveSolve iteration: ", globalIterationCount, " with row ", rowIndex, " and item ", itemIndex, " with varindex = ", varIndex)
    print("Row vars:", row)
    print("Assignments:", assignmentList)
    print("numbersAvail:", numbersAvailable)
    
  # are we at last item of row?
  if (itemIndex == rowlen-1):
    # yes, so we can just CALCULATE the last value
    lastVal = calculateLastValueOfRow(row, assignmentList, rowTotal)
    # was this variable already assigned a dif value?
    if (varIndex in assignmentList):
      # does it match?
      if (assignmentList[varIndex] != lastVal):
        # does not match, so that's a failure
        return False
      else:
        # matches, so we are consistent
        pass
    else:
      if (not lastVal in numbersAvailable):
        # calculated number is not in list, just return False
        if doDebugPrint:
          print("Last item for row calculated to be ", lastVal," but not in available list, so aborting.")
        return False
      # assign good calculated val
      if doDebugPrint:
        print("Last item for row calculated GOOD as ", lastVal)
      assignmentList[varIndex] = lastVal
      numbersAvailable.remove(lastVal)
    # are we done?
    if (rowIndex == len(rowData)-1):
      # yes, all done, so return true
      return True
    # not done, go to first item of next row
    retv = recursiveSolve(rowIndex+1, 0, rowData, numbersAvailable, assignmentList, rowTotal)
    return retv

  # we are at an intermediate index
  # but is it already assigned?!
  if (varIndex in assignmentList):
    # already assigned, so just skip it
    return recursiveSolve(rowIndex, itemIndex+1, rowData, numbersAvailable, assignmentList, rowTotal)


  # we are at an intermediate index, not yet assigned; we need to recursively loop it through all available numbers
  rowTotalSoFar = calcRowPartialTotal(row, assignmentList, itemIndex)
  
  global globalRandomizeSearch
  if (globalRandomizeSearch):
    # randomize numbersAvailable
    random.shuffle(numbersAvailable)
  
  for i in range(0, len(numbersAvailable)):
    anum = numbersAvailable[i]
    if (rowTotalSoFar + anum >= rowTotal):
      # too big dont bother trying this number
      continue
    # make clean copies
    numbersAvailableCopy = copy.deepcopy(numbersAvailable)
    assignmentListCopy = copy.deepcopy(assignmentList)
    # assign it this try
    assignmentListCopy[varIndex]=anum
    # remove it from available numbers
    #del numbersAvailableCopy[i]
    numbersAvailableCopy.remove(anum)
    # now recursive call for others
    retv = recursiveSolve(rowIndex, itemIndex+1, rowData, numbersAvailableCopy, assignmentListCopy, rowTotal)
    if (retv):
      # assign solution?
      deepReplaceList(assignmentList, assignmentListCopy)
      deepReplaceArray(numbersAvailable, numbersAvailable)
      return retv
    # otherwise loop and try another
    
  # could not find solution
  return False
  
  
  

  
  
if __name__ == "__main__":
  main()  
  
  
  
  
  
'''
eqdata.json
  {
"min":1,
"max":19 ,
"rowTotal":38,

"rowData": [
 [0,1,2],
 [2,6,11],
 [11,15,18],
 [18,17,16],
 [16,12,7],
 [7,3,0],
 
 [3,4,5,6],
 [6,10,14,17],
 [17,13,8,3],
 
 [1,5,10,15],
 [15,14,13,12],
 [12,8,4,1],
 
 [0,4,9,14,18],
 [2,5,9,13,16],
 [7,8,9,10,11]
]
}
'''