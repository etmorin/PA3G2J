import random
import numpy as np
from members import *
from positionTracker import *

PARAMETERS = ["bodySize", "nbrOfArms", "lengthBones",
                       "widthBones", "radiusArticulations",
                       "numberOfArticulations", "muscleStrength","asymetry"]

PARAM_MIN_MAX = [[10,121], [1,8],[10,100], [5,60],[2,32],[1,7],[1000,5000],[1,15]]

ADN_LENGTH = 32

"""
    /!\ : TEMPORAIRE :  /!\ 

    père = [1101,1100,1000,...]
    mère = [0001,1101,1001,...]
    
    fils = [1001,1101,1001,...]

    [1111] = un allele

    Nos alleles:

    longueur os : 1 -> 325 , par pas de 25
    largeurs os : 1 -> 60 , par pas de 4
    nombre bras : 1 -> 16 , par pas de 1
    nombre articulations: 1 -> 7 , par pas de 0,5, arrondis à l'inférieur
    taille du corps: 16 -> 121 , par pas de 8
    taille articulation: 1 -> 32 , par pas de 2
    puissance muscle: 200 -> 3200 , par pas de 200
    vecteur changement taille des membres: 1 -> 16 , par pas de 1
    asymetry: 0,1 : taille des os égales au sein du meme bras /
      2,3 : taille des membres égales


"""


class Individual():

    def __init__(self, dna, bodyInSpace=None, father=None, mother=None) :
        self.father = father
        self.mother = mother
        self.dna = dna
        self.bodyInSpace = bodyInSpace
        self.positionTracker = PositionTracker()
        self.mutationRiskPerThousand = 10
        self.bestScore = 0
        self.creature = None

        if type(dna) == str :
            self.dna = Dna(dna)

    def __str__(self) :
        return(self.dna.get_geneString())

    def get_father(self):
        return self.father
    
    def get_mother(self):
        return self.mother
    
    def get_dna(self):
        return self.dna
    
    def get_bodyInSpace(self):
        return self.bodyInSpace
    
    def set_bodyInSpace(self, bodyInSpace):
        self.bodyInSpace = bodyInSpace
        
    def get_currentScore(self):
        self.updateTracker()
        return self.positionTracker.getRanDistance()
    
    def get_bestScore(self):
        self.updateTracker()
        self.bestScore = self.positionTracker.getMaxRanDistance()
        return self.positionTracker.getMaxRanDistance()
    
    def set_mutationRisk(self, newMutationRisk):
        self.mutationRiskPerThousand = newMutationRisk
        
    def updateTracker(self):
        self.positionTracker.update()

    def reproduce(self,mate):
        """
        methode de reproduction de l'individu, appelle également la fonction de mutation

        args: 
            mate: un objet de type individu avec lequel notre objet va se reproduire
        
        returns:
            child: un objet de type individu qui est l'enfant des deux autres individus.
    
        """

        otherDna = mate.get_dna()

        reproductionMode = random.randint(0,2)

        newDnaString = self.mixingDna(self.dna,otherDna, reproductionMode) 
        newDnaString = self.mutationCenter(newDnaString)
        newDna = Dna(newDnaString)
        child = Individual(newDna,father = self,mother = mate)
        return child
    
    def mixingDna(self, mydna, matedna, mode):
        """
        Mélange deux objets de type ADN
        Args:
            mydna, matedna: objets de type ADN
            mode , un int entre 0 et 2 qui décide quel parent aura une part prioritaire sur l'adn de l'enfant
        
        returns:
            string utilisable par objet adn
        
        """
        reproductionFactor = [10, 15, 5]
        myFactor = reproductionFactor[mode]

        dna1 = mydna.get_geneString()
        dna2 = matedna.get_geneString()
        newDnaString =""

        for i in range(len(dna1)):
            if dna1[i] != dna2[i]:
                chance = random.randint(1,20)

                if chance >= myFactor:
                    newDnaString += dna2[i]
                else:
                    newDnaString += dna1[i]
                    
            else:
                newDnaString += dna1[i]
        return newDnaString
    
    
    def mutationCenter(self,dnaString):

        for letter in dnaString:
            chance = random.randint(0,999)

            if (chance <= self.mutationRiskPerThousand):
                choice = random.randint(0,len(dnaString)-1)
                listedString = list(dnaString)

                if listedString[choice] == "1":
                    listedString[choice] = "0"

                else:
                    listedString[choice] = "1"
                dnaString = "".join(listedString)

        return dnaString
    
    def createBody(self, space, posX, posY, maskCategory):
        """
        dessine une créature dans l'espace.
        Args:
            space: l'espace pymunk
            posX,posY : deux int pour la position
            maskCategory: un bin indiquant la catégorie et le masque de collision
                        il faut que chaque category soit une puissance de 2 allant jusqu'à 32bit
                        donc 1,2,4,8,16,32,64,....
        Returns:
            un objet de type créature
        """

        dictionnary = self.dna.dnaToParam(PARAMETERS)
        paramValues = list(dictionnary.values())
        paramValues = map(int,paramValues)
        
        bodySize,nbrOfArm,lengthBones,widthBones,radiusArticulations,numberOfArticulations,muscleStrength,asymetry = paramValues
        self.creature = Creature(space, posX, posY,
                            bodySize,nbrOfArm,lengthBones,widthBones,
                            radiusArticulations,numberOfArticulations,
                            muscleStrength,maskCategory ,asymetry)
        self.bodyInSpace = self.creature
        self.positionTracker.setObjectToFollow(self.bodyInSpace.getCenterShape())
        return self.bodyInSpace
    
    def switchTransparancy(self):
        if self.creature:
            self.creature.switch_transparancy()


