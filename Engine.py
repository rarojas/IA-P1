from Player import *
from Cell import *

SEPARATOR = ','
END_LINE = '\n'
EMPTY_STRING = ''

class Engine():

    optionsField = [typeCell.name for typeCell in list(TypeCell)]
    optionsPlayer = [typePlayer.name for typePlayer in list(TypePlayer)]



    def __init__(self):
        self.player = Player(TypePlayer.HUMAN)
        self.noRows = 0
        self.noColumns = 0
        self.field = []

    def calculateDistance(self,a,b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def getElementWithMinF(self, openSet):
        if len(openSet) == 0:
            return None
        element = openSet.itervalues().next()
        for  key,node in openSet.iteritems():
            if node.f() < element.f():
                element = node
        return element

    def readDataFromFile(self,filename):
        self.matrix = []
        dataFile = open(filename)
        with dataFile as stream:
            content = stream.readlines()
        for line in content:
            row = line.replace(END_LINE,EMPTY_STRING).split(SEPARATOR)
            self.matrix.append(row)
        return self.matrix

    def saveMapToFile(self):
        data = []
        for row in self.field:
            rowData = ""
            for cell in row:
                rowData = rowData + "," + repr(cell.celltype.value)
                rowData = rowData[1:]
                data.append(rowData)
        with tkFileDialog.asksaveasfile('w', defaultextension='.dat') as file:
            file.write("\n".join(data))
