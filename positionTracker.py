import pygame as pg
import pymunk as pm


class PositionTracker():
    def __init__(self):
        self.objectToFollow = None
        self.startPosition = pg.Vector2(0,0)
        self.objectPosition = None
        self.offset = None
        self.ranDistance = 0.0
        self.maxRanDistance = 0.0
    
    def setObjectToFollow(self, newObject):
        self.objectToFollow = newObject
        self.startPosition = newObject.body.position

    def getRanDistance(self):
        return self.ranDistance/100

    def getMaxRanDistance(self):
        return self.maxRanDistance/100

    def update(self):
        if not self.objectToFollow:
            return
        self.objectPosition = self.objectToFollow.body.position 
        self.offset = pm.Vec2d(self.objectPosition.x - self.startPosition.x, self.objectPosition.y - self.startPosition.y)
        self.ranDistance = self.offset.x
        if self.offset.x > self.maxRanDistance:
            self.maxRanDistance = self.offset.x