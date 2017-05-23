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


class Game(Frame):
    Selected = None
    cursor = (0,0)
    position = (0,0)
    ItemList = {}
    field = []
    canvas = None
    noRows = 0
    noColumns = 0
    ListboxOptionsTypeField = None
    optionsField = [typeCell.name for typeCell in list(TypeCell)]
    optionsPlayer = [typePlayer.name for typePlayer in list(TypePlayer)]
    size = 33
    height = 300
    width = 300
    Arbol = None
    Prioridad = [Direction.RIGHT, Direction.LEFT, Direction.UP, Direction.DOWN]
    startPoint = (0,0)
    finalPoint = (12,12)
    vectors = {}
    goal = None


    def initialize(self):
        self.Selected = None
        self.cursor = (0,0)
        self.position = (0,0)
        self.ItemList = {}
        self.field = []
        self.canvas = None
        self.noRows = 0
        self.noColumns = 0
        self.ListboxOptionsTypeField = None



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
            self.ListboxOptionsTypeField.set(self.optionsField[cell.celltype.value])
            self.labelInfoCellPosition["text"] = "Position : " + chr(self.Cursor[0] + 66) + repr(self.Cursor[1])
            self.updateInfo(cell)

    def updateLabels(self):
        cell = self.Selected
        self.ListboxOptionsTypeField.set(self.optionsField[cell.celltype.value])
        self.labelInfoCellPosition["text"] = "Position : " + chr(self.position[0] + 65) + repr(self.position[1])
        self.updateInfo(cell)


    def markCell(self):
        self.Selected.marked = True
        x = ((self.Selected.i + 1) * self.size) + (self.size / 2)
        y = ((self.Selected.j + 1) * self.size) + (self.size / 2)
        r = 5
        self.canvas.create_oval(x - r, y - r,x + r,y + r, outline="black", fill="black", width=2)
        self.updateInfo(self.Selected)

    def textCell(self,position, text):
        cell = self.field[position[1]][position[0]]
        cell.text = text
        x = ((cell.i + 1) * self.size) + (self.size / 2)
        y = ((cell.j + 1) * self.size) + (self.size / 2)
        if(cell.text_id is None):
            cell.text_id = self.canvas.create_text(x - 15, y - 15, anchor="nw")
        if(cell.visited):
            text = "X" + text
            fill = "red"
        else:
            fill = "green"
            text = "O" + text
        self.canvas.itemconfig(cell.text_id, text = text,font="Times 12",fill =fill)

    def updateInfo(self,cell):
        if cell.visited:
            self.labelInfoCellVisited["text"] = "Visitado : Si"
        else:
            self.labelInfoCellVisited["text"] = "Visitado : No"
        if cell.marked:
            self.labelInfoCellMark["text"] = "Marcado : Si"
        else:
            self.labelInfoCellMark["text"] = "Marcado : No"


    def onOptionsMenuSelection(self, event):
        if self.Selected != None:
            self.Selected.celltype = TypeCell(TypeCell.parse(event))
            self.canvas.itemconfig(self.Selected.itemId, fill = self.Selected.celltype)

    def onOptionsPlayerSelection(self,event):
        self.player.typePlayer = Player.parse(event)
        self.labelInfoPlayer["text"] = "Tipo " + self.player.typePlayer.name + " costo Total: " + repr(self.player.costTotal)


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

    def updateMark(self,newPosition, mark):
        x = ((newPosition[0] + 1) * self.size) + (self.size / 2)
        y = ((newPosition[1] + 1) * self.size) + (self.size / 2)
        r = 15
        newCords = (x - r, y - r,x + r,y + r)
        self.canvas.coords(mark, newCords)

    def togleHighlightPosition(self, newPosition):
        current = self.field[self.position[1]][self.position[0]]
        self.labelInfoPlayer["text"] = "Tipo " + self.player.typePlayer.name + " costo Total: " + repr(self.player.costTotal)
        current.visited = True
        new = self.field[newPosition[1]][newPosition[0]]
        self.Selected = new
        self.updateLabels()
        self.canvas.itemconfig(current.itemId, outline="")
        self.position = newPosition
        self.updateMark(newPosition,self.markPlayer)
        new.visited =  True
        self.canvas.itemconfig(new.itemId, outline="black")
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

    def start(self):
        self.remainStep = 0
        self.stepBySteps = False
        prioridad = self.listPrioridad.get(0, END)
        self.Prioridad = []
        for name in prioridad:
            self.Prioridad.append(Direction(name))

        t = threading.Thread(target=self.visitar, args=(self.arbol,))
        self.A = pgv.AGraph()
        self.A.node_attr['shape']='box'
        t.start()

    def stepByStep(self):
        self.stepBySteps = True
        self.remainStep = 0
        t = threading.Thread(target=self.visitar, args=(self.arbol,))
        t.start()

    def forward(self):
        self.remainStep = self.remainStep + 1

    def visitar(self, nodo):
        while self.remainStep == 0 and self.stepBySteps:
            time.sleep(.2)
        self.step += 1
        self.remainStep -= 1
        if self.canMove(nodo.elemento):
            self.togleHighlightPosition(nodo.elemento)
        if nodo.elemento == self.finalPoint:
            self.goal = nodo
            self.A.layout() # layout with default (neato)
            self.A.draw('simple.png')
            self.getPath()
            return nodo
        self.vectors[nodo.str()] = True
        childrens = self.getMoves(nodo.elemento)
        nodo.hijos = childrens
        self.currentNode = nodo
        if len(nodo.hijos) == 0:
            return None
        for children in nodo.hijos:
            children.parent = nodo
            self.A.add_edge(nodo.str(), children.str(), label = children.direction.name)
            result = self.visitar(children)
            if result is None:
                #Se regresa por que no hay hijos
                n = self.A.get_node(nodo.str())
                n.attr['color'] = 'red'
                self.togleHighlightPosition(nodo.elemento)
                continue
            else:
                return result

    def startSearchAnchor(self):
        self.remainStep = 0
        self.stepBySteps = False
        prioridad = self.listPrioridad.get(0, END)
        self.Prioridad = []
        for name in prioridad:
            self.Prioridad.append(Direction(name))

        t = threading.Thread(target=self.search, args=([self.arbol],))
        self.A = pgv.AGraph()
        self.A.node_attr['shape']='box'
        t.start()

    def search(self,nodes):
        childrens = []
        for nodo in nodes:
            if self.canMove(nodo.elemento):
                self.togleHighlightPosition(nodo.elemento)
            self.vectors[nodo.str()] = True
            nodo.hijos = self.getMoves(nodo.elemento)
            self.currentNode = nodo

            for children in nodo.hijos:
                children.parent = nodo
                self.A.add_edge(nodo.str(), children.str(), label = children.direction.name)
                if children.elemento == self.finalPoint:
                    self.goal = children
                    self.getPath()
                    return nodo
                childrens.append(children)
        self.search(childrens)


    def iterativeDeepSearch(self):
        self.remainStep = 0
        self.stepBySteps = False
        values = self.endPoint.get().split(",")
        self.finalPoint = (int(values[0]),int(values[1]))
        prioridad = self.listPrioridad.get(0, END)

        self.Prioridad = []
        for name in prioridad:
            self.Prioridad.append(Direction(name))

        self.deep = int(self.deepSpin.get())
        self.increment = int(self.incrementSpin.get())
        self.openNodes = { self.arbol.str() : self.arbol }
        t = threading.Thread(target=self.IDDFS, args=())
        self.A = pgv.AGraph()
        self.A.node_attr['shape']='box'
        t.start()


    def IDDFS(self):
        deep_next = self.deep
        while self.deep < 2000:
            if len(self.openNodes) == 0:
                return False
            for key, nodo in self.openNodes.copy().iteritems():
                if self.DDFS(nodo, deep_next):
                    return True
                else:
                    self.deep += self.increment
                    deep_next = self.increment


    def DDFS(self,nodo,remain_depth):
        if self.canMove(nodo.elemento):
            self.togleHighlightPosition(nodo.elemento)

        if remain_depth <= 0:
            return False

        if nodo.elemento == self.finalPoint:
            self.goal = nodo
            self.getPath()
            return True

        key = nodo.str()
        self.vectors[key] = nodo
        del self.openNodes[key]
        childrens = self.getMoves(nodo.elemento)
        nodo.hijos = childrens

        for children in nodo.hijos:
            children.parent = nodo
            childrenKey = children.str()
            self.openNodes[childrenKey] = children
            self.A.add_edge(key, childrenKey, label = children.direction.name)
            if self.DDFS(children, remain_depth - 1):
                return True
        return False


    def searchA_star(self):
        values = self.endPoint.get().split(",")
        self.finalPoint = (int(values[0]),int(values[1]))
        t = threading.Thread(target=self.A_start, args=(self.arbol, self.finalPoint))
        t.start()


    def A_start(self,src,goal):
        self.closedSet = {}
        self.openSet = {}
        self.openSet[src.str()] = src

        while len(self.openSet) > 0:
            current = self.engine.getElementWithMinF(self.openSet)
            del self.openSet[current.str()]
            if self.canMove(current.elemento):
                self.togleHighlightPosition(current.elemento)
            childrens = self.getMoves(current.elemento)
            self.textCell(current.elemento, "(" + repr(current.f())+ ")")
            if current.elemento == goal:
                    self.goal = current
                    break
            for children in childrens:
                children.parent = current
                children.g = current.g + children.cost
                children.h = self.engine.calculateDistance(children.elemento, goal)
                childrenKey = children.str()
                self.textCell(children.elemento, "(" + repr(children.f())+ ")")
                if childrenKey in self.openSet:
                    if  children.f() >= self.openSet[childrenKey].f():
                        continue
                if childrenKey in self.closedSet:
                    if children.f() >= self.closedSet[childrenKey].f():
                        continue
                self.openSet[childrenKey] = children
            self.closedSet[current.str()] = current

        if not self.goal is None:
            element = self.goal
            parents = []
            while not element.parent is None:
                self.togleHighlightPosition(element.elemento)
                self.markCell()
                time.sleep(.1)
                parents.append(element.parent)
                element = element.parent

            time.sleep(.2)
            self.togleHighlightPosition(element.elemento)
            parents.append(element)
            self.A = pgv.AGraph()
            time.sleep(1)

            self.A = pgv.AGraph()
            for children in parents:
                if not children.parent is None:
                    self.A.add_edge(children.str(), children.parent.str(), label = children.direction.name)

            self.A.layout() # layout with default (neato)
            self.A.draw('simple.png') # draw png

    def getPath(self):
        if not self.goal is None:
            element = self.goal
            parents = []
            while not element.parent is None:
                self.togleHighlightPosition(element.elemento)
                self.markCell()
                time.sleep(.1)
                parents.append(element.parent)
                element = element.parent

            time.sleep(.2)
            self.togleHighlightPosition(element.elemento)
            parents.append(element)
            #self.A = pgv.AGraph()
            time.sleep(1)

            #self.A = pgv.AGraph()
            #for children in parents:
            #    if not children.parent is None:
            #        self.A.add_edge(children.str(), children.parent.str(), label = children.direction.name)

            #self.A.layout() # layout with default (neato)
            #self.A.draw('simple.png') # draw png


    def setPositions(self):
        valuesInitialPoint = self.initialPoint.get().split(",")
        self.startPoint = (int(valuesInitialPoint[0]),int(valuesInitialPoint[1]))
        valuesEndPoint = self.endPoint.get().split(",")
        self.finalPoint = (int(valuesEndPoint[0]),int(valuesEndPoint[1]))
        self.updateMark(self.finalPoint,self.markFinal)

        self.arbol = Arbol(self.startPoint, 0)
        self.position = self.startPoint
        self.togleHighlightPosition(self.position)

    def main(self):
        matrix = self.engine.readDataFromFile(self.filename)

        self.player = Player(TypePlayer.HUMAN)
        self.noRows = len(matrix)
        self.noColumns = len(matrix[0])
        self.width = (self.noColumns + 1) * self.size
        self.height = (self.noRows + 1  ) * self.size

        self.canvas = Canvas(self, width = self.width, height = self.height, bg="gray")
        self.canvas.pack(anchor=NE,side=LEFT)

        self.ListboxOptionsTypeField = StringVar(self)
        self.options = OptionMenu(self, self.ListboxOptionsTypeField, *(self.optionsField),command = self.onOptionsMenuSelection)

        self.ListboxOptionsTypePlayer = StringVar(self)
        self.optionsTypePlayer = OptionMenu(self, self.ListboxOptionsTypePlayer, *(self.optionsPlayer),command = self.onOptionsPlayerSelection)
        self.ListboxOptionsTypePlayer.set("HUMAN")

        self.labelInfoCellPosition = Label(self,text="")
        self.options.pack(fill="x", padx = 5, pady = 5)

        self.labelInfoCellPosition.pack(fill="x" ,padx = 5, pady = 2)
        self.labelInfoCellVisited = Label(self,text="")
        self.labelInfoCellVisited.pack(fill="x" ,padx = 5, pady = 2)

        self.optionsTypePlayer.pack(fill="x", padx = 5, pady = 2)


        self.labelInfoCellMark = Label(self,text="")
        self.labelInfoCellMark.pack(fill="x" ,padx = 5, pady = 2)

        self.labelInfoPlayer = Label(self,text="")
        self.labelInfoPlayer.pack(fill="x" ,padx = 5, pady = 2)

        self.listPrioridad = DragDropListbox(self, width = 15)
        self.listPrioridad.pack()
        for direction in self.Prioridad:
            self.listPrioridad.insert(END, direction.value)


        updateBtn = Button(self,text="Update position", command=self.setPositions)
        updateBtn.pack()

        b = Button(self,text="start first depth search", command=self.start)
        b.pack()

        bSteps = Button(self, text="steps", command=self.stepByStep)
        bSteps.pack()

        bNext = Button(self, text="next", command=self.forward)
        bNext.pack()

        btnSearhcAnchor = Button(self,text="start first breadth", command=self.startSearchAnchor)
        btnSearhcAnchor.pack()

        btnIDDFS = Button(self,text="start IDDFS", command=self.iterativeDeepSearch)
        btnIDDFS.pack()

        btnAstart = Button(self,text="start A*", command=self.searchA_star)
        btnAstart.pack()


        labelStart = Label(self,text="Start point")
        labelStart.pack(fill="x" ,padx = 5, pady = 2)
        self.initialPoint = StringVar()
        e = Entry(self, textvariable=self.initialPoint)
        e.pack()
        self.initialPoint.set("0,0")

        labelEnd = Label(self,text="Final point")
        labelEnd.pack(fill="x" ,padx = 5, pady = 2)
        self.endPoint = StringVar()
        eFinal = Entry(self, textvariable=self.endPoint)
        eFinal.pack()
        self.endPoint.set("12,12")


        self.master.bind("<Key>", self.onKeyPress)
        self.generateCoords()

        labelDepth = Label(self,text="Inital depth")
        labelDepth.pack(fill="x" ,padx = 5, pady = 2)

        self.deepSpin = Spinbox(self, from_ = 1 ,to= 100000)
        self.deepSpin.pack()

        labelIncrement = Label(self,text="Increment depth")
        labelIncrement.pack(fill="x" ,padx = 5, pady = 2)

        self.incrementSpin = Spinbox(self, from_ = 0,to= 100000)
        self.incrementSpin.pack()



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
                rectangle = self.canvas.create_rectangle(x,y,x1,y1, fill="black", tag = idRectangle,outline="",width="2")
                square.itemId = rectangle
                self.canvas.tag_bind(idRectangle, "<Button-1>", self.callback)
                self.ItemList[rectangle] = (i,j)
                self.field[j].append(square)
                i += 1
            j += 1



        self.markPlayer = self.canvas.create_oval( ((self.position[0] + 1) * self.size) + self.size / 4,((self.position[1] + 1) * self.size) + self.size / 4, self.size, self.size, outline="red", fill="red", width=2)
        self.togleHighlightPosition(self.position)
        x = ((self.finalPoint[0] + 1) * self.size) + (self.size / 2)
        y = ((self.finalPoint[1] + 1) * self.size) + (self.size / 2)
        r = 15
        self.markFinal = self.canvas.create_oval( x - r,  y - r ,x + r , y + r, outline="blue", fill="blue", width=2)



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
        self.createMenubar()
        self.canvas = Canvas(self, width = self.width, height = self.height, bg="gray")
        self.canvas.pack(anchor=NE,side=LEFT)
        self.master.title("P1")
        #self.filename = "map.dat"
        #self.loadMap()

def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
Canvas.create_circle = _create_circle

game = Game()
game.mainloop()
