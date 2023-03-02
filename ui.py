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
        self.individualToFollow = None

    def setObjectToFollow(self, individualToFollow):
        self.individualToFollow = individualToFollow

    def update(self):
        self.distance = self.individualToFollow.get_currentScore() if self.individualToFollow else 0.00
        self.text = self.style.render("Distance parcourue: {:.2f}m".format(self.distance),1,pg.Color(0,0,0))

    def draw(self):
        self.update()
        textRect = self.text.get_rect(center=pg.Vector2(self.surface.get_rect().centerx,21))
        self.surface.blit(self.text, textRect)
    
    def reset(self):
        self.__init__(self.surface)
        
class GenTimer():
    def __init__(self, surface):
        self.surface = surface
        self.temps = None
        self.style = pg.font.SysFont("Arial", 28)
        
    def update(self,startTime, currentTime, totalTime):
        self.temps = totalTime - (currentTime-startTime)
        self.text = self.style.render("{:.2f}s".format(self.temps),1,pg.Color(0,0,0))

    def draw(self):
        topleft = self.surface.get_rect().topleft
        textRect = self.text.get_rect(topleft=pg.Vector2(topleft[0] + 10, topleft[1] + 10))
        self.surface.blit(self.text, textRect)