from Tkinter import *
import tkFileDialog
from sys import argv
from Cell import *
from Engine import *
import os,sys
from Player import *

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
    width =300

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
            self.updatePosition(Direction.UP)
        if event.keysym == Direction.DOWN.value:
            self.updatePosition(Direction.DOWN)
        if event.keysym == Direction.LEFT.value:
            self.updatePosition(Direction.LEFT)
        if event.keysym == Direction.RIGHT.value:
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
        new = self.field[newPosition[1]][newPosition[0]]
        cost = self.player.move(new.celltype)
        self.labelInfoPlayer["text"] = "Tipo " + self.player.typePlayer.name + " costo Total: " + repr(self.player.costTotal)
        if cost == 0:
            self.updateLabels()
            return
        current.visited = True
        self.Selected = new
        self.updateLabels()
        self.canvas.itemconfig(current.itemId, outline="")
        x = ((newPosition[0] + 1) * self.size) + (self.size / 2)
        y = ((newPosition[1] + 1) * self.size) + (self.size / 2)
        r = 15
        newCords = (x - r, y - r,x + r,y + r)
        self.canvas.coords(self.markPlayer, newCords)
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

        self.labelInfoCellPosition.pack(fill="x" ,padx = 5, pady = 5)
        self.labelInfoCellVisited = Label(self,text="")
        self.labelInfoCellVisited.pack(fill="x" ,padx = 5, pady = 5)

        self.optionsTypePlayer.pack(fill="x", padx = 5, pady = 5)

        self.labelInfoCellMark = Label(self,text="")
        self.labelInfoCellMark.pack(fill="x" ,padx = 5, pady = 5)

        self.labelInfoPlayer = Label(self,text="")
        self.labelInfoPlayer.pack(fill="x" ,padx = 5, pady = 5)

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
                self.canvas.tag_bind(idRectangle, "<Button-1>", self.callback)
                self.ItemList[rectangle] = (i,j)
                self.field[j].append(square)
                i += 1
            j += 1
        self.markPlayer = self.canvas.create_oval( ((self.cursor[0] + 1) * self.size) + self.size / 4,((self.cursor[0] + 1) * self.size) + self.size / 4, self.size, self.size, outline="red", fill="red", width=2)
        self.togleHighlightPosition(self.position)


    def loadMap(self):
        fname =  tkFileDialog.askopenfilename()
        if fname:
            self.filename = fname
            for child in self.winfo_children():
                child.destroy()
            self.createMenubar()
            self.initialize()
            self.main()

    def createMenubar(self):
        self.menubar = Menu(self)
        filemenu = Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="Open",command=self.loadMap)
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

def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
Canvas.create_circle = _create_circle

game = Game()
game.mainloop()
