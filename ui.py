import pygame as pg
import sys
from positionTracker import PositionTracker

class Button:
    def __init__(self, text, pos, size, surface, func=lambda:print("no Action")) -> None:
        self.func = func
        self.pos = pos
        self.surface = surface

        self.text = pg.font.SysFont("Arial", 38).render(text,1,pg.Color(236,240,241))

        self.topRect = pg.Rect(pos, size)
        self.topCol = pg.Color(52,73,94)

        self.sides = pg.Rect(pos, size)
        self.sidesCol = pg.Color(44,62,80)


    def draw(self):
        pg.draw.rect(self.surface,self.sidesCol, self.sides,border_radius = 12)
        pg.draw.rect(self.surface,self.topCol, self.topRect,border_radius = 12)
        textRect = self.text.get_rect(center=self.topRect.center)
        self.surface.blit(self.text, textRect)


    def checkClick(self):
        mousePos = pg.mouse.get_pos()
        if self.topRect.collidepoint(mousePos):
                self.onClick()


    def onClick(self):
        self.func()


class ToggleButton(Button):
    def __init__(self, text1, text2, pos, size, surface, func1=lambda : print("no first Action"),
                                                 func2=lambda : print("no second Action")) -> None:
        super().__init__(text1, pos, size, surface, func1)
        self.toggled = False
        self.text2 = pg.font.SysFont("Arial", 38).render(text2,1,pg.Color(236,240,241))
        self.func2 = func2
    
    def draw(self):
        text = self.text if not self.toggled else self.text2
        pg.draw.rect(self.surface,self.sidesCol, self.sides,border_radius = 12)
        pg.draw.rect(self.surface,self.topCol, self.topRect,border_radius = 12)
        textRect = text.get_rect(center=self.topRect.center)
        self.surface.blit(text, textRect)
        
    def onClick(self):
        if not self.toggled:
            self.toggled = True
            self.func()
        else:
            self.toggled = False
            self.func2()


class DistanceCounter():
    def __init__(self, surface, objectToFollow = None):
        self.surface = surface
        self.distance = 0.00
        self.style = pg.font.SysFont("Arial", 28)
        self.positionTracker = PositionTracker()
        if objectToFollow:
            self.positionTracker.setObjectToFollow(objectToFollow)

    def setObjectToFollow(self, objectToFollow):
        self.positionTracker.setObjectToFollow(objectToFollow)

    def update(self):
        self.distance = float(self.positionTracker.getRanDistance()/100) if self.positionTracker.getRanDistance() else self.distance
        self.text = self.style.render("Distance parcourue: {:.2f}m".format(self.distance),1,pg.Color(0,0,0))

    def draw(self):
        self.update()
        textRect = self.text.get_rect(center=pg.Vector2(self.surface.get_rect().centerx,21))
        self.surface.blit(self.text, textRect)