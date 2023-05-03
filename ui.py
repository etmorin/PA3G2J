import pygame as pg
import sys
from positionTracker import PositionTracker

class Button:
    def __init__(self, text, pos, size, surface, func=lambda:print("no Action")) -> None:
        self.func = func
        self.pos = pos
        self.surface = surface
        self.locked = False

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
        
    def lock(self):
        self.locked = True
        
    def unlock(self):
        self.locked = False


    def checkClick(self):
        if self.locked:
            return
        mousePos = pg.mouse.get_pos()
        if self.topRect.collidepoint(mousePos):
                self.onClick()
    
    def checkClick2(self, event):
        if self.locked:
            return False
        if event.type == pg.MOUSEBUTTONUP:
            mousePos = event.pos
            if self.topRect.collidepoint(mousePos):
                self.onClick()
                return True
        return False


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
            

class cycleButton(Button):
    def __init__(self, baseText, pos, size, surface, funcList=[], textList=[]) -> None:
        super().__init__(baseText, pos, size, surface, funcList)
        self.textList = []
        self.textList.append(baseText)
        self.func = []
        self.func.append(lambda: True)
        self.state = 0
        
    def addFunc(self, func, text):
        self.func.append(func)
        self.textList.append(text)
    
    def draw(self):
        pg.draw.rect(self.surface,self.sidesCol, self.sides,border_radius = 12)
        pg.draw.rect(self.surface,self.topCol, self.topRect,border_radius = 12)
        self.text = pg.font.SysFont("Arial", 38).render(self.textList[self.state],1,pg.Color(236,240,241))
        textRect = self.text.get_rect(center=self.topRect.center)
        self.surface.blit(self.text, textRect)
        
    def onClick(self):
        if not self.func:
            return
        self.func[self.state]()
        self.state = (self.state + 1) % len(self.textList)
        if(self.state == 0): self.state = 1
    

    


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
        backgroundRect = textRect.copy()
        backgroundRect.top -= 5
        backgroundRect.left -= 5
        backgroundRect.height += 10
        backgroundRect.width += 10
        pg.draw.rect(self.surface, pg.Color(236, 240, 241), backgroundRect)
        self.surface.blit(self.text, textRect)
        
class GenCounter():
    def __init__(self, surface):
        self.surface = surface
        self.currentGen = 0
        self.style = pg.font.SysFont("Arial", 20)
        
    def next(self):
        self.currentGen += 1
        self.update()
        
    def reset(self):
        self.currentGen = 0
        self.update()
        
    def update(self):
        self.text = self.style.render("Génération actuelle : {}".format(self.currentGen),1,pg.Color(0,0,0))

    def draw(self):
        if self.currentGen == 0:
            return
        topleft = self.surface.get_rect().topleft
        textRect = self.text.get_rect(topleft=pg.Vector2(topleft[0] + 5, topleft[1] + 40))
        self.surface.blit(self.text, textRect)


class StatDisplay():
    def __init__(self, surface) -> None:
        self.surface = surface



class InputBox:
    def __init__(self, x, y, w, h, font, label):
        self.rect = pg.Rect(x, y, w, h)
        self.color = pg.Color('black')
        self.text = ''
        self.font = font
        self.txt_surface = self.font.render(self.text, True, self.color)
        self.active = False
        self.label = label
        self.label_surface = self.font.render(self.label, True, self.color)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = pg.Color('blue') if self.active else pg.Color('black')
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    pass
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, self.color)

    def draw(self, screen):
        screen.blit(self.label_surface, (self.rect.x - self.label_surface.get_width() - 10, self.rect.y + self.rect.h // 2 - self.label_surface.get_height() // 2))
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + self.rect.h // 2 - self.txt_surface.get_height() // 2))
        pg.draw.rect(screen, self.color, self.rect, 2)
