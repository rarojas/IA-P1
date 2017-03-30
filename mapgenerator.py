import sys
from noise import pnoise2, snoise2

f = open("map.dat", 'wt')
if len(sys.argv) > 2:
    octaves = int(sys.argv[1])
    size = int(sys.argv[2])
else:
    octaves = 4
    size = 20
freq = 1 * octaves
for y in range(size):
    cells = []
    for x in range(size):
        cells.append(repr(int(snoise2(x / freq, y / freq, octaves) * 3 + 2)))
    line = reduce(lambda x, y: x + "," + y, cells)
    f.write(line + "\n")
f.close()
