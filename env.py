import pygame as pg
import pymunk as pm
import pymunk.pygame_util

class Env:
    def __init__(self, window) -> None:
        self.window = window
        self.space = pm.Space()
        self.space.gravity =(0, -981)
        pymunk.pygame_util.positive_y_is_up = True
        self.floor = self.createFloor()
    
    def createFloor(self):
        body = pm.Body(body_type=pm.Body.STATIC)
        body.position = (0, 20)
        shape = pm.Poly.create_box(body, (22000, 20))
        shape.friction = 1.0
        self.space.add(body, shape)
        self.graduation = {}
        for i in range(-110,111,1):
            body = pm.Body(body_type=pm.Body.STATIC)
            body.position = (100*i, 5)
            shape = pm.Poly.create_box(body, (5, 10))
            self.space.add(body, shape)
            self.graduation[i] = shape
        return shape
 
    def reset(self):
        self.__init__(self.window)
    
    def step(self,dt):
        self.space.step(dt)