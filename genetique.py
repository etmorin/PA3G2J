class Individu():
    def __init__(self, dna, father, mother) :
        self.father = father
        self.mother = mother
        self.dna = dna

    def get_father(self):
        return self.father
    
    def get_mother(self):
        return self.mother
    
    def get_dna(self):
        return self.dna

    def reproduce(self,mate):

        otherDna = mate.dna
        newDna = "calcul nouvel adn"   #TODO
        child = Individu(newDna,self,mate)
        return child
    


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