import pygame as pg
import sys

class Button:
    def __init__(self, text, pos, size, surface, func=lambda:print("no Action")) -> None:
        self.func = func
        self.pos = pos
        self.pressed = False
        self.surface = surface

        self.text = pg.font.SysFont("Arial", 40).render(text,1,pg.Color(236,240,241))

        self.topRect = pg.Rect(pos, size)
        self.topCol = pg.Color(52,73,94)

        self.sides = pg.Rect(pos, size)
        self.sidesCol = pg.Color(44,62,80)


    def draw(self):
        pg.draw.rect(self.surface,self.sidesCol, self.sides,border_radius = 12)
        pg.draw.rect(self.surface,self.topCol, self.topRect,border_radius = 12)
        textRect = self.text.get_rect(center=self.topRect.center)
        self.surface.blit(self.text, textRect)
        self.check_click()


    def check_click(self):
        mousePos = pg.mouse.get_pos()
        if self.topRect.collidepoint(mousePos) and pg.mouse.get_pressed()[0]:
            if not self.pressed:
                self.onClick()


    def onClick(self):
        self.pressed = True
        self.func()
