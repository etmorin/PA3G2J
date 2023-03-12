import pygame
import pymunk
import pymunk.pygame_util
import math


"""
Pour une créature, il faut trois éléments,
les os, longueurs fixées à la création
les muscles, se tendent et se détendent entre deux os
les articulations, la liaison entre deux os taille fixe.

"""
#classe virtuelle, sert de template aux membres
class BodyPart:

    def __init__(self, posX, posY, length, width,category):
        self.posX   = posX
        self.posY   = posY
        self.length = length
        self.width  = width
        self.body   = pymunk.Body()
        self.shape  = None
        self.body.position = (posX, posY)
        self.category = category

       
    def get_shape(self):
        return self.shape
    
    def get_body(self):
        return self.body
    
    def get_posX(self):
        return self.posX
    
    def get_posY(self):
        return self.posY
    


 
class Bone(BodyPart):

    def __init__(self, posX, posY, length, width, category):
        super().__init__(  posX, posY, length, width,category)
        self.shape       = pymunk.Poly.create_box(self.body,(length, width))
        self.shape.mass  = length*width/100 
        self.shape.color = (0,0,0,100) #NOIR
        self.shape.elasticity = 0.7
        self.shape.friction   = 1 #pour ne pas glisser sur le sol
        self.shape.filter = pymunk.ShapeFilter(categories=category,mask=category)
    
    def get_length(self):
        return self.length
    
    def get_width(self):
        return self.width


    

class Articulation(BodyPart):

    def __init__(self,  posX, posY, length, width, category):
        super().__init__(  posX, posY, length, width, category)
        self.shape       = pymunk.Circle(self.body, self.length) #ici length=radius
        self.shape.mass  = length*2
        self.shape.color = (255,0,0,100)#ROUGE
        self.shape.elasticity = 0.7
        self.shape.friction   = 1 #pour ne pas glisser sur le sol
        self.shape.filter = pymunk.ShapeFilter(categories=category,mask=category)
        self.radius = length

    def get_radius(self):
        return self.radius

class Torso(BodyPart):

    def __init__(self, posX, posY, length, width, category):
        super().__init__(posX, posY, length, width,category)
        self.category = category


    def round(self):
        self.shape = pymunk.Circle(self.body,self.length)
        self.shape.mass = self.length*2
        self.shape.color = (0,255,0,100) #Vert
        self.shape.filter = pymunk.ShapeFilter(categories=self.category,mask=self.category)


class Arm(BodyPart):

    def __init__(self,space, posX, posY, length, width, articulationSize, numberOfArticulations, muscleStrength,category,factor):
        super().__init__(posX, posY, length, width,category)
        self.space = space
        self.muscleStrength = muscleStrength
        self.bone1 = Bone(posX, posY, length, width, category)
        space.add(self.bone1.get_body(),self.bone1.get_shape())
        self.previousBone = self.bone1
        self.previousboneBody = self.previousBone.get_body()
        self.previousArticulationSize = articulationSize
        

    def sizeRefactoring(self,length,width,articulationSize,factor):

        temp1 = factor*length
        temp2 = factor*width
        temp3 = factor*articulationSize
        if temp1 > 30  and temp2 > 10 and temp3 > 5:
            length,width,articulationSize = int(temp1), int(temp2), int(temp3)

        return length, width, articulationSize
    


class ArmRight(Arm):

    def __init__(self,space, posX, posY, length, width, articulationSize, numberOfArticulations, muscleStrength,category,factor):
        super().__init__(space, posX, posY, length, width, articulationSize, numberOfArticulations, muscleStrength,category,factor)
        for i in range(1,numberOfArticulations+1):
            self.add_articulation(i, posX, posY, length, width, articulationSize, category)
            length,width,articulationSize = self.sizeRefactoring(length,width,articulationSize,factor)

    def add_articulation(self,i,posX, posY, length, width, articulationSize, category):

        bone = Bone(self.previousBone.get_posX()+ self.previousBone.get_length()+2*self.previousArticulationSize,posY,length,width, category)
        articulation = Articulation(self.previousBone.get_posX()+self.previousBone.get_length()/2+articulationSize, posY, articulationSize, 0, category)
        self.previousArticulationSize = articulation.get_radius()
        self.space.add(bone.get_body(),bone.get_shape())
        self.space.add(articulation.get_body(),articulation.get_shape())
        joint1 =  pymunk.PivotJoint(self.previousboneBody,articulation.get_body(),(self.previousBone.get_posX()+self.previousBone.get_length()/2,posY))
        joint2 =  pymunk.PivotJoint(bone.get_body(),articulation.get_body(),(bone.get_posX()-length/2,posY))
        spring = pymunk.DampedSpring(bone.get_body(), self.previousboneBody, (0,0), (0,0), 0, self.muscleStrength, 100)
        self.space.add(joint1,joint2,spring)
        self.previousBone = bone
        self.previousboneBody = bone.get_body()
 

    
