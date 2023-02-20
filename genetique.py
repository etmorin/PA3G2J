import random

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

    def __init__(self, dna, father, mother) :
        self.father = father
        self.mother = mother
        self.dna = dna
        self.mutationRiskPerThousand = 10

    def __str__(self) :
        return(self.dna.get_geneString())

    def get_father(self):
        return self.father
    
    def get_mother(self):
        return self.mother
    
    def get_dna(self):
        return self.dna
    
    def set_mutationRisk(self, newMutationRisk):
        self.mutationRiskPerThousand = newMutationRisk

    def reproduce(self,mate):

        otherDna = mate.get_dna()
        newDnaString = self.mixing_dna(self.dna,otherDna) 
        newDnaString = self.mutation_center(newDnaString)
        newDna = Dna(newDnaString)
        child = Individual(newDna,self,mate)
        return child
    
    def mixing_dna(self, mydna, matedna):

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
    
    
    def mutation_center(self,dnaString):

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
            


class Dna():

    def __init__(self,string) :
        self.geneString = string
        self.geneList = []
        self.dataGene = 16

    def __str__(self) :
        return self.geneString


    def gene_separation(self):

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

        multiplicationFactor= [ 15,  1,  50, 4 ,  2, 0.5, 200, 1]

        self.geneList = self.gene_separation()
        print(self.geneList)
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

    

"""                                                                            
                        *****                  TESTING                     *****
"""                                                                             
    
stringMale   = "00000000000000000000000000000000"

stringFemale = "11111111111111111111111111111111"


adnMale = Dna(stringMale)
adnFemale = Dna(stringFemale)

male = Individual(adnMale,None,None)
female = Individual(adnFemale,None,None)

"""for i in range(100):
    guy = male.reproduce(male)
    print(guy)"""

creatureParameters = {"bodySize" : 30 , "nbrOfArms": 1, "lengthBones": 100,
                       "widthBones" : 10, "radiusArticulations":5,
                       "numberOfArticulations": 2, "muscleStrength": 1500}

colinadn= male.reproduce(female)
colin = colinadn.get_dna()
dico = colin.dnaToParam(PARAMETERS)
print(dico)