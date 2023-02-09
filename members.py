import pygame
import pymunk
import pymunk.pygame_util

"""
Pour une créature, il faut trois éléments,
les os, longueurs fixées à la création
les muscles, se tendent et se détendent entre deux os
les articulations, la liaison entre deux os taille fixe.

"""
#classe virtuelle, sert de template aux membres
class BodyPart:
    def __init__(self, startPosX, startPosY, length, width):
        self.startPosX = startPosX
        self.startPosY = startPosY
        self.length = length
        self.width = width
        self.body = pymunk.Body()
        self.body.position = (startPosX, startPosY)
        self.shape = None

    def get_shape(self):
        return self.shape
    
    def get_body(self):
        return self.body
    

class Bone(BodyPart):
    def __init__(self, startPosX, startPosY, length, width):
        super().__init__(  startPosX, startPosY, length, width)

        self.shape = pymunk.Poly.create_box(self.body,(length, width))
        self.shape.mass = 10 #TODO:mettre une masse qui est un ratio de la taille
        self.shape.color = (0,0,0,100) #NOIR

    

class Articulation(BodyPart):
    def __init__(self,  startPosX, startPosY, length, width):
        super().__init__(  startPosX, startPosY, length, width)

        self.shape = pymunk.Circle(self.body, self.length) #ici length=radius
        self.shape.mass = 10
        self.shape.color = (255,0,0,100)#ROUGE

      

class Muscle(BodyPart):
    """
    TODO: Ajouter la méthode de changement de taille du muscle lors
    de la contraction
    """
    def __init__(self, startPosX, startPosY, length, width):
        super().__init__( startPosX, startPosY, length, width)
        self.shape = pymunk.Segment(self.body, (-25,0), (25,0), radius = 5)
        self.shape.mass = 10
        self.shape.color = (255,105,180,100) #rose profond

        

