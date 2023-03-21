import pygame as pg
import pymunk as pm
import pymunk.pygame_util

class Env:
    def __init__(self, window) -> None:
        self.window = window
        self.space = pm.Space()
        self.space.gravity =(0, -981)
        self.floorIncline = 0
        self.currentObstacles = "Aucun"
        pymunk.pygame_util.positive_y_is_up = True
        self.floor = self.createFloor()
    
    def set_floorIncline(self, incline):
        self.floorIncline = incline
    
    
    def createFloor(self):
        body = pm.Body(body_type=pm.Body.STATIC)
        body.position = (0, 20)
        body.center_of_gravity = (0,0)
        body._set_angle(self.floorIncline*3.14/180)
        shape = pm.Poly.create_box(body, (22000, 20))
        shape.friction = 1.0
        self.space.add(body, shape)
        self.graduation = {}
        self.obstacles = {}
        self.createGraduations()
        return shape
    
    def createGraduations(self):
        for i in range(-110,111,1):
            body = pm.Body(body_type=pm.Body.STATIC)
            body.position = (100*i, 5+1.75*i*self.floorIncline)
            shape = pm.Poly.create_box(body, (5, 10))
            self.space.add(body, shape)
            self.graduation[i] = shape
        
    
    def createObstacleSet(self, obstacles):
        self.currentObstacles = obstacles
        if obstacles == "hedges":
            self.resetObstacles()
            self.createHedges()
        elif obstacles == "incline":
            self.resetObstacles()
            self.set_floorIncline(5)
            self.resetFloor()
            
    def createHedges(self):
        for i in range(5,110,5):
            body = pm.Body(body_type=pm.Body.STATIC)
            body.position = (100*i, 120)
            shape = pm.Poly.create_box(body, (5, 200))
            self.space.add(body, shape)
            self.obstacles[i] = shape
            
            
    def resetObstacles(self):
        if (self.floorIncline != 0): self.floorIncline = 0; self.resetFloor()
        for obstacle in self.obstacles.values():
            self.space.remove(obstacle)
    
    def resetFloor(self):
        for graduation in self.graduation.values():
            self.space.remove(graduation)
        self.space.remove(self.floor)
        self.floor = self.createFloor()
 
    def reset(self):
        incline = self.floorIncline
        currentObstacles = self.currentObstacles
        self.__init__(self.window)
        self.floorIncline = incline
        self.resetFloor()
        self.resetObstacles()
        self.createObstacleSet(currentObstacles)
    
    def step(self,dt):
        self.space.step(dt)