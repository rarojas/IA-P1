class Arbol:

    hijos = []
    deep = 0
    cost = 0
    g = 0
    h = 0
    parent = None

    def __init__(self, elemento,direction):
        self.elemento = elemento
        self.direction =  direction

    def agregarElemento(self, elemento ):
        self.hijos.append(Arbol(elemento))

    def str(self):
        return repr(self.elemento[1]) + ',' + repr(self.elemento[0])

    def f(self):
        return self.g + self.h
