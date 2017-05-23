from Tkinter import *
import tkFileDialog
from Engine import *
import sys
from Player import *
from DragDropListbox import *
from Arbol import *
import threading
import pygraphviz as pgv
import time
import Queue
from Table import *
from Individual import *
import logging

logger = logging.getLogger('practice2')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())




class Game(Frame):
    Selected = None
    cursor = (0,0)
    position = (0,0)
    ItemList = {}
    field = []
    canvas = None
    noRows = 0
    noColumns = 0
    size = 33
    height = 300
    width = 300
    Arbol = None
    Prioridad = [Direction.RIGHT, Direction.LEFT, Direction.UP, Direction.DOWN]
    startPoint = (0,0)
    finalPoint = (5,2)
    vectors = {}
    goal = None
    monkey = None
    human = None
    octupus = None
    portal = (10,9)
    stone = (14,3)
    key = (13,14)
    temple = (7,6)
    friend = (14,6)
    exit = (8,10)
    optionsField = [typeCell.name for typeCell in list(TypeCell)]
    initPoints = [(1,9),(2,13),(4,13)]



    def initialize(self):
        self.Selected = None
        self.cursor = (0,0)
        self.position = (0,0)
        self.ItemList = {}
        self.field = []
        self.canvas = None
        self.noRows = 0
        self.noColumns = 0

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


    def onKeyPress(self, event):
        if event.keysym == 'o':
            self.markCell()
        if event.keysym == Direction.UP.value:
            self.updatePosition(self.position,Direction.UP)
        if event.keysym == Direction.DOWN.value:
            self.updatePosition(self.position,Direction.DOWN)
        if event.keysym == Direction.LEFT.value:
            self.updatePosition(self.position,Direction.LEFT)
        if event.keysym == Direction.RIGHT.value:
            self.updatePosition(self.position,Direction.RIGHT)
        if event.keysym == 'Escape':
            self.destroy()
            sys.exit()

    def callback(self,event):
        canvas = event.widget
        x = canvas.canvasx(event.x)
        y = canvas.canvasy(event.y)
        rect = canvas.find_closest(x, y)[0]
        item = self.ItemList[rect]
        if item != None:
            cell = self.field[item[1]][item[0]]
            if self.Selected != None:
                self.canvas.itemconfig(self.Selected.itemId,outline="")
            self.Selected = cell
            self.Cursor = (cell.i,cell.j)
            self.canvas.itemconfig(rect, outline="black")

    def markCell(self):
        self.Selected.marked = True
        x = ((self.Selected.i + 1) * self.size) + (self.size / 2)
        y = ((self.Selected.j + 1) * self.size) + (self.size / 2)
        r = 5
        color =  "black"
        if self.player.typePlayer == TypePlayer.MONKEY:
            color = "brown"
        if self.player.typePlayer == TypePlayer.OCTUPUS:
            color = "white"
        self.canvas.create_oval(x - r, y - r,x + r,y + r, outline=color, fill=color, width=2)

    def textCell(self,position, text):
        cell = self.field[position[1]][position[0]]
        cell.text = text
        x = ((cell.i + 1) * self.size) + (self.size / 2)
        y = ((cell.j + 1) * self.size) + (self.size / 2)
        if(cell.text_id is None):
            cell.text_id = self.canvas.create_text(x - 15, y - 15, anchor="nw")
        self.canvas.itemconfig(cell.text_id, text = text,font="Times 12",fill = fill)

    def generateCoords(self):
        halfSize = self.size / 2
        for row in range(self.noRows):
            y = (row + 1) * self.size
            y1 = y + self.size
            self.canvas.create_rectangle(0, y, self.size, y1, fill="gray")
            self.canvas.create_text(halfSize, y + halfSize, text = repr(row), width = self.size)

        for col in range(self.noColumns):
            x = (col + 1) * self.size
            x1 = x + self.size
            self.canvas.create_rectangle(x, 0, x1, self.size, fill="gray")
            self.canvas.create_text(x + halfSize, halfSize, text = chr(col + 65), width = self.size)

    def updatePosition(self,position,direction):
        newPosition = self.getNewPosition(position, direction)
        if self.canMove(newPosition):
            self.togleHighlightPosition(newPosition)

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

    def togleHighlightPosition(self, newPosition):
        current = self.field[self.position[1]][self.position[0]]
        current.visited = True
        self.canvas.itemconfig(current.itemId, outline="")
        new = self.field[newPosition[1]][newPosition[0]]
        self.Selected = new
        self.player.position = newPosition
        self.canvas.coords(self.player.idText, self.player.getCoordsText()[0],self.player.getCoordsText()[1])
        new.visited =  True
        self.canvas.itemconfig(new.itemId, outline="black")
        self.position = newPosition
        self.revealAroundCells()

    def revealAroundCells(self):
        vertical = range(self.position[1]-1, self.position[1] + 2)
        horizontal = range(self.position[0]-1, self.position[0] + 2)
        for x in horizontal:
            for y in vertical:
                self.revealCell(x,y)

    def revealCell(self, x,y):
        if x > -1 and y > -1 and x < self.noColumns  and y < self.noRows:
            cell = self.field[y][x]
            if not cell.visible:
                self.canvas.itemconfig(cell.itemId,fill= cell.celltype)
                cell.visible = True

    def revealOneCell(self, position):
        cell = self.field[position[1]][position[0]]
        if not cell.visible:
            self.canvas.itemconfig(cell.itemId, fill= cell.celltype)
            cell.visible = True

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


    def searchA_star(self):
        self.players = [self.human,self.octupus,self.monkey,self.sasquatch,self.croc,self.werewolf]
        self.subgoals = [self.stone, self.temple, self.key, self.friend]
        self.geneticEngine.players = self.players
        self.geneticEngine.objectives = self.subgoals
        self.geneticEngine.initPoints = self.initPoints
        self.geneticEngine.exit = self.portal

        self.queue = Queue.Queue()
        masterThread = threading.Thread(target=self.runSearches, args=(self.players, self.subgoals))
        masterThread.start()
        self.master.after(100, self.process_queue)


    def process_queue(self):
        try:
            msg = self.queue.get(0)
        except Queue.Empty:
            self.master.after(100, self.process_queue)

    def findPath(self):
        self.geneticEngine.runSearch()

    def runSearches(self,players,subgoals):
        self.results = []
        self.paths = []
        self.costs = []
        logger.info('Running')
        arrivePoints = subgoals +  self.initPoints + [self.portal]
        for idxPlayer, player in enumerate(players):
            self.results.append([])
            self.paths.append([])
            costByPlayer = []
            for idxSubgoal, subgoal in enumerate(arrivePoints):
                costBySubgoal = []
                for idxInitPoints, initPoint in enumerate(arrivePoints):
                    player.initialPosition = initPoint
                    player.position = player.initialPosition
                    player.finalPoint = subgoal
                    self.geneticEngine.player = player
                    t = threading.Thread(target = self.findPath)
                    t.start()
                    t.join()
                    costBySubgoal.append(self.geneticEngine.cost)
                costByPlayer.append(costBySubgoal)
            self.costs.append(costByPlayer)

        self.geneticEngine.costs = self.costs

        logger.info('costos')
        for idxPlayer, costByPlayer in enumerate(self.costs):
            logger.info(players[idxPlayer])
            for costByPath in costByPlayer:
                logger.info(costByPath)

        self.geneticEngine.searchBetterResult()
        self.queue.put("Task finished")


    def drawPath(self,arbol):
        if not arbol is None:
            element = arbol
            parents = []
            while not element.parent is None:
                time.sleep(.2)
                self.togleHighlightPosition(element.elemento)
                parents.append(element.parent)
                element = element.parent
                self.markCell()
            self.markCell()
            self.togleHighlightPosition(element.elemento)
            parents.append(element)
            self.A = pgv.AGraph()
            for children in parents:
                if not children.parent is None:
                    self.A.add_edge(children.str(), children.parent.str(), label = children.direction.name)
            self.A.layout()
            self.A.draw('simple.png')

    def onOptionsMenuSelection(self, event):
        if self.Selected != None:
            self.Selected.celltype = TypeCell(TypeCell.parse(event))
            self.canvas.itemconfig(self.Selected.itemId, fill = self.Selected.celltype)

    def main(self):
        matrix = self.engine.readDataFromFile(self.filename)

        self.monkey = Player(TypePlayer.MONKEY)
        self.monkey.initialPosition = (4,13)
        self.human = Player(TypePlayer.HUMAN)
        self.human.initialPosition = (2,13)
        self.octupus = Player(TypePlayer.OCTUPUS)
        self.octupus.initialPosition = (1,9)
        self.croc = Player(TypePlayer.CROC)
        self.sasquatch = Player(TypePlayer.SASQUATCH)
        self.werewolf = Player(TypePlayer.WEREWOLF)


        self.noRows = len(matrix)
        self.noColumns = len(matrix[0])

        self.geneticEngine.noColumns = self.noColumns
        self.geneticEngine.noRows = self.noRows

        self.width = (self.noColumns + 1) * self.size
        self.height = (self.noRows + 1  ) * self.size

        self.canvas = Canvas(self, width = self.width, height = self.height, bg="gray")
        self.canvas.pack(anchor=NE,side=LEFT)
        self.generateCoords()

        j = 0
        for row in matrix:
            i = 0
            self.field.append([])
            for cell in row:
                square = Cell(i,j)
                square.celltype = TypeCell(int(cell))
                idRectangle = "rec:" + str(i) + "," + str(j)
                x =  (i  + 1 ) * self.size
                y =  (j  + 1 ) * self.size
                x1 = x + self.size
                y1 =  y + self.size
                rectangle = self.canvas.create_rectangle(x,y,x1,y1, fill=square.celltype, tag = idRectangle,outline="",width="2")
                square.itemId = rectangle
                self.canvas.tag_bind(idRectangle, "<Button-1>", self.callback)
                self.ItemList[rectangle] = (i,j)
                self.field[j].append(square)
                i += 1
            j += 1

        self.geneticEngine.field = self.field

        btnAstart = Button(self,text="start A*", command=self.searchA_star)
        btnAstart.pack()

        t = SimpleTable(self)
        t.pack(side="top", fill="x")
        t.set(0,0,"")
        t.set(1,0,self.human.typePlayer.name)
        t.set(2,0,self.octupus.typePlayer.name)
        t.set(3,0,self.monkey.typePlayer.name)
        t.set(0,1,"I-S")
        t.set(0,2,"I-S-P")
        t.set(0,3,"I-T")
        t.set(0,4,"I-T-P")
        t.set(0,5,"I-K")
        t.set(0,6,"I-K-P")
        self.table = t

        self.ListboxOptionsTypeField = StringVar(self)
        self.options = OptionMenu(self, self.ListboxOptionsTypeField, *(self.optionsField),command = self.onOptionsMenuSelection)


        btnReset = Button(self,text="Reset", command=self.reset)
        btnReset.pack()

        self.options.pack(fill="x", padx = 5, pady = 5)

        labelHuman = Label(self,text="Human Initial Point")
        labelHuman.pack(fill="x" ,padx = 5, pady = 2)
        self.humanPoint = StringVar()
        entryHuman = Entry(self, textvariable = self.humanPoint)
        entryHuman.pack()
        self.humanPoint.set("4,13")

        labelMonkey = Label(self,text="Monkey Initial Point")
        labelMonkey.pack(fill="x" ,padx = 5, pady = 2)
        self.monkeyPoint = StringVar()
        entryMonkey = Entry(self, textvariable = self.monkeyPoint)
        entryMonkey.pack()
        self.monkeyPoint.set("2,13")

        labelOctupus = Label(self,text="Octupus Initial Point")
        labelOctupus.pack(fill="x" ,padx = 5, pady = 2)
        self.octupusPoint = StringVar()
        entryOctupus = Entry(self, textvariable = self.octupusPoint)
        entryOctupus.pack()
        self.octupusPoint.set("1,9")

        labelPortal = Label(self,text="Portal Initial Point")
        labelPortal.pack(fill="x" ,padx = 5, pady = 2)
        self.portalPoint = StringVar()
        entryPortal = Entry(self, textvariable = self.portalPoint)
        entryPortal.pack()
        self.portalPoint.set("10,9")

        labelKey = Label(self,text="Key Point")
        labelKey.pack(fill="x" ,padx = 5, pady = 2)
        self.keyPoint = StringVar()
        entryKey = Entry(self, textvariable = self.keyPoint)
        entryKey.pack()
        self.keyPoint.set("13,14")

        labelTemple = Label(self,text="Temple Point")
        labelTemple.pack(fill="x" ,padx = 5, pady = 2)
        self.templePoint = StringVar()
        entryTemple = Entry(self, textvariable = self.templePoint)
        entryTemple.pack()
        self.templePoint.set("7,6")

        labelStone = Label(self,text="Stone  Point")
        labelStone.pack(fill="x" ,padx = 5, pady = 2)
        self.stonePoint = StringVar()
        entryStone = Entry(self, textvariable = self.stonePoint)
        entryStone.pack()
        self.stonePoint.set("14,2")


        labelFriend = Label(self,text="Friend  Point")
        labelFriend.pack(fill="x" ,padx = 5, pady = 2)
        self.friendPoint = StringVar()
        entryFriend = Entry(self, textvariable = self.friendPoint)
        entryFriend.pack()
        self.friendPoint.set("14,6")


        self.idPortal = self.canvas.create_text(self.getCoordsText(self.portal), text="P")

        self.idKey = self.canvas.create_text(self.getCoordsText(self.key), text="K")
        self.idStone = self.canvas.create_text(self.getCoordsText(self.stone), text="S")
        self.idTemple = self.canvas.create_text(self.getCoordsText(self.temple), text="T")
        self.idFriend = self.canvas.create_text(self.getCoordsText(self.friend), text="F")

        self.initPointsIds = []
        for idx, initialPosition in enumerate(self.initPoints):
            self.initPointsIds.append(self.canvas.create_text(self.getCoordsText(initialPosition), text=repr(idx)))


        self.initializePlayers()

    def reset(self):
        self.initializePlayers()


    def initializePlayers(self):
        point = self.portalPoint.get().split(",")
        self.portal = (int(point[0]), int(point[1]))
        point = self.keyPoint.get().split(",")
        self.key = (int(point[0]), int(point[1]))
        point = self.templePoint.get().split(",")
        self.temple = (int(point[0]), int(point[1]))
        point = self.stonePoint.get().split(",")
        self.stone = (int(point[0]), int(point[1]))
        point = self.friendPoint.get().split(",")
        self.friend = (int(point[0]), int(point[1]))

        point = self.stonePoint.get().split(",")
        self.stone = (int(point[0]), int(point[1]))
        self.objectives = [self.portal,self.key,self.temple,self.friend]


        self.canvas.coords(self.idPortal,self.getCoordsText(self.portal))
        self.revealOneCell(self.portal)
        self.canvas.coords(self.idKey,self.getCoordsText(self.key))
        self.revealOneCell(self.key)
        self.canvas.coords(self.idTemple,self.getCoordsText(self.temple))
        self.revealOneCell(self.temple)
        self.canvas.coords(self.idStone,self.getCoordsText(self.stone))
        self.revealOneCell(self.stone)
        self.canvas.coords(self.idFriend,self.getCoordsText(self.friend))
        self.revealOneCell(self.friend)


    def getCoordsText(self, position):
        x = ((position[0] + 1) * self.size) + (self.size / 2)
        y = ((position[1] + 1) * self.size) + (self.size / 2)
        return (x,y)

    def selectFile(self):
        fname = tkFileDialog.askopenfilename()
        if fname:
            self.filename = fname
            self.loadMap()


    def loadMap(self):
        for child in self.winfo_children():
            child.destroy()
        self.createMenubar()
        self.initialize()
        self.main()
        self.arbol = Arbol(self.startPoint, 0)
        self.step = 0
        self.currentNode = self.arbol


    def createMenubar(self):
        self.menubar = Menu(self)
        filemenu = Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="Open",command=self.selectFile)
        filemenu.add_command(label="Save",command=self.saveMapToFile)
        filemenu.add_separator()
        filemenu.add_command(label="Exit",command=self.quit)
        self.menubar.add_cascade(label="File", menu=filemenu)

        try:
            self.master.config(menu =self.menubar)
        except AttributeError:
            self.master.tk.call(master,"config", "-menu",self.menubar)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        Pack.config(self)
        self.engine = Engine()
        self.geneticEngine = GeneticEngine([],[])
        self.createMenubar()
        self.canvas = Canvas(self, width = self.width, height = self.height, bg="gray")
        self.canvas.pack(anchor=NE,side=LEFT)
        self.master.title("P1")
        self.filename = "pratice.dat"
        self.loadMap()

def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
Canvas.create_circle = _create_circle

game = Game()
game.mainloop()
