import pymunk
import pygame
import pymunk.pygame_util
from genetique import *
import time
import ui


# Initialize Pygame and PyMunk
pygame.init()
space = pymunk.Space()

WIDTH, HEIGHT = 1000, 800
window = pygame.display.set_mode((WIDTH, HEIGHT))

def draw(space, window,draw_options):
    window.fill("white")
    space.debug_draw(draw_options)
    pygame.display.update()

def create_boundaries(space, width, height):
    
    pos, size= (width/2, height - 10), (width,20)
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = pos
    shape = pymunk.Poly.create_box(body,size)
    shape.elasticity = 0.4
    shape.friction = 0.5
    space.add(body,shape)

def start(space):
    creatureParameters = {"bodySize" : 30 , "nbrOfArms": 1, "lengthBones": 100,
                       "widthBones" : 10, "radiusArticulations":5,
                       "numberOfArticulations": 2, "muscleStrength": 1000}
    frankensteinDna = Dna(None)
    frankensteinDna.paramToDna(creatureParameters)
    frankenstein = Individual(frankensteinDna)
    frankenstein.createBody(space, 300,300,1)

    #autres gen:
   
    frankensteinJunior = Individual("0100001001000010001000100010")
    frankensteinJunior.createBody(space, 300,300,2)

    franken2 = Dna(string="0100001001000010001000100010")
    franken2body = Individual(franken2)
    franken2body.createBody(space,400,400,4)

def verifyStringDna(stringDna):

    if len(stringDna) != 32 : #ici on pourra lier avec genetique.LengthDNA
        print("String ADN de taille invalide")
        raise ValueError

    elif not all(letter in "01" for letter in stringDna):
        print("L'ADN de notre créature n'accepte que des 0 et des 1")
        raise IndexError
    

def insertCreature(stringDna, currentGen):

    verifyStringDna(stringDna)
    newMember = Individual(stringDna)
    currentGen.add_individual(newMember)
    
  

def run(window, width, height):

    run = True
    clock = pygame.time.Clock()
    fps = 60
    dt = 1/fps

    space = pymunk.Space()
    space.gravity = (0,981)


    

    create_boundaries(space, width, height)
    

    draw_options = pymunk.pygame_util.DrawOptions(window)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        draw(space, window, draw_options)
        space.step(dt)
        clock.tick(fps)
    pygame.quit


if __name__ == "__main__":
    run(window, WIDTH, HEIGHT)











