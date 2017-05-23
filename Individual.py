from random import shuffle,randint
from Cell import *
from Arbol import *

class Individual():

    evaluation = None
    representation = None
    costByWay = []

    def __init__(self,representation):
        self.representation = representation
        self.value = reduce(lambda x,y: repr(x) + repr(y), representation,'')

    def __key(self):
        return (self.value)

    def __eq__(x, y):
        return x.__key() == y.__key()

    def __hash__(self):
        return hash(self.__key())

    def __repr__(self):
        line = repr(self.evaluation) + " : " + repr(self.representation)
        return line




class GeneticEngine():
    generations = 500
    size =  1000
    population = []
    players = []
    objectives = []
    individualSize = None
    initPoints = []
    Prioridad = [Direction.RIGHT, Direction.LEFT, Direction.UP, Direction.DOWN]
    noRows = 0
    noColumns = 0
    cost = -1



    def __init__(self,players, objectives):
        self.players = players
        self.objectives =  objectives

    def validEvaluation(self,item):
        return not item.evaluation is None

    def searchBetterResult(self):
        self.createPopulation()
        print "\n".join(map(repr, self.population))
        return
        for generation  in range(self.generations):
            self.createChildrens()
        return self.population

    def createPopulation(self):
        self.individualSize = len(self.objectives) * 2
        for index in range(self.size):
            individual = self.createInvidividual()
            self.population.append(individual)
        self.population = filter(self.validEvaluation, self.population)
        self.population = list(set(self.population))
        self.population =  self.selectBetters(self.population)
        return self.population

    def selectBetters(self,population):
        population = list(set(population))
        population = sorted(population, key=lambda individual: individual.evaluation)
        return population


    def createInvidividual(self):
        representation = [0] * self.individualSize
        halfSize = self.individualSize / 2
        stackPlayers = [i for i in range(len(self.players))]
        shuffle(stackPlayers)
        playersAvailables = stackPlayers[:randint(1,3)]
        initPoints = len(self.initPoints) - 1

        for index in range(halfSize):
            representation[index] = playersAvailables[randint(0,len(playersAvailables) - 1)]
            representation[index + halfSize] = randint(0,initPoints)

        evaluation = self.evaluate(representation)
        individual = Individual(representation)
        individual.evaluation = evaluation
        return individual

    def createChildrens(self):
        remain = len(self.population) % 2 != 0
        parents = self.population
        newPopulation = []
        if remain:
            parents.pop()
        shuffle(parents)
        it = iter(parents)
        result = zip(it,it)
        childrens = []
        for couple in result:
            newChildrens = self.crossover(couple)
            if not newChildrens is None:
                childrens = childrens + newChildrens
            newPopulation.append(childrens)
        return childrens


    def crossover(self):
        a = couple[0].representation
        b = couple[1].representation
        return []
        childrens = self.getChildrens(a,b)
        return childrens

    def getChildrens(self,a,b):
        childrens = []
        pivot = random.randint(1,len(a) - 1)
        children = a[0:pivot] + b[pivot:]

        evaluation = self.evaluate(children)
        if evaluation is None:
            return self.getChildrens(a,b)
        childrens.append(Individual(evaluation, children))

        children = b[0:pivot] + a[pivot:]
        evaluation = self.evaluate(children)
        childrens.append(Individual(evaluation, children))
        if evaluation is None:
            return self.getChildrens(a,b)
        return childrens


    def evaluate(self,representation):
        totalCost = 0
        halfSize = self.individualSize / 2
        players = { }
        for index in range(halfSize):
            if not representation[index] in players:
                players[representation[index]] = [representation[index + halfSize], index]
            else:
                players[representation[index]].append(index)
        for idxPlayer,path in players.iteritems():
            costsByPlayer = self.costs[idxPlayer]
            path.append(7)
            for index,step in enumerate(path):
                if len(path) == (index + 1):
                    continue
                cost = costsByPlayer[step][path[index + 1]]
                if cost == -1:
                    return None
                totalCost = totalCost + cost
        return totalCost

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

    def canMove(self, newPosition):
        if newPosition is None:
            return False
        new = self.field[newPosition[1]][newPosition[0]]
        cost = self.player.costForCellType(new.celltype)
        return cost != 0

    def costMove(self,newPosition):
        if newPosition is None:
            return 0
        new = self.field[newPosition[1]][newPosition[0]]
        cost = self.player.costForCellType(new.celltype)
        return cost

    def getMoves(self, position):
        childrens = []
        for direction in self.Prioridad:
            new = self.getNewPosition(position, direction)
            if self.canMove(new):
                elemento = repr(new[1])+','+repr(new[0])
                if not (elemento in self.vectors):
                    children = Arbol(new, direction)
                    children.cost = self.costMove(new)
                    childrens.append(children)
        return childrens

    def getNewPosition(self, position, direction):
        newPosition = None
        if direction == Direction.UP:
            y = position[1] - 1
            if y > -1:
                newPosition = (position[0], y)
        if direction == Direction.DOWN:
            y = position[1] + 1
            if y < self.noRows:
                newPosition = (position[0], y)
        if direction == Direction.LEFT:
            x = position[0] - 1
            if x > -1:
                newPosition = (x, position[1])
        if direction == Direction.RIGHT:
            x = position[0] + 1
            if x < self.noColumns:
                newPosition = (x, position[1])
        return newPosition

    def runSearch(self):
        self.arbol = Arbol(self.player.position, 0)
        self.A_start(self.arbol, self.player.finalPoint)
        return self.cost


    def A_start(self,src,goal):
        self.closedSet = {}
        self.openSet = {}
        self.openSet[src.str()] = src
        self.vectors = {}
        self.cost = -1
        while len(self.openSet) > 0:
            current = self.getElementWithMinF(self.openSet)
            del self.openSet[current.str()]
            childrens = self.getMoves(current.elemento)
            if current.elemento == goal:
                    self.goal = current
                    self.arbol = current
                    self.cost = current.g
                    break
            for children in childrens:
                children.parent = current
                children.g = current.g + children.cost
                children.h = self.calculateDistance(children.elemento, goal)
                childrenKey = children.str()
                if childrenKey in self.openSet:
                    if  children.f() >= self.openSet[childrenKey].f():
                        continue
                if childrenKey in self.closedSet:
                    if children.f() >= self.closedSet[childrenKey].f():
                        continue
                self.openSet[childrenKey] = children
            self.closedSet[current.str()] = current
