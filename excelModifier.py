import xlwt
import xlrd
from xlutils.copy import copy
class excel():
    fileName = ''

    def __init__(self,fileName, sheetIndex):
        self.rd = xlrd.open_workbook(fileName)
        self.wt = copy(self.rd)
        self.readSheet = self.rd.sheet_by_index(sheetIndex)
        self.writeSheet = self.wt.get_sheet(sheetIndex)
        self.fileName = fileName
    
    def getValue(self,row,col):
        return self.Readsheet.cell_value(row,col)
    
    def getNumberOfRows(self):
        return self.Readsheet.nrows
    
    def getNumberOfCols(self):
        return self.Readsheet.ncols

    def addValue(self,row,col,value):
        self.writeSheet.write(row,col,value)

    def save(self):
        self.wt.save(self.fileName)
    

