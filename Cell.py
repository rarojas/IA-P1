from enum import Enum

class Direction(Enum):
    UP = 111
    DOWN = 116
    LEFT = 113
    RIGHT = 114

class TypeCell(Enum):
    MOUNTAIN,LAND, WATER, SAND,FORREST,WALL = range(6)

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
        if self is  TypeCell.WALL:
            return 'black'

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
        if value == "WALL":
            return TypeCell.WALL


class Cell(object):
    size = 50
    celltype = TypeCell( TypeCell.MOUNTAIN)
    visited = False
    visible = False
    itemId = None

    def __init__(self, i,j):
        self.i = i
        self.j = j