class ArmLeft(Arm):

    def __init__(self,space, posX, posY, length, width, articulationSize, numberOfArticulations, muscleStrength,category,factor):
        super().__init__(space, posX, posY, length, width, articulationSize, numberOfArticulations, muscleStrength,category,factor)
        for i in range(1,numberOfArticulations+1):
            self.add_articulation(i, posX, posY, length, width, articulationSize, category)
            length,width,articulationSize = self.sizeRefactoring(length,width,articulationSize,factor)

    def add_articulation(self,i,posX, posY, length, width, articulationSize, category):
        bone = Bone(self.previousBone.get_posX() - self.previousBone.get_length()-2*self.previousArticulationSize,posY,length,width, category)
        articulation = Articulation(self.previousBone.get_posX()-self.previousBone.get_length()/2-articulationSize, posY, articulationSize, 0, category)
        self.previousArticulationSize = articulation.get_radius()
        self.space.add(bone.get_body(),bone.get_shape())
        self.space.add(articulation.get_body(),articulation.get_shape())
        joint1 =  pymunk.PivotJoint(self.previousboneBody,articulation.get_body(),(self.previousBone.get_posX()-self.previousBone.get_length()/2,posY))
        joint2 =  pymunk.PivotJoint(bone.get_body(),articulation.get_body(),(bone.get_posX()+length/2,posY))
        spring = pymunk.DampedSpring(bone.get_body(), self.previousboneBody, (0,0), (0,0), 0, self.muscleStrength, 100)
        self.space.add(joint1,joint2,spring)
        self.previousboneBody = bone.get_body()
        self.previousBone = bone


class Creature():

    def __init__(self, space, posX, posY, bodySize, nbrOfArms, lengthBones, widthBones, radiusArticulations,numberOfArticulations, muscleStrength,category,asymetry):
        

        self.parameters = [bodySize,nbrOfArms,lengthBones,widthBones,radiusArticulations,numberOfArticulations,muscleStrength,asymetry]
        self.torso = Torso(posX,posY,bodySize,width=0,category=category)
        self.torso.round()
        body  = self.torso.get_body()
        shape = self.torso.get_shape()
        factorBones, factorArms = self.asymetryFactory(asymetry)
        
        sizesList =[]


        for i in range(nbrOfArms):

            cercleX = posX + bodySize*math.cos(i*2*math.pi/(nbrOfArms))
            cercleY = posY + bodySize*math.sin(i*2*math.pi/(nbrOfArms))

            if cercleX<posX:   #bras gauche
                arm = ArmLeft(space, cercleX-(lengthBones/2), cercleY, lengthBones, widthBones, radiusArticulations,numberOfArticulations, muscleStrength,category,factorBones)
            else:              #bras droit
                arm = ArmRight(space, cercleX+(lengthBones/2), cercleY, lengthBones, widthBones, radiusArticulations,numberOfArticulations, muscleStrength,category,factorBones)

            joint = pymunk.PivotJoint(arm.bone1.get_body(),body,(cercleX,cercleY))
            spring = pymunk.DampedSpring(arm.bone1.get_body(), body, (0,0), (0,0), 0, muscleStrength, 100)
            space.add(joint,spring)

            if i < (nbrOfArms/2):
                sizesList.insert(0,(lengthBones,widthBones,radiusArticulations))
                if i != 0:
                    temp1 = factorArms*lengthBones
                    temp2 = factorArms*widthBones
                    temp3 = factorArms*widthBones
                    if temp1 > 30  and temp2 > 10 and temp3 > 5:
                        lengthBones,widthBones,radiusArticulations = int(temp1), int(temp2), int(temp3)
            else:
                lengthBones,widthBones,radiusArticulations = sizesList.pop()
            
        space.add(body,shape)


        


    def asymetryFactory(self, asymetryFactor):
        if asymetryFactor < 8  and asymetryFactor%2 == 0:
            factorbones =  1
            factorarms = 1
        elif asymetryFactor < 8 and asymetryFactor%2 != 0 :
            factorbones =1 
            factorarms = 0.95
        elif asymetryFactor >= 8 and asymetryFactor%2 ==0:
            factorbones = 0.95
            factorarms = 1
        elif asymetryFactor >= 8 and asymetryFactor%2 != 0:
            factorbones = 0.95
            factorarms = 0.75
        return factorbones, factorarms



    def getCenterShape(self):
        return self.torso.get_shape()






