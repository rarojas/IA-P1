from Tkinter import *
from sys import argv
master = Tk()
script, filename = argv
dataFile = open(filename)
with dataFile as stream:
    content = stream.readlines()

noRows = 0
noColumns = 0
Matrix = [[]]
for line in content:
    row = line.replace("\n").split(',')
    print row

w = Canvas(master, width=600, height=600)
w.pack()
w.create_rectangle(50, 25, 150, 75, fill="blue")




mainloop()
