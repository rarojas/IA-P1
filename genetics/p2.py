from Tkinter import *
import ttk
import tkFileDialog
import threading
import time
from math import *
from itertools import izip
from operator import attrgetter,itemgetter
import random
import Queue



class Article(object):
    def __init__(self,number,weight, importance, existences,_type):
        self.number = number
        self.weight = weight
        self.importance = importance
        self.existences =  existences
        self.type = _type

    def __repr__(self):
        return repr(self.number) + " " + repr(self.weight) + " " + repr(self.importance) + " " + repr(self.existences) + " " + repr(self.type)



class Individual(object):
    def __init__(self,evaluation,representation):
        self.evaluation = evaluation
        self.representation = representation
        self.value = reduce(lambda x,y: repr(x) + repr(y), representation,'')

    def __key(self):
        return (self.value)

    def __eq__(x, y):
        return x.__key() == y.__key()

    def __hash__(self):
        return hash(self.__key())

    def __repr__(self):
        return repr(self.evaluation) + " : " + repr(self.representation)



class Main(Frame):

    mutationProb = 0.001

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


    def validEvaluation(self,item):
        return not item.evaluation is None

    def selectBetters(self, population, sizePopulation):
        population = list(set(population))
        population = sorted(population, key=lambda individual: individual.evaluation[0],reverse=True)
        return population[:sizePopulation]


    def compute(self):
        self.btn.config(state="disable")
        generations = int(self.entryGenerations.get())
        self.MAX_WEIGHT = int(self.entryWeight.get())
        sizePopulation = int(self.entryIndividuals.get())
        sizeChildrens = int(self.entryReproduction.get())
        self.progress["maximum"] = generations
        if self.ByType.get() == 1:
            return self.computeByType(sizePopulation)

        population =  self.createFirstGeneration(sizePopulation)
        population = filter(self.validEvaluation, population)
        population = list(set(population))
        for generation in range(generations):
            childrens = self.createChildrens(population,sizeChildrens)
            childrens = filter(self.validEvaluation, childrens)
            population = self.selectBetters(population + childrens, sizePopulation)
            bestFitness  = population[0].evaluation
            self.lblFitness['text'] = repr(bestFitness)
            self.progress["value"] = generation

        output = '\n'.join(map(repr,population))
        self.queue.put(output)
        self.btn.config(state="normal")
        self.progress["value"] = 0
        #self.area.delete('1.0', END)
        #self.area.insert(END, output)

    def computeByType(self,sizePopulation):
        population = self.createFirstGenerationByRulesType(sizePopulation)
        generations = int(self.entryGenerations.get())
        sizeChildrens = int(self.entryReproduction.get())

        for generation in range(generations):
            childrens = self.createChildrensByRules(population,sizeChildrens)
            childrens = filter(self.validEvaluation, childrens)
            population = self.selectBetters(population, sizePopulation)
            bestFitness  = population[0].evaluation
            self.lblFitness['text'] = repr(bestFitness)
            self.progress["value"] = generation

        self.btn.config(state="normal")
        self.progress["value"] = 0
        output = '\n'.join(map(repr,population))
        self.queue.put(output)


    def createChildrensByRules(self,population, pairs):
        noParents = pairs * 2
        parents = population[:noParents]
        populationByType = [[]] * len(self.rules)
        newPopulation = []
        for individual in population:
            populationByType[individual.representation[0]].append(individual)

        for breed in populationByType:
            sizeBreed = len(breed)
            if sizeBreed < 2:
                continue
            random.shuffle(breed)
            it = iter(breed)
            result = zip(it,it)
            childrens = []
            for couple in result:
                newChildrens = self.crossoverByType(couple)
                if not newChildrens is None:
                    childrens = childrens + newChildrens
            newPopulation.append(childrens)
        return childrens

    def crossoverByType(self,couple):
        a = couple[0].representation
        b = couple[1].representation
        if b is None:
            return  None
        childrens = self.getChildrensByType(a,b)
        if random.random() < self.mutationProb:
            mutated =  self.mutateByType(childrens)
            childrens = childrens + mutated
        return childrens


    def mutateByType(self,childrens):
        representation = childrens[0].representation
        idxArticle = random.randint(0,len(representation) - 2)
        rule = self.rules[representation[0]]
        article = self.articles[idxArticle]
        if not article.type in rule:
            return []

        representation[idxArticle] = random.randint(0,article.existences)
        evaluation = self.evaluateByType(representation)
        if evaluation is None:
            return []
        print 'mutation'
        return [Individual(evaluation,representation)]

    def getChildrensByType(self,a,b):
        childrens = []
        pivot = random.randint(2,len(a) - 1)
        children = a[0:pivot] + b[pivot:]

        evaluation = self.evaluateByType(children)
        #if evaluation is None:
        #    return self.getChildrens(a,b)
        childrens.append(Individual(evaluation, children))

        children = b[0:pivot] + a[pivot:]
        evaluation = self.evaluateByType(children)
        childrens.append(Individual(evaluation, children))
        #if evaluation is None:
        #    return self.getChildrens(a,b)
        return childrens

    def createFirstGenerationByRulesType(self,sizePopulation):
        self.rules = [['Liquid','Food'],['Document','Electronic'],['Food','Electronic']]
        self.types = []
        for populationType in self.rules:
            articlesByRule = []
            for noArticle,article in enumerate(self.articles):
                if article.type in populationType:
                    articlesByRule.append((noArticle + 1, article))
            self.types.append(articlesByRule)

        size = len(self.articles)
        population = []
        for (populationType,rules)  in enumerate(self.types):
            for index in range(sizePopulation):
                individual = self.createRandomIndividualByRules(size,(populationType,rules))
                if not individual.evaluation is None :
                    population.append(individual)
        return population

    def createRandomIndividualByRules(self,size, rules, timeout = 300):
        representation = [0] * (size + 1)
        representation[0] = rules[0]
        for articleInfo in rules[1]:
            if(self.ByExitence.get() == 1):
                value =  random.randint(0,articleInfo[1].existences)
            else:
                value =  random.randint(0,1)
            representation[articleInfo[0]] = value

        evaluation = self.evaluateByType(representation)
        if evaluation is None and timeout > 0:
            self.createRandomIndividualByRules(size, rules,timeout = timeout - 1)
        individual = Individual(evaluation,representation)
        return individual



    def evaluateByType(self,representation):
        representation = representation[1:]
        importance = reduce(self.importance,  zip(representation,self.articles), 0)
        weight = reduce(self.weight,  zip(representation,self.articles), 0)
        if weight > self.MAX_WEIGHT:
            return None
        return (importance,weight)

    def createChildrens(self,population, pairs):
        noParents = pairs * 2
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
        idxArticle = random.randint(0,len(representation) - 1)
        if(self.ByExitence.get() == 1):
            article = self.articles[idxArticle]
            value =  random.randint(0,article.existences)
        else:
            value =  random.randint(0,1)
        representation[idxArticle] = value
        evaluation = self.evaluate(representation)
        if evaluation is None:
            return []
        return [Individual(evaluation,representation)]

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
        #if evaluation is None:
        #    return self.getChildrens(a,b)
        childrens.append(Individual(evaluation, children))

        children = b[0:pivot] + a[pivot:]
        evaluation = self.evaluate(children)
        childrens.append(Individual(evaluation, children))
        #if evaluation is None:
        #    return self.getChildrens(a,b)
        return childrens

    def createFirstGeneration(self, size):
        population = []
        for index  in range(size):
            population.append(self.createRandomIndividual())
        return population

    def createRandomIndividual(self,timeout = 250):
        size = len(self.articles)
        representation = [0] * size
        for index, article  in enumerate(self.articles):
            if(self.ByExitence.get() == 1):
                value =  random.randint(0,article.existences)
            else:
                value =  random.randint(0,1)
            representation[index] = value
        evaluation = self.evaluate(representation)
        if evaluation is None and timeout > 0:
            self.createRandomIndividual(timeout = timeout - 1)
        individual = Individual(evaluation,representation)
        return individual

    def evaluate(self, representation):
        importance = reduce(self.importance,  zip(representation,self.articles), 0)
        weight = reduce(self.weight,  zip(representation,self.articles), 0)
        if weight > self.MAX_WEIGHT:
            return None
        return (importance,weight)

    def weight(self,x,y):
        weight = y[0] * y[1].weight
        return x + weight

    def importance(self,x,y):
        importance = y[0] * y[1].importance
        return x + importance

    def selectFile(self):
        fname = tkFileDialog.askopenfilename()
        if fname:
            self.filename = fname
            self.loadFile()


    def loadFile(self):
        file = open(self.filename,"r")
        rows = file.readlines()
        articles = []
        for row in rows:
            data = row.replace('\n','').split(' ')
            if len(data) == 5:
                articles.append(Article(int(data[0]),int(data[1]),int(data[2]),int(data[3]),data[4]))
        self.articles = articles
        output = '\n'.join(map(repr,articles))
        self.areaData.delete('1.0', END)
        self.areaData.insert(END, output)



    def initialize(self):
        self.pack(fill=BOTH, expand=True)
        self.rowconfigure(8, pad=7)


        exitencesVar = IntVar()
        checkExitences = Checkbutton(self, text="Apply Existences", variable=exitencesVar)
        checkExitences.var = exitencesVar
        checkExitences.grid(sticky=W, row = 1 ,column= 0,columnspan = 2)
        self.ByExitence = exitencesVar



        typeVar = IntVar()
        checkType = Checkbutton(self, text="Apply Type", variable=typeVar)
        checkType.var = typeVar
        checkType.grid(sticky=W, row = 1 ,column= 3,columnspan = 2)
        self.ByType = typeVar



        lblWeight = Label(self, text="Max Weight")
        lblWeight.grid(sticky=W, row= 6 ,column= 0)

        entryWeight = Spinbox(self, from_=17, to=10000)
        entryWeight.grid(sticky=W, row= 6 ,column= 1)


        lblIndividuals = Label(self, text="No. Individuals by Generation")
        lblIndividuals.grid(sticky=W,row= 6 ,column= 3)

        entryIndividuals = Spinbox(self, from_=20, to=10000)
        entryIndividuals.grid(sticky=W,row= 6 ,column= 4)


        lblChromosomes = Label(self, text="Individuals for reproduction")
        lblChromosomes.grid(sticky=W, row= 7 ,column= 0)


        entryReproduction = Spinbox(self, from_=1, to=1000)
        entryReproduction.grid(sticky=W, row= 7 ,column= 1)


        lblGenerations = Label(self, text="Generations")
        lblGenerations.grid(sticky=W,row= 7 ,column= 3)

        entryGenerations = Spinbox(self, from_=10, to=10000)
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
        self.btn = btn

        areaData = Text(self,height=12,width=100)
        areaData.grid(sticky=W,row= 9,column= 0,columnspan=2,rowspan=4,pady=10)

        area = Text(self,height=12,width=100)
        area.grid(sticky=W,row= 9,column= 3,columnspan=3,rowspan=4,pady=10)

        self.areaData = areaData
        self.entryGenerations = entryGenerations
        self.entryReproduction = entryReproduction
        self.entryIndividuals = entryIndividuals
        self.area = area
        self.entryWeight = entryWeight
        self.createMenu()


    def createMenu(self):
        self.menubar = Menu(self)
        filemenu = Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="Open",command=self.selectFile)
        filemenu.add_separator()
        filemenu.add_command(label="Exit",command=self.quit)
        self.menubar.add_cascade(label="File", menu=filemenu)

        try:
            self.master.config(menu = self.menubar)
        except AttributeError:
            self.master.tk.call(master,"config", "-menu",self.menubar)

    def __init__(self, master = None):
        Frame.__init__(self, master)
        Pack.config(self)
        self.master.title("P1")
        self.initialize()
        self.queue = Queue.Queue()


root = Tk()
main = Main(root)
main.mainloop()
