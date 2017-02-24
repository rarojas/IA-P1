class nodo:
    ramas, dato = [],None

    def __init__(self, dato):
        self.hijos  = []
        self.dato = dato

class arbol:
    def __init__(self, raiz):
        self.raiz = raiz

    def agregarNodo(self, elemento, padre):
        subarbol = buscar(raiz, padre)
        subarbol.hijos.append(nodo(elemento))

    def buscar(self, arbol, elemento):
        if arbol.dato == elemento.datoa:
            return arbol
        for subarbol in arbol.hijos:
            arbolBuscado = buscar(subarbol, elemento)
            if arbolBuscado != None:
                return arbolBuscado
            return None
