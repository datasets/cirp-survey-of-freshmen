from PyPDF2 import PdfFileWriter, PdfFileReader
import tabula
import pandas
import os
import time

class PDF:
    def __init__(self, pageNumber, output, path):
        self.pageNumber = pageNumber
        self.output = output
        self.path = path

class CSV:
    def __init__(self, pageNumber, path):
        self.pageNumber = pageNumber
        self.path = path

class Table:
    def __init__(self, pageNumber, path):
        self.pageNumber = pageNumber
        self.path = path
        self.columnNames = self.setColumnNamesByPageNumber(pageNumber)

    def setColumnNamesByPageNumber(self, pageNum):
        if pageNum in range(27,50):
            return ['', 'All Bacc Institutions', '4-yr Coll(Baccalaureate Institutions)',
            'Universities(Baccalaureate Institutions)', 'Public 4-year Colleges',
            'Private 4-year Colleges', 'Nonsec 4-year Colleges', 'Catholic 4-year Colleges',
            'Oth Relig 4-year Colleges', 'Public Universities', 'Private Universities',
            'All HBCU', 'Public HBCU', 'Private HBCU']
        elif pageNum == 55:
            return ['Institution Type', 'Strat Cell', 'Selectivity Level', 'Selectivity Average Score',
            'Institutions Population', 'Institution Survey', 'Institution Norms Sample',
            'Unweighted Number', 'Weighted Number', 'Weighted Number Men',
            'Weighted Number Women', 'Cell Wights Men', 'Cell weights Women']
        elif pageNum in range(71,78):
            return ['ACE', 'Institution', 'City', 'State', 'Stratification Cell',
            'Included in National Norms']
        elif pageNum == 82:
            return ['Unweighted size of comparison groups' , '1%', '5%', '10%',
            '15%', '20%', '25%', '30%', '35%', '40%', '45%', '50%']
        else:
            return []

    def extractTableDataFrame(self, df):
        numRows = len(df.index)
        dataFrameValuesList = []
        if len(self.columnNames) in [6, 12, 14]:
            rowOffset = 2 if len(self.columnNames) == 14 else 1
            for rowIndex in range(rowOffset, numRows):
                originRowValuesList = df.iloc[rowIndex,0:].values
                if len(self.columnNames) in [12,14]:
                    newRowValuesList = returnNewRowValuesList(originRowValuesList)
                elif len(self.columnNames) == 6:
                    newRowValuesList = list(filter(lambda x: x != '', originRowValuesList))
                else:
                    newRowValuesList = []
                dataFrameValuesList.append(newRowValuesList)
            self.dataFrame = pandas.DataFrame(dataFrameValuesList, columns = self.columnNames)

    def saveToCSV(self):
        if len(self.columnNames) != []:
            self.dataFrame.to_csv(self.path, index=False)

# This function also saves all separate PDF pages to disk
def splitDocIntoPDFObjects(pdfDocumentFilePath):
    pdfDocument = PdfFileReader(open(pdfDocumentFilePath, 'rb'))
    pdfNumberOfPages = pdfDocument.numPages
    listOfPdfObjects = []
    for pageNum in range(26, pdfNumberOfPages):
        page = pdfDocument.getPage(pageNum)
        pageOutput = PdfFileWriter()
        pageOutput.addPage(page)
        pdfPagePath = "data/page_" + str(pageNum - 4) + ".pdf"
        pdfObject = PDF(pageNumber = pageNum, output = pageOutput, path = pdfPagePath)
        with open(pdfObject.path, "wb") as outputStream:
            pageOutput.write(outputStream)
        listOfPdfObjects.append(pdfObject)
    return listOfPdfObjects

# This function also saves csv files to disk
def fromPdfCreateCsvObjects(listOfPdfObjects):
    csvObjects = []
    for pdfObject in listOfPdfObjects:
        csvFilePath = pdfObject.path.replace('.pdf', '.csv')
        csvObject = CSV(pageNumber = pdfObject.pageNumber, path = csvFilePath)
        tabula.convert_into(pdfObject.path, csvObject.path, output_format="csv")
        csvObjects.append(csvObject)
    return csvObjects

def deletePdfPagesFromDisk(pdfObjects):
    for obj in pdfObjects:
        os.remove(obj.path)

# Turns values that have ' ' between numbers into lists e.g. '0.2 0.4' --> ['0.2', '0.4']
def returnNewRowValuesList(oldRowValuesList):
    newRowValuesList = [oldRowValuesList[0]]
    for compoundValue in oldRowValuesList[1:]:
        values = str(compoundValue).split(' ')
        newRowValuesList += list(map(lambda x: x if x != 'nan' else '', values))
    return newRowValuesList


def extractTables(csvObjects):
    tables = {}
    for obj in csvObjects:
        try:
            table = Table(pageNumber = obj.pageNumber, path = obj.path)
            df = pandas.read_csv(obj.path)
            df = df.fillna('')
            table.extractTableDataFrame(df)
            tables[table.pageNumber] = table
            table.saveToCSV()
        except:
            os.remove(obj.path) # remove empty CSV file
    return tables


t0 = time.time()
pdfDocumentFilePath = 'TheAmericanFreshman2014.pdf'
pdfObjects = splitDocIntoPDFObjects(pdfDocumentFilePath)
csvObjects = fromPdfCreateCsvObjects(pdfObjects)
deletePdfPagesFromDisk(pdfObjects)
tables = extractTables(csvObjects)
print(time.time()-t0)