class Dna():

    def __init__(self,string) :
        self.geneString = string
        self.geneList = []
        self.dataGene = 16

    def __str__(self) :
        return self.geneString


    def geneSeparation(self):
        """
        sépare les éléments du string adn en une liste d'éléments de longueur 4
        
        """

        i = 0
        temp = ""
        for element in self.geneString:
            i += 1
            temp += element

            if i==4:
                self.geneList.append(temp)
                temp = ""
                i = 0
        return self.geneList


    def get_geneList(self):
        return self.geneList
    
    
    def get_geneString(self):
        return self.geneString
    

    def paramToDna(self,parameters):
        """
        Args:
            parameters: a dictionnary countaining the parameters as 
            keys and int as values

        Returns:
            Dna string
        """

        divisionFactor={"bodySize": 4, "nbrOfArms": 0.5, "lengthBones": 7,
                         "widthBones": 2 , "radiusArticulations": 1.5,
                         "numberOfArticulations": 0.5, "muscleStrength": 350, 
                         "asymetry": 1}
        self.geneString=""
        i=0

        for parameter in parameters:
    
            temp = parameters[parameter]/divisionFactor[parameter]
            temp = self.paramSizeControl(temp,i)
            i+=1
            temp = self.control(temp)
            temp = str(bin(int(temp)))
            temp= temp[2:]      #on retire le 0b de la notation binaire
            bitString= bin(self.dataGene)
            bitString= bitString[3:] #on retire le ob ET le 1 de la notation binaire
            list1 = list(bitString)[::-1]
            list2 = list(temp)[::-1]# on renverse les deux nombres binaires pour itérer depuis la fin
            for i in range(len(list2)):
                list1[i] = list2[i]
            list1 = list1[::-1]# on remet à l'endroit et on sauvegarde
            string = "".join(list1)
            self.geneString += string
        

        return self.geneString
    
    def dnaToParam(self,parameters):
        """
        Args:
            a list of strings of the parameters names

        Returns:
            a dictionnary countaining the parameters names as keys 
            and their values as ints
        
        """

        multiplicationFactor= [ 4,  0.5,  7, 2 ,  1.5, 0.5, 350, 1]

        self.geneList = self.geneSeparation()
  

        tempList = []
        for i in range (len(self.geneList)): 

            temp = int(self.geneList[i],2)
            temp = temp*multiplicationFactor[i]
            temp = self.paramSizeControl(temp,i)

            tempList.append(temp)

        dictionnary = dict(zip(parameters,tempList))
        return dictionnary

    def paramSizeControl(self,temp,i):

        if temp < PARAM_MIN_MAX[i][0]:
            temp = PARAM_MIN_MAX[i][0]

        elif temp > PARAM_MIN_MAX[i][1]:
            temp = PARAM_MIN_MAX[i][1]
        
        return temp


    def control(self,temp):

        if temp >= self.dataGene:
            temp = self.dataGene-1
        return temp
    
    def listToDictionnary(self,list):

        
        dico = dict(zip(list,PARAMETERS))
        return dico
    




