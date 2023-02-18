import random



"""
    
    père = [1101,1100,1000,...]
    mère = [0001,1101,1001,...]
    
    fils = [1001,1101,1001,...]

    [1111] = un allele

    Nos alleles:

    longueur os
    largeurs os
    nombre bras
    nombre articulations
    taille du corps
    taille articulation
    puissance muscle
    vecteur changement taille des membres

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


    def gene_separation(self):
        i = 0
        temp=""
        for element in self.string:
            i+=1
            temp += element
            if i==4:
                self.geneList.append(temp)
                temp =""
                i = 0


    def get_geneList(self):
        return self.geneList
    
    
    def get_geneString(self):
        return self.geneString
    

"""                                                                            
                        *****                  TESTING                     *****
"""                                                                             
    
stringMale   = "00000000000000000000000000000000"
stringFemale = "11111111111111111111111111111111"

adnMale = Dna(stringMale)
adnFemale = Dna(stringFemale)

male = Individual(adnMale,None,None)
female = Individual(adnFemale,None,None)

for i in range(100):
    guy = male.reproduce(male)
    print(guy)