import pygame
import pymunk
import pymunk.pygame_util
import math
from genetique import *

"""
Pour une créature, il faut trois éléments,
les os, longueurs fixées à la création
les muscles, se tendent et se détendent entre deux os
les articulations, la liaison entre deux os taille fixe.

"""
#classe virtuelle, sert de template aux membres
class BodyPart:

    def __init__(self, posX, posY, length, width):
        self.posX   = posX
        self.posY   = posY
        self.length = length
        self.width  = width
        self.body   = pymunk.Body()
        self.shape  = None
        self.body.position = (posX, posY)

       
    def get_shape(self):
        return self.shape
    
    def get_body(self):
        return self.body
    
    def get_posX(self):
        return self.posX
    
    def get_posY(self):
        return self.posY

 
class Bone(BodyPart):

    def __init__(self, posX, posY, length, width):
        super().__init__(  posX, posY, length, width)
        self.shape       = pymunk.Poly.create_box(self.body,(length, width))
        self.shape.mass  = length*width/100 
        self.shape.color = (0,0,0,100) #NOIR
        self.shape.elasticity = 0.7
        self.shape.friction   = 1 #pour ne pas glisser sur le sol

    

class Articulation(BodyPart):

    def __init__(self,  posX, posY, length, width):
        super().__init__(  posX, posY, length, width)
        self.shape       = pymunk.Circle(self.body, self.length) #ici length=radius
        self.shape.mass  = length*2
        self.shape.color = (255,0,0,100)#ROUGE
        self.shape.elasticity = 0.7
        self.shape.friction   = 1 #pour ne pas glisser sur le sol

class Torso(BodyPart):

    def __init__(self, posX, posY, length, width):
        super().__init__(posX, posY, length, width)


    def round(self):
        self.shape = pymunk.Circle(self.body,self.length)
        self.shape.mass = self.length*2
        self.shape.color = (0,255,0,100) #Vert

class Arm(BodyPart):

    def __init__(self,space, posX, posY, length, width, articulationSize, numberOfArticulations, muscleStrength):
        super().__init__(posX, posY, length, width)
        self.space = space
        self.muscleStrength = muscleStrength
        self.bone1 = Bone(posX, posY, length, width)
        self.bone1.get_shape().filter = pymunk.ShapeFilter(group=1)
        space.add(self.bone1.get_body(),self.bone1.get_shape())
        self.previousbone = self.bone1.get_body()
        

        for i in range(1,numberOfArticulations+1):
            self.add_articulation(i, posX, posY, length, width, articulationSize)


    def add_articulation(self,i,posX, posY, length, width, articulationSize):

        bone = Bone((posX+(length+(articulationSize*2))*i),posY,length,width)
        articulation = Articulation(posX+(length + 2*articulationSize)*(i-1) +length/2+articulationSize, posY, articulationSize, 0)
        bone.get_shape().filter = pymunk.ShapeFilter(group=1)
        articulation.get_shape().filter = pymunk.ShapeFilter(group=1)
        self.space.add(bone.get_body(),bone.get_shape())
        self.space.add(articulation.get_body(),articulation.get_shape())
        joint1 =  pymunk.PivotJoint(self.previousbone,articulation.get_body(),(posX + (i-1)*(length+2*articulationSize)+length/2,posY))
        joint2 =  pymunk.PivotJoint(bone.get_body(),articulation.get_body(),(posX+(i-1)*(length+2*articulationSize)+ length/2+articulationSize*2,posY))
        spring = pymunk.DampedSpring(bone.get_body(), self.previousbone, (0,0), (0,0), 0, self.muscleStrength, 100)
        self.space.add(joint1,joint2,spring)
        self.previousbone = bone.get_body()
 


class Creature():

    def __init__(self, space, posX, posY, bodySize, nbrOfArms, lengthBones, widthBones, radiusArticulations,numberOfArticulations, muscleStrength, collisionLayer = 1):
        

        self.parameters = [bodySize,nbrOfArms,lengthBones,widthBones,radiusArticulations,numberOfArticulations,muscleStrength]
        self.torso = Torso(posX,posY,bodySize,width=0)
        self.torso.round()
        body  = self.torso.get_body()
        shape = self.torso.get_shape()
        shape.filter = pymunk.ShapeFilter(group=1)

        for i in range(nbrOfArms):

            cercleX = posX + bodySize*math.cos(i*2*math.pi/(nbrOfArms))
            cercleY = posY + bodySize*math.sin(i*2*math.pi/(nbrOfArms))
            
            
            if cercleX<posX:   #bras gauche
                arm = Arm(space, cercleX-((lengthBones+2*radiusArticulations)*(numberOfArticulations))-0.5*lengthBones, cercleY, lengthBones, widthBones, radiusArticulations,numberOfArticulations, muscleStrength)
                joint = pymunk.PivotJoint(arm.previousbone,body,(cercleX,cercleY))
                spring = pymunk.DampedSpring(arm.previousbone, body, (0,0), (0,0), 0, muscleStrength, 100)

            else:              #bras droit
                arm = Arm(space, cercleX+(lengthBones/2), cercleY, lengthBones, widthBones, radiusArticulations,numberOfArticulations, muscleStrength)
                joint = pymunk.PivotJoint(arm.bone1.get_body(),body,(cercleX,cercleY))
                spring = pymunk.DampedSpring(arm.bone1.get_body(), body, (0,0), (0,0), 0, muscleStrength, 100)

            space.add(joint,spring)
        space.add(body,shape)

    def getCenterShape(self):
        return self.torso.get_shape()
        #TODO: ajouter nom creature, ajouter la puissance des muscles (varier via armright)






