from Tkinter import *
import ttk
import tkFileDialog
import threading
import time
import random
from math import *
from itertools import izip
from operator import attrgetter
import Queue



class Individual(object):
    def __init__(self, evaluation, representation):
        self.evaluation = evaluation
        self.representation = representation
        self.binary = reduce(lambda x,y: x + repr(y), representation,'')
        self.value = int(self.binary , 2)

    def __key(self):
        return (self.value)

    def __eq__(x, y):
        return x.__key() == y.__key()

    def __hash__(self):
        return hash(self.__key())

    def __repr__(self):
        return "evaluation : " + repr(self.evaluation) + " value : " + repr(self.value) + " repr: " + self.binary

class Main(Frame):

    FUNCIONS = [
    ("X^2", "1"),
    ("sin(x) *  40", "2"),
    ("cos(x) + x", "3"),
    ("(1000/abs(50 - x)) + x", "4"),
    ("(1000/abs(50 - x)) + (1000/abs(30 - x)) + (1000/abs(80 - x))  + x", "5"),
    ]

    MODES = [
    ("MAX", "1"),
    ("MIN", "2"),
    ]

    mutationProb = 0.01

    def run(self):
        t = threading.Thread(target=self.compute)
        t.start()
        self.periodicCall()

    def processIncoming(self):
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                self.area.delete('1.0', END)
                self.area.insert(END, msg)
            except Queue.Empty:
                pass

    def periodicCall(self):
        self.processIncoming()
        self.master.after(100, self.periodicCall)

    def compute(self):
        self.btn.config(state="disable")
        minVal = int(self.fromValue.get())
        maxVal = int(self.toValue.get())
        self.range = (minVal,maxVal)
        mode = self.mode.get()
        self.reverse = True
        if mode == "2":
            self.reverse = False
        sizePopulation = int(self.chromosomesValue.get())
        generations = int(self.generationsValue.get())
        self.progress["maximum"] = generations
        maxValue = [int(x) for x in bin(maxVal)[2:]]
        size =  len(maxValue)
        minValue = [int(x) for x in bin(minVal)[2:]]
        minValue = [0] * (size - len(minValue)) + minValue
        population = self.generateFirstGen(sizePopulation, size)
        population = list(set(population))
        for generation in range(generations):
            childrens = self.createChildrens(population)
            population = self.selectBetters(population + childrens, sizePopulation)
            bestFitness  = population[0].evaluation
            self.lblFitness['text'] = repr(bestFitness)
            self.progress["value"] = generation
        output = '\n'.join(map(repr, population[:10]))
        self.queue.put(output)
        self.btn.config(state="normal")
        self.progress["value"] = 0


    def generateFirstGen(self,generationSize,sizeIndividual):
        population = []
        for index in range(generationSize):
            population.append(self.generate(sizeIndividual))
        return population

    def generate(self,size):
        individual = []
        for index  in range(size):
            individual.append(random.randint(0,1))
        evaluation = self.evaluate(individual)
        if evaluation is None:
            return self.generate(size)
        return Individual(evaluation,individual)

    def crossover(self,couple):
        a = couple[0].representation
        b = couple[1].representation
        childrens = self.getChildrens(a,b)
        return childrens

    def getChildrens(self,a,b):
        childrens = []
        pivot = random.randint(1,len(a) - 1)
        children = a[0:pivot] + b[pivot:]

        evaluation = self.evaluate(children)
        if evaluation is None:
            return self.getChildrens(a,b)
        childrens.append(Individual(evaluation, children))

        children = b[0:pivot] + a[pivot:]
        evaluation = self.evaluate(children)
        childrens.append(Individual(evaluation, children))
        if evaluation is None:
            return self.getChildrens(a,b)
        return childrens

    def mutation(self, individual):
        pivot = random.randint(0,len(a) - 1)
        if individual[pivot] == 0:
            individual[pivot] = 1
        else:
            individual[pivot] = 0
        return individual

    def evaluate(self, individual):
        binary = reduce(lambda x,y: x + repr(y), individual,'')
        value = int(binary , 2)
        try:
            if value < self.range[0] or value > self.range[1]:
                return  None
            funcion = self.funcion.get()
            if funcion == "1":
                return pow(value,2)
            if funcion == "2":
                return sin(value) * 40
            if funcion == "3":
                return cos(value) + value
            if funcion == "4":
                return (1000/abs(50 - value)) + value
            if funcion == "5":
                return (1000/abs(50 - value)) + (1000/abs(30 - value)) + (1000/abs(80 - value)) + value
        except ZeroDivisionError:
            return float("inf")
        else:
            return None

    def createChildrens(self,population):
        noParents = int(len(population) / 2)
        parents = population[:noParents]
        it = iter(population)
        result = zip(it,it)
        childrens = []
        for couple in result:
            childrens = childrens + self.crossover(couple)
            if random.random() < self.mutationProb:
                mutated =  self.mutate(childrens)
                childrens = childrens + mutated
        return childrens

    def mutate(self,childrens):
        representation = childrens[0].representation
        representation[random.randint(0, len(representation) - 1)] = random.randint(0,1)
        evaluation = self.evaluate(representation)
        if evaluation is None:
            return []
        return [Individual(evaluation,representation)]

    def selectBetters(self, population, sizePopulation):
        population = list(set(population))
        population = sorted(population, key=attrgetter('evaluation'), reverse= self.reverse)
        return population[:sizePopulation]

    def initialize(self):
        self.pack(fill=BOTH, expand=True)
        self.rowconfigure(8, pad=7)

        funcion = StringVar()
        funcion.set("1")

        lbFuncion = Label(self, text="Function")
        lbFuncion.grid(sticky=W,row =0 ,column= 0)

        lbModo = Label(self, text="Modo")
        lbModo.grid(sticky=W,row =0 ,column= 3)


        for index, fun in enumerate(self.FUNCIONS):
            value = fun[1]
            text = fun[0]
            b = Radiobutton(self, text=text, variable=funcion, value=value)
            b.grid(row = 1 + index,column= 1,sticky=W)


        mode = StringVar()
        mode.set("1")

        for index, fun in enumerate(self.MODES):
            value = fun[1]
            text = fun[0]
            b = Radiobutton(self, text=text, variable=mode, value=value)
            b.grid(row = 1 + index, column= 3,sticky=W)


        lblFrom = Label(self, text="From x: ")
        lblFrom.grid(sticky=W, row= 6 ,column= 0)

        fromValue = StringVar()
        fromValue.set("0")
        entryFrom = Entry(self, textvariable=fromValue)
        entryFrom.grid(sticky=W, row= 6 ,column= 1)


        lblTo = Label(self, text="To x: ")
        lblTo.grid(sticky=W,row= 6 ,column= 3)

        toValue = StringVar()
        toValue.set("100")
        entryTo = Entry(self, textvariable=toValue)
        entryTo.grid(sticky=W,row= 6 ,column= 4)


        lblChromosomes = Label(self, text="Chromosomes: ")
        lblChromosomes.grid(sticky=W, row= 7 ,column= 0)

        chromosomesValue = StringVar()
        chromosomesValue.set("100")
        entryChromosomes = Entry(self, textvariable=chromosomesValue)
        entryChromosomes.grid(sticky=W, row= 7 ,column= 1)


        lblGenerations = Label(self, text="Generations: ")
        lblGenerations.grid(sticky=W,row= 7 ,column= 3)

        generationsValue = StringVar()
        generationsValue.set("100")
        entryGenerations = Entry(self, textvariable=generationsValue)
        entryGenerations.grid(sticky=W,row= 7 ,column= 4)

        self.progress = ttk.Progressbar(self, orient="horizontal",length=200, mode="determinate")
        self.progress.grid(sticky=W,row= 8 ,column = 0,columnspan=2)
        self.progress["value"] = 0

        lblBestFitness = Label(self, text="Best Fitness: ")
        lblBestFitness.grid(sticky=W,row= 8 ,column= 2)

        lblFitness = Label(self, text="NA")
        lblFitness.grid(sticky=W, row= 8 ,column= 3)
        self.lblFitness = lblFitness


        btn = Button(self,text="Do it", command=self.run)
        btn.grid(sticky=W,row= 8 ,column = 4)

        area = Text(self,height=12,width=100)
        area.grid(sticky=W,row= 9,column= 1,columnspan=3,rowspan=3,pady=10)


        self.btn = btn
        self.area = area
        self.fromValue = fromValue
        self.mode = mode
        self.funcion = funcion
        self.generationsValue = generationsValue
        self.chromosomesValue = chromosomesValue
        self.fromValue = fromValue
        self.toValue = toValue


    def __init__(self, master = None):
        Frame.__init__(self, master)
        Pack.config(self)
        self.master.title("P1")
        self.initialize()
        self.queue = Queue.Queue()


root = Tk()
main = Main(root)
main.mainloop()
