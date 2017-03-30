from enum import Enum
from Cell import TypeCell as tc
class TypePlayer(Enum):
    HUMAN,MONKEY,OCTUPUS,SASQUATCH = range(4)


class Player(object):
    def __init__(self,typePlayer):
        self.typePlayer = typePlayer
        self.costTotal = 0

    def move(self,typeCell):
        cost = self.costMove[self.typePlayer][typeCell]
        if cost == None:
            return 0
        self.costTotal = self.costTotal + cost
        return cost

    def costForCellType(self,typeCell):
        cost = self.costMove[self.typePlayer][typeCell]
        if cost == None:
            return 0
        return cost

    @staticmethod
    def parse(value):
        if value == "HUMAN":
            return TypePlayer.HUMAN
        if value == "MONKEY":
            return TypePlayer.MONKEY
        if value == "OCTUPUS":
            return TypePlayer.OCTUPUS
        if value == "SASQUATCH":
            return TypePlayer.SASQUATCH

    costMove = {
        TypePlayer.HUMAN : { tc.MOUNTAIN : None, tc.LAND : 1, tc.WATER : 2, tc.SAND : 3, tc.FORREST : 4 },
        TypePlayer.MONKEY : { tc.MOUNTAIN : None, tc.LAND : 2, tc.WATER : 4, tc.SAND : 3, tc.FORREST : 1 },
        TypePlayer.OCTUPUS : { tc.MOUNTAIN : None, tc.LAND : 2, tc.WATER : 1, tc.SAND : None, tc.FORREST : 3 },
        TypePlayer.SASQUATCH : { tc.MOUNTAIN : 15, tc.LAND : 3, tc.WATER : None, tc.SAND : None, tc.FORREST : 4 },
    }
