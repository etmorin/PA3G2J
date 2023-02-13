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
    def __init__(self, posX, posY, length, width):
        self.posX = posX
        self.posY = posY
        self.length = length
        self.width = width
        self.body = pymunk.Body()
        self.body.position = (posX, posY)
        self.shape = None

    def get_shape(self):
        return self.shape
    
    def get_body(self):
        return self.body
    
    def get_posX(self):
        return self.posX
    
    def get_posY(self):
        return self.posY
    
    def set_body(self,body):
        self.body = body
    
    

class Bone(BodyPart):
    def __init__(self, posX, posY, length, width):
        super().__init__(  posX, posY, length, width)

        self.shape = pymunk.Poly.create_box(self.body,(length, width))
        self.shape.mass = 10 #TODO:mettre une masse qui est un ratio de la taille
        self.shape.color = (0,0,0,100) #NOIR
        self.shape.elasticity = 0.7
    

class Articulation(BodyPart):
    def __init__(self,  posX, posY, length, width):
        super().__init__(  posX, posY, length, width)

        self.shape = pymunk.Circle(self.body, self.length) #ici length=radius
        self.shape.mass = 10
        self.shape.color = (255,0,0,100)#ROUGE

      
    """class Muscle(BodyPart):
    

    def __init__(self, posX, posY,otherPosX, otherPosY, length, width):
        super().__init__( posX, posY, length, width)
        self.shape = pymunk.Segment(self.body, (posX, posY),(otherPosX,otherPosY), radius = width)
        self.shape.mass = 10
        self.shape.color = (255,105,180,100) #rose profond"""

        
class ArmRight():
    def __init__(self, space, posX, posY, length, width, articulationsize):

        self.bone1 = Bone(posX, posY, length, width)
        self.bone2 = Bone((posX+length+(articulationsize*2)),posY,length,width)
        self.articulation = Articulation(posX+length/2+articulationsize, posY, articulationsize, 0)
        body1 = self.bone1.get_body()
        shape1 = self.bone1.get_shape()
        space.add(body1,shape1)

        body2 = self.bone2.get_body()
        shape2= self.bone2.get_shape()
        space.add(body2,shape2)

        body3= self.articulation.get_body()
        shape3= self.articulation.get_shape()
        space.add(body3,shape3)

        joint1 = pymunk.PivotJoint(body1,body3,(posX+length/2,posY))
        joint2 = pymunk.PivotJoint(body2,body3,(posX+length/2+articulationsize*2,posY))
        space.add(joint1)
        space.add(joint2)
        spring = pymunk.DampedSpring(body1, body2, (0,0), (0,0), 0, 500, 100)
        space.add(spring)
