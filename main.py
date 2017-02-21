from Tkinter import *
from sys import argv
from Cell import *

Selected = None
cursor = (0,0)
ItemList = {}
field = []
canvas = None


def key(event):
    print "pressed", repr(event.char)
    #if(event.char == '')

def callback(event):
    print "clicked at", event.x, event.y
    canvas = event.widget
    x = canvas.canvasx(event.x)
    y = canvas.canvasy(event.y)
    rect = canvas.find_closest(x, y)[0]

    item = ItemList[rect]
    if item != None:
        global Selected
        global Cursor
        cell = field[item[0]][item[1]]
        if Selected != None:
            canvas.itemconfig(Selected.itemId, outline="")
        Selected = cell
        Cursor = (cell.i,cell.j)
        canvas.itemconfig(rect, outline="black")

def onOptionsMenuSelection(event):
    if Selected != None:
        global Selected
        Selected.celltype = TypeCell(TypeCell.parse(event))
        canvas.itemconfig(Selected.itemId, fill = Selected.celltype)


def main():
    master = Tk()
    script, filename = argv
    dataFile = open(filename)
    with dataFile as stream:
        content = stream.readlines()
    noRows = 0
    noColumns = 0
    size = 50
    matrix = []
    for line in content:
        row = line.replace("\n","").split(',')
        matrix.append(row)
        noRows+= 1
    global canvas
    canvas = Canvas(master, width=600, height=600)
    canvas.pack()

    variable = StringVar(master)
    optionsField = ["MOUNTAIN", "LAND", "WATER","SAND","FORREST"]
    options = OptionMenu(master, variable, *(optionsField),command = onOptionsMenuSelection)
    options.pack()
    canvas.bind("<Key>", key)

    i = 0
    for row in matrix:
        j = 0
        field.append([])
        for cell in row:
            square = Cell(i,j)
            square.celltype = TypeCell(int(cell) + 1)
            idRectangle = "rec:" + str(i) + "," + str(j)
            rectangle = canvas.create_rectangle(i * size, j * size , ((1 + i) * size) , ((1 + j) * size ) , fill= square.celltype, tag = idRectangle, outline = "")
            square.itemId = rectangle
            canvas.tag_bind(idRectangle, "<Button-1>", callback)
            ItemList[rectangle] = (i,j)
            field[i].append(square)
            j += 1
        i += 1


    master.mainloop()

if __name__ == "__main__":
    main()
