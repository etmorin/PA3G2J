import pymunk
import pygame
import pymunk.pygame_util
from genetique import *
import time


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
  

def run(window, width, height):

    run = True
    clock = pygame.time.Clock()
    fps = 60
    dt = 1/fps

    space = pymunk.Space()
    space.gravity = (0,981)

    #première gen
    creatureParameters = {"bodySize" : 30 , "nbrOfArms": 1, "lengthBones": 100,
                       "widthBones" : 10, "radiusArticulations":5,
                       "numberOfArticulations": 2, "muscleStrength": 1000}
    frankensteinDna = Dna(None)
    frankensteinDna.paramToDna(creatureParameters)
    frankenstein = Individual(frankensteinDna)
    frankenstein.draw(space, 300,300,1)

    #autres gen:
   
    frankensteinJunior = Individual("0100001001000010001000100010")
    frankensteinJunior.draw(space, 300,300,2)

    franken2 = Dna(string="0100001001000010001000100010")
    franken2body = Individual(franken2)
    franken2body.draw(space,400,400,4)





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


class Handler():

    def __init__(self, firstGeneration, genSize, repetitions):

        self.currentGen = firstGeneration
        self.repetitions = repetitions
        self.genSize = genSize

    def handling(self):

        self.startTime = time.perf_counter()
        self.currentTime = time.perf_counter()

        while self.currentTime - self.startTime < 20 :
            
            for individual in self.currentGen.individualsList:
                
                todo = "draw et faire la course"

            self.currentTime = time.perf_counter()
        

        self.currentGen = self.currentGen.createNextGeneration(self.genSize)
        


    def repetor(self):

        for i in range (self.repetitions):
            self.handling()






