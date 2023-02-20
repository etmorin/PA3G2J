import pygame as pg
import pymunk as pm


class PositionTracker():
    def __init__(self):
        self.objectToFollow = None
        self.startPosition = pg.Vector2(0,0)
        self.objectPosition = None
        self.offset = None
    
    def setObjectToFollow(self, newObject):
        self.objectToFollow = newObject
        self.startPosition = newObject.body.position

    def getRanDistance(self):
        if self.offset:
            return self.offset.x

    def getMaxRanDistance(self):
        pass

    def update(self):
        if not self.objectToFollow:
            return
        self.objectPosition = self.objectToFollow.body.position 
        self.offset = pm.Vec2d(self.objectPosition.x - self.startPosition.x, self.objectPosition.y - self.startPosition.y)