class Generation():

    def __init__(self, depth, size, space) :
        self.individualsList = []
        self.generationDepth =  depth
        self.size = size
        self.space = space
        if depth == 0:
            self.createFirstGen(size)

    def __str__(self):
        string = "Generation of  depth : "
        string += str(self.generationDepth)
        string +="\n"
        for individual in self.individualsList:
            string+=individual.dna.get_geneString()
            string += "\n"
        return string

    def add_individual(self, individual):
        self.individualsList.append(individual)
        

    def get_individualList(self):
        return self.individualsList
    
    
    def get_generationDepth(self):
        return self.generationDepth
    
    def updateTrackers(self):
        for individual in self.individualsList:
            individual.updateTracker()

    def get_generationSize(self):
        return self.size
    
    def findBestIndividual(self,n):
        """
        Parcours la liste des individus et prend les n plus efficaces
            Args:
                n , le nombre d'individus recherchés
            Return:
                liste des n meilleurs individus
        """
        

        bestIndividuals=[]

        for i in range(n):
            maxscore = 0
            best = None
            for individual in self.individualsList:
                score = individual.get_bestScore()
                if score >= maxscore and individual not in bestIndividuals :
                    maxscore = score
                    best = individual
            bestIndividuals.append(best)
        
        return bestIndividuals
    
    def createNextGeneration(self, sizeOfGeneration, parents):
        """
        Créé une génération de taille n = int en prenant comme parent les deux individus les plus forts de cette génération.
            Args:
                sizeOfGeneration: un int la taille voulue de la nouvelle gen
            returns:
                newGen : un objet de type génération contenant sizeOfGeneration individus
        
        """
        if len(parents) == sizeOfGeneration:
            return self.createNextGenerationWeighted(parents)

        bestIndividuals = parents
        newGen  = Generation(self.generationDepth+1,sizeOfGeneration, self.space)
        
        for i in range (sizeOfGeneration):
            newIndividual = bestIndividuals[0].reproduce(bestIndividuals[1])
            newGen.add_individual(newIndividual)

        return newGen
    
    def createNextGenerationWeighted(self, parents):
        weights = [(individual.get_bestScore()+100)*100 for individual in parents]
        probs = []
        for weight in weights:
            probs.append(weight/sum(weights))
        newGen  = Generation(self.generationDepth+1, len(parents), self.space)
        for i in range(len(parents)):
            parent1, parent2 = np.random.choice(parents,size=2,replace=False,p=probs)
            child = parent1.reproduce(parent2)
            newGen.add_individual(child)
        return newGen
    
    def createFirstGen(self, sizeOfGeneration):
        """
        Crée la premiere génération totalement aléatoirement
            Args:
                sizeOfGeneration: un int la taille voulue de la nouvelle gen
            returns:
                None (transforme cet objet génération)
        """


        for i in range(sizeOfGeneration):

            adnString = ""

            for j in range(ADN_LENGTH):

                oneOrZero = random.randint(0,1)
                adnString += str(oneOrZero)
            
            newIndividual = Individual(adnString)
            newIndividual.createBody(self.space, 0, 350, 2**i)
            self.individualsList.append(newIndividual)



            



"""                                                                            
                        *****                  TESTING                     *****
"""                                                                             
    
"""stringMale   = "00000000000000000000000000000000"

stringFemale = "11111111111111111111111111111111"



male = Individual(stringMale)
female = Individual(stringFemale)

for i in range(100):
    guy = male.reproduce(female)
    print(guy)

creatureParameters = {"bodySize" : 30 , "nbrOfArms": 1, "lengthBones": 100,
                       "widthBones" : 10, "radiusArticulations":5,
                       "numberOfArticulations": 2, "muscleStrength": 1500, "asymetry" : 6}
"""

"""
        Ici exemple fonctionnement génération
"""

"""firstGen = Generation(0,5)
print(firstGen)

previousGen = firstGen

for i in range(100):
    currentGen = previousGen.createNextGeneration(5)
    print(currentGen)
    previousGen = currentGen"""

"""firstGen = Generation(0,5)
run = Handler(firstGen, 100, 5)
run.start()"""
