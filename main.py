from Tkinter import *
from sys import argv
from Cell import *

Selected = None
cursor = (0,0)
position = (0,0)
ItemList = {}
field = []
canvas = None
ListboxOptionsTypeField = None
optionsField = ["MOUNTAIN", "LAND", "WATER","SAND","FORREST"]
size = 50
noRows = 0
noColumns = 0

def key(event):
    if event.keycode == Direction.UP.value:
        updatePosition(Direction.UP)
    if event.keycode == Direction.DOWN.value:
        updatePosition(Direction.DOWN)
    if event.keycode == Direction.LEFT.value:
        updatePosition(Direction.LEFT)
    if event.keycode == Direction.RIGHT.value:
        updatePosition(Direction.RIGHT)

def callback(event):
    canvas = event.widget
    x = canvas.canvasx(event.x)
    y = canvas.canvasy(event.y)
    rect = canvas.find_closest(x, y)[0]
    item = ItemList[rect]
    if item != None:
        global Selected
        global Cursor
        global ListboxOptionsTypeField
        cell = field[item[1]][item[0]]
        if Selected != None:
            canvas.itemconfig(Selected.itemId,outline="")
        Selected = cell
        Cursor = (cell.i,cell.j)
        canvas.itemconfig(rect, outline="black")
        ListboxOptionsTypeField.set(optionsField[cell.celltype.valueInt()])

def onOptionsMenuSelection(event):
    if Selected != None:
        global Selected
        Selected.celltype = TypeCell(TypeCell.parse(event))
        canvas.itemconfig(Selected.itemId, fill = Selected.celltype)

def generateCoords(noRows,noColumns,canvas):
    for row in range(noRows):
        y = (row + 1) * size
        y1 = y + size
        canvas.create_rectangle( 0,y, size,y1, fill="gray")
    for col in range(noColumns):
        x = (col + 1) * size
        x1 = x + size
        canvas.create_rectangle(x,0,x1, size, fill="gray")

def updatePosition(direction):
    newPosition = None
    if direction == Direction.UP:
        y = position[1] - 1
        if y > -1:
            newPosition = (position[0],y)
    if direction == Direction.DOWN:
        y = position[1] + 1
        if y < noRows:
            newPosition = (position[0],y)
    if direction == Direction.LEFT:
        x = position[0] - 1
        if x > -1:
            newPosition = (x,position[1])
    if direction == Direction.RIGHT:
        x = position[0] + 1
        if x < noColumns:
            newPosition = (x,position[1])
    if newPosition != None:
        togleHighlightPosition(newPosition)


def togleHighlightPosition(newPosition):
    global position
    current = field[position[1]][position[0]]
    canvas.itemconfig(current.itemId, outline="")
    new = field[newPosition[1]][newPosition[0]]
    canvas.itemconfig(new.itemId, outline="black")
    position = newPosition
    revealAroundCells()

def revealAroundCells():
    vertical = range(position[1]-1, position[1]+2)
    horizontal = range(position[0]-1, position[0]+2)
    for x in horizontal:
        for y in vertical:
            revealCell(x,y)

def revealCell(x,y):
    if x > -1 and y > -1 and x < noColumns  and y < noRows:
        cell = field[y][x]
        if not cell.visible:
            canvas.itemconfig(cell.itemId,fill= cell.celltype)


def main():
    master = Tk()
    script, filename = argv
    dataFile = open(filename)
    with dataFile as stream:
        content = stream.readlines()
    global noRows
    global noColumns
    matrix = []
    for line in content:
        row = line.replace("\n","").split(',')
        matrix.append(row)
        noRows+= 1
    noColumns = len(matrix[0])
    global canvas
    width = (noColumns + 1)* size
    height = (noRows + 1) * size
    canvas = Canvas(master, width=width, height=height,bg="gray")
    canvas.pack(anchor="ne",side="left")
    global ListboxOptionsTypeField
    ListboxOptionsTypeField = StringVar(master)
    options = OptionMenu(master, ListboxOptionsTypeField, *(optionsField),command = onOptionsMenuSelection)
    options.pack(fill="x",side="left", anchor="n",expand="1")
    master.bind("<Key>", key)

    generateCoords(noRows,noColumns,canvas)

    j = 0
    for row in matrix:
        i = 0
        field.append([])
        for cell in row:
            square = Cell(i,j)
            square.celltype = TypeCell(int(cell) + 1)
            idRectangle = "rec:" + str(i) + "," + str(j)
            x =  (i  + 1 ) * size
            y =  (j  + 1 ) * size
            x1 = x + size
            y1 =  y + size
            rectangle = canvas.create_rectangle(x,y,x1,y1, fill="black", tag = idRectangle,outline="",width="2")
            square.itemId = rectangle
            canvas.tag_bind(idRectangle, "<Button-1>", callback)
            ItemList[rectangle] = (i,j)
            field[j].append(square)
            i += 1
        j += 1

    togleHighlightPosition(position)
    master.mainloop()

if __name__ == "__main__":
    main()
