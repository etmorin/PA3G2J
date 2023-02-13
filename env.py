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
        body.position = (self.window.get_width()/2, 20)
        shape = pm.Poly.create_box(body, (1000, 20))
        self.space.add(body, shape)
        return shape
        
    def addObject(self):
        body = pm.Body()
        body.position = (self.window.get_width()/2, 60)
        shape = pm.Circle(body, 20)
        shape.mass = 10
        self.space.add(body,shape)
        return shape
        
    def step(self,dt):
        self.space.step(dt)