from Tkinter import *
from sys import argv
from Cell import *
from Engine import *
import os,sys

class Game(Frame):
    Selected = None
    cursor = (0,0)
    position = (0,0)
    ItemList = {}
    field = []
    canvas = None
    ListboxOptionsTypeField = None
    optionsField = ["MOUNTAIN", "LAND", "WATER","SAND","FORREST"]
    size = 33
    noRows = 0
    noColumns = 0


    def saveMapToFile(self):
        pass

    def onKeyPress(self, event):
        print 'even'
        if event.keycode == Direction.UP.value:
            self.updatePosition(Direction.UP)
        if event.keycode == Direction.DOWN.value:
            self.updatePosition(Direction.DOWN)
        if event.keycode == Direction.LEFT.value:
            self.updatePosition(Direction.LEFT)
        if event.keycode == Direction.RIGHT.value:
            self.updatePosition(Direction.RIGHT)
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


    def updateInfo(self,cell):
        if cell.visited:
            self.labelInfoCellVisited["text"] = "Visitado : Si"
        else:
            self.labelInfoCellVisited["text"] = "Visitado : No"


    def onOptionsMenuSelection(self, event):
        if self.Selected != None:
            self.Selected.celltype = TypeCell(TypeCell.parse(event))
            self.canvas.itemconfig(self.Selected.itemId, fill = self.Selected.celltype)

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

    def updatePosition(self, direction):
        newPosition = None
        if direction == Direction.UP:
            y = self.position[1] - 1
            if y > -1:
                newPosition = (self.position[0],y)
        if direction == Direction.DOWN:
            y = self.position[1] + 1
            if y < self.noRows:
                newPosition = (self.position[0],y)
        if direction == Direction.LEFT:
            x = self.position[0] - 1
            if x > -1:
                newPosition = (x, self.position[1])
        if direction == Direction.RIGHT:
            x = self.position[0] + 1
            if x < self.noColumns:
                newPosition = (x,self.position[1])
        if newPosition != None:
            self.togleHighlightPosition(newPosition)


    def togleHighlightPosition(self, newPosition):
        current = self.field[self.position[1]][self.position[0]]
        current.visited = True
        self.canvas.itemconfig(current.itemId, outline="")
        new = self.field[newPosition[1]][newPosition[0]]
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


    def main(self):
        self.filename = argv[1]
        matrix = self.engine.readDataFromFile(self.filename)
        self.noRows = len(matrix)
        self.noColumns = len(matrix[0])
        self.width = (self.noColumns + 1) * self.size
        self.height = (self.noRows + 1  ) * self.size
        self.canvas = Canvas(self, width = self.width, height = self.height, bg="gray")
        self.canvas.pack(anchor=NE,side=LEFT)
        self.ListboxOptionsTypeField
        self.ListboxOptionsTypeField = StringVar(self)
        self.options = OptionMenu(self, self.ListboxOptionsTypeField, *(self.optionsField),command = self.onOptionsMenuSelection)
        self.labelInfoCellPosition = Label(self,text="")
        self.options.pack(fill="x", padx = 5, pady = 5)
        self.labelInfoCellPosition.pack(fill="x" ,padx = 5, pady = 5)
        self.labelInfoCellVisited = Label(self,text="")
        self.labelInfoCellVisited.pack(fill="x" ,padx = 5, pady = 5)
        self.master.bind("<Key>", self.onKeyPress)
        self.background_image = PhotoImage(file = os.path.join("assets","Floor.gif"))
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
                rectangle = self.canvas.create_rectangle(x,y,x1,y1, fill="black", tag = idRectangle,outline="",width="2")
                square.itemId = rectangle
                #self.canvas.create_image(x,y, image = self.background_image,anchor = NW)
                self.canvas.tag_bind(idRectangle, "<Button-1>", self.callback)
                self.ItemList[rectangle] = (i,j)
                self.field[j].append(square)
                i += 1
            j += 1

        self.togleHighlightPosition(self.position)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        Pack.config(self)
        self.engine = Engine()
        self.main()

game = Game()
game.mainloop()
