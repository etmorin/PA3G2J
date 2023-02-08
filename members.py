import pygame
import pymunk

"""
Pour une créature, il faut trois éléments,
les os, longueurs fixées à la création
les muscles, se tendent et se détendent entre deux os
les articulations, la liaison entre deux os taille fixe.

"""

class BodyPart:
    def __init__(self, startPosX, startPosY,length, width):
        self.startPosX = startPosX
        self.startPosY = startPosY
        self.length = length
        self.width = width

class Bone(BodyPart):
    def __init__(self, startPosX, startPosY,length, width):
        super().__init__(self, startPosX, startPosY,length, width)
        self.color = pygame.Color(255,255,255,0)
        self.form = "rectangle"

class Articulation(BodyPart):
    def __init__(self, startPosX, startPosY,length, width):
        super().__init__(self, startPosX, startPosY,length, width)
        self.color = pygame.Color(255,0,0,0)
        self.form = "round"

class Muscle(BodyPart):
    """
    TODO: Ajouter la fonction de changement de taille du muscle lors
    de la contraction
    """
    def __init__(self, startPosX, startPosY,length, width):
        super().__init__(self, startPosX, startPosY,length, width)
        self.color = pygame.Color(240,0,0,100)
        self.form= "oval"

