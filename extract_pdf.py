from PyPDF2 import PdfFileWriter, PdfFileReader
import tabula
import pandas
import io

def extractTablesFromPDF(pdfFilePath, startPage, endPage):
    pdfDocument = PdfFileReader(open(pdfFilePath, 'rb'))
    pdfNumPages = pdfDocument.numPages
    csvPathList = []
    for pageNum in range(startPage, endPage+1):

        page = pdfDocument.getPage(pageNum)
        pageOutput = PdfFileWriter()
        pageOutput.addPage(page)
        pdfPageFilePath = "output/page_" + str(pageNum) + ".pdf"
        csvFilePath = "output/page_" + str(pageNum) + ".csv"

        with open(pdfPageFilePath, "wb") as outputStream:
            pageOutput.write(outputStream)

        tabula.convert_into(pdfPageFilePath, csvFilePath, output_format="csv")
        csvPathList.append(csvFilePath)
    return csvPathList


# Turns values that have ' ' between numbers into lists e.g. '0.2 0.4' --> ['0.2', '0.4']
def returnNewRowValuesList(oldRowValuesList):
    newRowValuesList = [oldRowValuesList[0]]
    for value in oldRowValuesList[1:]:
        value = str(value).split(' ')
        newRowValuesList += value
    return newRowValuesList


def modifyTables(csvPathList, columns):
    for csvFilePath in csvPathList:
        originDF = pandas.read_csv(csvFilePath)
        originDF.fillna('')
        numRows = len(originDF.index)
        newValuesList = []
        for rowIndex in range(2,numRows):
            originRowValuesList = originDF.iloc[rowIndex,0:].values
            newRowValuesList = returnNewRowValuesList(originRowValuesList)
            newValuesList.append(newRowValuesList)

        newDataFrame = pandas.DataFrame(newValuesList, columns = columns)
        newDataFrame.fillna('')
        newDataFrame.to_csv(csvFilePath, index=False)

startPage, endPage = [28, 28]
pdfFilePath = 'TheAmericanFreshman2014.pdf'
csvFilePathsList = extractTablesFromPDF(pdfFilePath, startPage, endPage)
columns =  ['All Bacc Institutions', '4-yr Coll(Baccalaureate Institutions)', 'Universities(Baccalaureate Institutions)',
            'Public 4-year Colleges', 'Private 4-year Colleges', 'Nonsec 4-year Colleges',
            'Nonsec 4-year Colleges', 'Catholic 4-year Colleges', 'Oth Relig 4-year Colleges',
            'Public Universities', 'Private Universities', 'All HBCU', 'Public HBCU',
            'Private HBCU']

modifyTables(csvFilePathsList, columns)

