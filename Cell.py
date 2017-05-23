from enum import Enum

class Direction(Enum):
    UP = 'Up'
    DOWN = 'Down'
    LEFT = 'Left'
    RIGHT = 'Right'

class TypeCell(Enum):
    MOUNTAIN,LAND, WATER, SAND,FORREST,SWAP,SNOW = range(7)

    def __str__(self):
        if self is TypeCell.MOUNTAIN:
            return 'gray'
        if self is TypeCell.LAND:
            return '#c47d01'
        if self is TypeCell.WATER:
            return 'blue'
        if self is  TypeCell.SAND:
            return 'brown'
        if self is  TypeCell.FORREST:
            return 'green'
        if self is  TypeCell.SWAP:
            return 'purple'
        if self is  TypeCell.SNOW:
            return 'white'

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
        if value == "SWAP":
            return TypeCell.SWAP
        if value == "SNOW":
            return TypeCell.SNOW



class Cell(object):
    size = 50
    celltype = TypeCell(TypeCell.MOUNTAIN)
    visited = False
    visible = False
    marked = False
    itemId = None
    text_id = None
    cost = 0
    g = 0
    h = 0

    def f(self):
        return self.g + self.h

    def __init__(self, i,j):
        self.i = i
        self.j = j
