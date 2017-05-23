from enum import Enum
from Cell import TypeCell as tc
class TypePlayer(Enum):
    HUMAN,MONKEY,OCTUPUS,SASQUATCH,CROC,WEREWOLF = range(6)


class Player(object):
    def __init__(self,typePlayer):
        self.typePlayer = typePlayer
        self.costTotal = 0
        self.position = (0,0)
        self.size = 33
        self.idText = None
        self.idMark = None

    def __repr__(self):
        return self.typePlayer.name + " position " + repr(self.position[0]) + ','+ repr(self.position[1])


    def getCoordsText(self):
        x = ((self.position[0] + 1) * self.size) + (self.size / 2)
        y = ((self.position[1] + 1) * self.size) + (self.size / 2)
        return (x,y)

    def getCoordsMark(self):
        x = ((self.position[0] + 1) * self.size) + (self.size / 2)
        y = ((self.position[1] + 1) * self.size) + (self.size / 2)
        r = 15
        return (x - r, y - r,x + r,y + r)

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
        if value == "CROC":
            return TypePlayer.CROC
        if value == "WEREWOLF":
            return TypePlayer.WEREWOLF

    costMove = {
        TypePlayer.HUMAN : { tc.MOUNTAIN : None, tc.LAND : 1, tc.WATER : 2, tc.SAND : 3,
                tc.FORREST : 4, tc.SWAP : 5, tc.SNOW : 5 },
        TypePlayer.MONKEY : { tc.MOUNTAIN : None, tc.LAND : 2, tc.WATER : 4, tc.SAND : 3,
                tc.FORREST : 1, tc.SWAP : 5, tc.SNOW : None },
        TypePlayer.OCTUPUS : { tc.MOUNTAIN : None, tc.LAND : 2, tc.WATER : 1, tc.SAND : None,
                tc.FORREST : 3, tc.SWAP : 2, tc.SNOW : None },
        TypePlayer.SASQUATCH : { tc.MOUNTAIN : 15, tc.LAND : 4, tc.WATER : None, tc.SAND : None,
                tc.FORREST : 4, tc.SWAP : 5, tc.SNOW : 3 },
        TypePlayer.CROC : { tc.MOUNTAIN : None, tc.LAND : 3, tc.WATER : 2, tc.SAND : 4,
                tc.FORREST : 5, tc.SWAP : 1, tc.SNOW : None },
        TypePlayer.WEREWOLF : { tc.MOUNTAIN : None, tc.LAND : 1, tc.WATER : 3, tc.SAND : 4,
                tc.FORREST : 2, tc.SWAP : None, tc.SNOW : 3 }
    }
