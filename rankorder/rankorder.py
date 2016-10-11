# -*- coding: utf-8 -*-
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_data_from_file():
    try:
        dataFile = os.path.join(BASE_DIR, 'files/rankorder/weakconcepts.txt')
        matrix = [line.rstrip('\n').rstrip('\r').split("\t") for line in open(dataFile)]
        return matrix
    except IOError:
        return('cannot open')


def get_binary_array(number):
    binaryArray = [0 for i in range(0, number)] #fill array with 0
    binaryArrayString = [0 for i in range(0, number)] #fill array with 0
    for i in range(0, number):
        binaryArray[i] = 2 ** (number-i-1) #pows 2^4, 2^3, 2^2...
        binaryArrayString[i] = number-i-1
    return (binaryArray, binaryArrayString)


def reorder_matrix_lines(matrix):
    binaryArray, binaryArrayString, linesWeightArray, linesPows = get_lines_weights_array(matrix)
    orderedLinesWeight = get_ordered_lines_weight(linesWeightArray)

    """orderedMatrix = sort_lines_weight(orderedLinesWeight, matrix)
    dataFile = os.path.join(BASE_DIR, 'files/rankorder/orderedmatrix.txt')
    save_matrix_on_file(orderedMatrix, dataFile, val=True)"""

    return binaryArray, binaryArrayString, linesWeightArray, linesPows


def get_lines_weights_array(matrix):
    columnsNumber = len(matrix[0]) - 1 #not including students column
    linesNumber = len(matrix) - 1 #not including weak concepts line
    linesPows = [[] for i in range(linesNumber)]

    binaryArray, binaryArrayString = get_binary_array(columnsNumber)

    linesWeightArray = [0 for i in range(0, linesNumber)] #fill array with 0
    for i in range(linesNumber):
        weight = 0
        for j in range(columnsNumber):
            weight += binaryArray[j] * int(matrix[i+1][j+1]) #convert string to int

            if int(matrix[i+1][j+1]) == 1:
               linesPows[i].append(binaryArrayString[j])

        linesWeightArray[i] = weight #save weight of each line
    return binaryArray, binaryArrayString, linesWeightArray, linesPows


def get_ordered_lines_weight(linesWeight):
    value = 1
    linesNumber = len(linesWeight)
    orderedLinesWeight = [0 for i in range(0, linesNumber)]  #fill array with 0
    linesWeightArrayCopy = linesWeight[:] #create linesWeightArray copy

    while value <= linesNumber:
        aux = 0
        lower = 2 ** (linesNumber + 2)
        for i in range(0, linesNumber):
            #print i, linesWeight_copy[i]
            if linesWeightArrayCopy[i] < lower:
                lower = linesWeightArrayCopy[i]
                #print "lower", lower
                aux = i

        linesWeightArrayCopy[aux] = 2 ** (linesNumber + 2)
        orderedLinesWeight[aux] = value
        value += 1
    return  orderedLinesWeight


#sort weights in decreasing order
def sort_lines_weight(orderedLinesWeight, matrix):
    value = 1
    columnsNumber = len(matrix[0])
    linesNumber = len(matrix)

    orderedMatrix = [[0 for col in range(columnsNumber)] for row in range(linesNumber)] #fill matrix with 0
    flag = 1

    orderedMatrix[0] = matrix[0]

    while value < linesNumber:
        aux = 1
        upper = 0
        for i in range(0, linesNumber - 1):
            if orderedLinesWeight[i] > upper:
                upper = orderedLinesWeight[i]
                aux = i
        #print "upper", upper, "i=", aux

        orderedLinesWeight[aux] = 0

        temp = matrix[aux+1]

        i = 0
        while i < columnsNumber:
            orderedMatrix[flag][i] = temp[i]
            i += 1

        value += 1
        flag += 1

    return orderedMatrix


#write matrix on a file
def save_matrix_on_file(matrix, file, val):
    columnsNumber = len(matrix[0]) - 1
    linesNumber = len(matrix) - 1

    dir = os.path.dirname(__file__)
    matrixFile = os.path.join(dir, file)
    openMatrixFile = open(matrixFile, 'w+')

    if (val): #just in case we need to add Headers
        i = 0
        while i <= columnsNumber:
            openMatrixFile.write("col" + str(i) + "\t")  # adding headers for using get_columns method
            i += 1

    openMatrixFile.write("\n")
    for i in range(linesNumber+1):
        for j in range(columnsNumber+1):
            openMatrixFile.write(repr(matrix[i][j]) + "\t") #use repr to save also the initial space
        openMatrixFile.write("\n")
    openMatrixFile.close()


