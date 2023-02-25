import random
from members import *

PARAMETERS = ["bodySize", "nbrOfArms", "lengthBones",
                       "widthBones", "radiusArticulations",
                       "numberOfArticulations", "muscleStrength"]

"""
    /!\ : TEMPORAIRE :  /!\ 

    père = [1101,1100,1000,...]
    mère = [0001,1101,1001,...]
    
    fils = [1001,1101,1001,...]

    [1111] = un allele

    Nos alleles:

    longueur os : 1 -> 750 , par pas de 50
    largeurs os : 1 -> 60 , par pas de 4
    nombre bras : 1 -> 16 , par pas de 1
    nombre articulations: 1 -> 7 , par pas de 0,5, arrondis à l'inférieur
    taille du corps: 16 -> 242 , par pas de 16
    taille articulation: 1 -> 32 , par pas de 2
    puissance muscle: 200 -> 3200 , par pas de 200
    vecteur changement taille des membres: 1 -> 16 , par pas de 1

"""


class Individual():

    def __init__(self, dna, bodyInSpace=None, father=None, mother=None) :
        self.father = father
        self.mother = mother
        self.dna = dna
        self.bodyInSpace = bodyInSpace
        self.mutationRiskPerThousand = 10
        self.bestScore = 0

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
    
    def set_mutationRisk(self, newMutationRisk):
        self.mutationRiskPerThousand = newMutationRisk

    def reproduce(self,mate):
        """
        methode de reproduction de l'individu, appelle également la fonction de mutation

        args: 
            mate: un objet de type individu avec lequel notre objet va se reproduire
        
        returns:
            child: un objet de type individu qui est l'enfant des deux autres individus.
    
        """

        otherDna = mate.get_dna()
        newDnaString = self.mixingDna(self.dna,otherDna) 
        newDnaString = self.mutationCenter(newDnaString)
        newDna = Dna(newDnaString)
        child = Individual(newDna,father = self,mother = mate)
        return child
    
    def mixingDna(self, mydna, matedna):
        """
        Mélange deux objets de type ADN
        Args:
            mydna, matedna: objets de type ADN
        
        returns:
            string utilisable par objet adn
        
        """

        dna1 = mydna.get_geneString()
        dna2 = matedna.get_geneString()
        newDnaString =""

        for i in range(len(dna1)):
            if dna1[i] != dna2[i]:
                chance = random.randint(0,1)

                if chance == 0:
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
    
    def draw(self, space, posX, posY, maskCategory):
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
        bodySize,nbrOfArm,lengthBones,widthBones,radiusArticulations,numberOfArticulations,muscleStrength = paramValues
        creature = Creature(space, posX, posY,
                            bodySize,nbrOfArm,lengthBones,widthBones,
                            radiusArticulations,numberOfArticulations,
                            muscleStrength,maskCategory )
        self.bodyInSpace = creature
        return self.bodyInSpace


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

        divisionFactor={"bodySize": 15, "nbrOfArms": 1, "lengthBones": 50,
                         "widthBones": 4 , "radiusArticulations": 2,
                         "numberOfArticulations": 0.5, "muscleStrength": 200}
        self.geneString=""

        for parameter in parameters:
            temp = parameters[parameter]/divisionFactor[parameter]
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

        multiplicationFactor= [ 15,  1,  50, 4 ,  2, 0.5, 200, 1]

        self.geneList = self.geneSeparation()

        tempList = []
        for i in range (len(self.geneList)):
            temp = int(self.geneList[i],2)

            tempList.append(temp*multiplicationFactor[i])

        dictionnary = dict(zip(parameters,tempList))
        return dictionnary



    def control(self,temp):

        if temp >= self.dataGene:
            temp = self.dataGene-1
        return temp
    
    def listToDictionnary(self,list):

        
        dico = dict(zip(list,PARAMETERS))
        return dico
    




class Generation():

    def __init__(self, depth) :
        self.individualsList = []
        self.individualTrackersList = []
        self.generationDepth =  depth

    def add_individual(self, individual):
        self.individualsList.append(individual)

    def add_individualTracker(self, individualTracker):
        self.individualTrackersList.append(individualTracker)

    def get_individualList(self):
        return self.individualsList
    
    def get_individualTrackerList(self):
        return self.individualTrackersList
    
    def get_generationDepth(self):
        return self.generationDepth
    
    def updateTrackers(self):
        for tracker in self.individualTrackersList:
            tracker.update()
    
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
            for individual in self.individualsList :
                if individual.bestScore > maxscore :
                    maxscore = individual.bestScore
                    best = individual
            bestIndividuals.append(best)
        
        return bestIndividuals
    








"""                                                                            
                        *****                  TESTING                     *****
"""                                                                             
    
"""stringMale   = "00000000000000000000000000000000"

stringFemale = "11111111111111111111111111111111"


adnMale = Dna(stringMale)
adnFemale = Dna(stringFemale)

male = Individual(adnMale,None,None)
female = Individual(adnFemale,None,None)

for i in range(100):
    guy = male.reproduce(male)
    print(guy)

creatureParameters = {"bodySize" : 30 , "nbrOfArms": 1, "lengthBones": 100,
                       "widthBones" : 10, "radiusArticulations":5,
                       "numberOfArticulations": 2, "muscleStrength": 1500}

param = list(creatureParameters.values())"""

