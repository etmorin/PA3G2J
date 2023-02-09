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
    space.add(body,shape)
  
def add_muscle(space):

    muscle=Muscle(300,300,100,10)
    shape=muscle.get_shape()
    body = muscle.get_body()
    space.add(body,shape)
    return shape
    
def add_bone(space):
    bone=Bone(600,600,100,30)
    shape = bone.get_shape()
    body = bone.get_body()
    space.add(body,shape)
    return shape

def test_joint(space):
    bone1=Bone()

def run(window, width, height):
    run = True
    clock = pygame.time.Clock()
    fps = 60
    dt = 1/fps

    space = pymunk.Space()
    space.gravity = (0,981)

    muscle = add_muscle(space)
    bone = add_bone(space)
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

"""# Create the bones of the skeleton
body1 = pymunk.Body()
body1.position = (100, 100)
segment1 = pymunk.Segment(body1, (0, 0), (50, 0), 5)

body2 = pymunk.Body()
body2.position = (150, 100)
segment2 = pymunk.Segment(body2, (0, 0), (50, 0), 5)

# Connect the bones with joints
joint = pymunk.PivotJoint(body1, body2, (100, 100), (150, 100))
space.add(body1, segment1, body2, segment2, joint)"""

