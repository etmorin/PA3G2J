import pymunk
import pygame
import pymunk.pygame_util
from  members import *

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

    frankenstein = Creature(space,500,600,50,3,100,10,10)
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

