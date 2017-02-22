SEPARATOR = ','
END_LINE = '\n'
EMPTY_STRING = ''

class Engine():

    def readDataFromFile(self,filename):
        matrix = []
        dataFile = open(filename)
        with dataFile as stream:
            content = stream.readlines()
        for line in content:
            row = line.replace(END_LINE,EMPTY_STRING).split(SEPARATOR)
            matrix.append(row)
        return matrix

    def createMarginMap(self):
        pass
