import pymunk as pm
import pymunk.pygame_util
import pygame as pg


class Camera:
    def __init__(self) -> None:
        self.env = None
        self.objectToFollow = None
        self.drawOptions = None
        self.startPosition = pg.Vector2(0,0)
        self.relativePosition = pg.Vector2(0,0)
        
    def setObjectToFollow(self, newObject):
        self.objectToFollow = newObject
        
    def setDrawOptions(self, drawOptions):
        self.drawOptions = drawOptions
        
    def setEnv(self, env):
        self.env = env
        
    def update(self):
        if not self.objectToFollow:
            return
        
        mainBodyPos = self.objectToFollow.body.position
        self.cameraOffset = -pm.Vec2d(mainBodyPos.x - self.startPosition.x, mainBodyPos.y - self.startPosition.y)
        
        self.drawOptions.transform = pm.Transform.translation(self.cameraOffset.x,self.cameraOffset.y)
        self.env.space.debug_draw(self.drawOptions)