#Split file by columns: took from https://bitbucket.org/alinium/fileparsers/wiki/Home
tab = "\t"
def get_columns(inFile, delim=tab, header=True):
    """
    Get columns of data from inFile. The order of the rows is respected

    :param inFile: column file separated by delim
    :param header: if True the first line will be considered a header line
    :returns: a tuple of 2 dicts (cols, indexToName). cols dict has keys that
    are headings in the inFile, and values are a list of all the entries in that
    column. indexToName dict maps column index to names that are used as keys in
    the cols dict. The names are the same as the headings used in inFile. If
    header is False, then column indices (starting from 0) are used for the
    heading names (i.e. the keys in the cols dict)

    Sample File:
    Heading 1    Heading 2    Heading 3
    row1value1   row1value2   row1value3
    row2value1   row2value2   row2value3

    Sample usage on sample file:
    cols, i2n = get_columns(sampleFile)
    cols["Heading 1"] == cols[i2n[0]]
    cols["Heading 2"] == cols[i2n[1]]
    cols["Heading 3"][0] == "row1value3"
    set(cols["Heading 1"]).union(set(cols["Heading 3"])
    """
    cols = {}
    indexToName = {}
    for lineNum, line in enumerate(inFile):
        if lineNum == 0:
            headings = line.strip().split(delim)
            k = 0
            for heading in headings:
                heading = heading.strip()
                if header:
                    cols[heading] = []
                    indexToName[k] = heading
                else:
                    # in this case the heading is actually just a cell
                    cols[k] = [heading]
                    indexToName[k] = k
                k += 1
        else:
            cells = line.strip().split(delim)
            k = 0
            for cell in cells:
                cell = cell.strip()
                cols[indexToName[k]] += [cell]
                k += 1
    return cols, indexToName


def reorder_matrix_columns(orderedMatrix):
    columnsNumber = len(orderedMatrix[0]) - 1 #not including students column
    columnsWeight = get_columns_weights_array(columnsNumber, orderedMatrix)
    orderedColumnsWeight = get_ordered_columns_weight(columnsNumber, columnsWeight)
    finalMatrix = sort_columns_weight(orderedColumnsWeight, orderedMatrix)
    return finalMatrix


def get_columns_weights_array(columnsNumber, orderedMatrix):
    linesNumber = len(orderedMatrix) - 1 #not including weak concepts line
    binaryArray = get_binary_array(linesNumber)
    orderedColumnsWeight = [0 for i in range(0, columnsNumber)] #fill array with 0
    for j in range(columnsNumber):
        weight = 0
        for i in range(linesNumber):
            weight += binaryArray[i] * int(orderedMatrix[i+1][j+1]) #convert string to int
        orderedColumnsWeight[j] = weight #save weight of each column
    return orderedColumnsWeight


def get_ordered_columns_weight(columnsNumber, columnsWeight):
    value = 1
    orderedColumnsWeight = [0 for i in range(0, columnsNumber)] #fill array with 0
    columnsWeightCopy = columnsWeight[:] #create columnsWeight_array copy

    while value <= columnsNumber:
        aux = 0
        lower = 2 ** 500 #REVISARRR PORQUE LA MATRIZ VERDADERA ES MUY GRANDE Y SE QUEDAN CORTOS ESOS EXPONENTES
        for i in range(0, columnsNumber):
            if columnsWeightCopy[i] < lower:
                lower = columnsWeightCopy[i]
                aux = i

        columnsWeightCopy[aux] = 2 ** 500 #REVISARRR PORQUE LA MATRIZ VERDADERA ES MUY GRANDE Y SE QUEDAN CORTOS ESOS EXPONENTES

        orderedColumnsWeight[aux] = value
        value += 1
    return orderedColumnsWeight


def sort_columns_weight(orderedColumnsWeight, orderedMatrix):
    value = 1
    columnsNumber = len(orderedMatrix[0])
    linesNumber = len(orderedMatrix)

    finalMatrix = [[0 for col in range(columnsNumber)] for row in range(linesNumber)] #fill matrix with 0

    orderedMatrix_file = os.path.join(BASE_DIR, 'files/rankorder/orderedMatrix.txt')
    openOrderedMatrixFile = open(orderedMatrix_file, 'r')
    cols, indexToName = get_columns(openOrderedMatrixFile)

    j = 0 #save first column with students
    while j < len(finalMatrix):
        finalMatrix[j][0] = cols["col0"][j]
        j += 1

    while value < columnsNumber:
        aux = 0
        upper = 0
        for i in range(0, columnsNumber-1):
            if orderedColumnsWeight[i] > upper:
                upper = orderedColumnsWeight[i]
                aux = i

        #print "upper", upper, "i=", aux

        orderedColumnsWeight[aux] = 0

        print "aux",aux,"columna", cols["col"+str(aux+1)]

        j = 0
        while j < len(finalMatrix):
            finalMatrix[j][aux+1] = cols["col" + str(aux+1)][j]
            j += 1

        value += 1

    return finalMatrix


def rank_order_algorithm():
    matrix = get_data_from_file() #data matrix

    finalMatrix = reorder_matrix_columns(orderedMatrix)

    for i in range(0, len(finalMatrix)):
        for j in range(0, len(finalMatrix[0])):
            print finalMatrix[i][j],
        print
    print
