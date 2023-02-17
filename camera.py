import pymunk as pm
import pymunk.pygame_util
import pygame as pg
import string


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
    
    def drawGraduations(self):
        for value, graduation in self.env.graduation.items():
            text = pg.font.SysFont("Arial", 30).render(str(value),1,pg.Color(0,0,0))
            posx, posy = graduation.body.position
            textRect = text.get_rect(center=(posx + self.offset.x, posy + 375 - self.offset.y))
            self.drawOptions.surface.blit(text, textRect)
        
    def update(self):
        if not self.objectToFollow:
            self.env.space.debug_draw(self.drawOptions)
            return
        self.objectPosition = self.objectToFollow.body.position 
        windowRect = self.drawOptions.surface.get_rect()
        self.offset = -pm.Vec2d(self.objectPosition.x - windowRect.width/2, self.objectPosition.y - windowRect.height/2)
        self.drawOptions.transform = pm.Transform.translation(self.offset.x, self.offset.y)
        self.env.space.debug_draw(self.drawOptions)
        self.drawGraduations()