import pymunk as pm
import pymunk.pygame_util
import pygame as pg


class Camera:
    def __init__(self) -> None:
        self.env = None
        self.objectToFollow = None
        self.drawOptions = None
        self.startPosition = pg.Vector2(0,0)
        self.objectPosition = None
        
    def setObjectToFollow(self, newObject):
        self.objectToFollow = newObject
        
        
    def setDrawOptions(self, drawOptions):
        self.drawOptions = drawOptions
        
    def setEnv(self, env):
        self.env = env
        
    def update(self):
        if not self.objectToFollow:
            self.env.space.debug_draw(self.drawOptions)
            return
        self.objectPosition = self.objectToFollow.body.position 
        windowRect = self.drawOptions.surface.get_rect()
        cameraOffset = pm.Vec2d(-self.objectPosition.x + windowRect.width/2, -self.objectPosition.y + windowRect.height/2)
        self.drawOptions.transform = pm.Transform.translation(cameraOffset.x, cameraOffset.y)
        self.env.space.debug_draw(self.drawOptions)
