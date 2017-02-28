from enum import Enum
from Cell import TypeCell as tc
class TypePlayer(Enum):
    HUMAN,MOKEY,OCTUPUS,SASQUATCH = range(4)


class Player:
    costTotal = 0
    def __init(selg,typePlayer):
        self.typePlayer = typePlayer

    def move(self,typeCell):
        cost  = self.costMove[self.typePlayer][typeCell]
        if cost == None:
            return 0
        costTotal = costTotal + cost
        return cost

    costMove = {
        TypePlayer.HUMAN : { tc.MOUNTAIN : None, tc.LAND : 1, tc.WATER : 2, tc.SAND : 3, tc.FORREST : 4 },
        TypePlayer.MONKEY : { tc.MOUNTAIN : None, tc.LAND : 2, tc.WATER : 4, tc.SAND : 3, tc.FORREST : 1 }
        TypePlayer.OCTUPUS : { tc.MOUNTAIN : None, tc.LAND : 2, tc.WATER : 1, tc.SAND : None, tc.FORREST : 3 }
        TypePlayer.SASQUATCH : { tc.MOUNTAIN : 15, tc.LAND : -3, tc.WATER : None, tc.SAND : None, tc.FORREST : 4 }

    }
