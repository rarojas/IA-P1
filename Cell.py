class TypeCell:
    MOUNTAIN,LAND, WATER, SAND,FORREST = range(5)
    def __init__(self, Type):
        self.value = Type

    def __str__(self):
        if self.value == TypeCell.MOUNTAIN:
            return 'gray'
        if self.value == TypeCell.LAND:
            return 'brown'
        if self.value == TypeCell.WATER:
            return 'blue'
        if self.value == TypeCell.SAND:
            return 'yellow'
        if self.value == TypeCell.FORREST:
            return 'green'
    @staticmethod
    def parse(value):
        if value == "MOUNTAIN":
            return TypeCell.MOUNTAIN
        if value == "LAND":
            return TypeCell.LAND
        if value == "WATER":
            return TypeCell.WATER
        if value == "SAND":
            return TypeCell.SAND
        if value == "FORREST":
            return TypeCell.FORREST



    def __eq__(self,y):
       return self.value==y.value


class Cell(object):
    size = 50
    celltype = TypeCell( TypeCell.MOUNTAIN)
    visited = None
    visisible = False
    itemId = None

    def __init__(self, i,j):
        self.i = i
        self.j = j
