import pymunk as pm
import pymunk.pygame_util
import pygame as pg
import ui
from env import Env
from camera import Camera
from members import *
from genetique import *


class App:
    def __init__(self) -> None:
        self.WIDTH = 980
        self.HEIGHT = 720
        self.fps = 60
        self.dt = 1/self.fps
        self.window = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        self.physicsWindow = self.window.subsurface(pg.Rect(self.WIDTH/4,self.HEIGHT/20,self.WIDTH/2,self.HEIGHT/2))
        self.env = Env(self.physicsWindow)
        self.drawOptions = pymunk.pygame_util.DrawOptions(self.physicsWindow)
        self.camera = Camera()
        self.camera.setDrawOptions(self.drawOptions)
        self.camera.setEnv(self.env)
        self.running = True
        self.genSize = 10
        self.genTime = 10
        self.population = []
        
        self.uiElements = []
        self.interactables = []
        self.setupUI()


    def start(self):
        for i in range(1, self.genSize+1,1):
            creature = Creature(self.env.space, 0, 50, 20, 2, 40, 5, 5, 1, 2000)
            self.population.append(creature)
        self.camera.setObjectToFollow(self.population[0].getCenterShape())
        distanceTracker = self.uiElements[1]
        distanceTracker.setObjectToFollow(self.population[0].getCenterShape())
        
    def reset(self):
        self.env.space.remove(self.walker)
    
    def setupUI(self):
        startButton = ui.ToggleButton("Start", "Reset", (860,650),(100,50), self.window, lambda:self.start(), lambda:self.reset())
        self.interactables.append(startButton)
        self.uiElements.append(startButton)
        distanceCounter = ui.DistanceCounter(self.window)
        self.uiElements.append(distanceCounter)

    
    def eventHandler(self, events):
        for event in events:
            if event.type == pg.QUIT:
                self.running = False
                break
            
            if event.type == pg.KEYDOWN:
                pressed = pg.key.get_pressed()
                
            if event.type == pg.MOUSEBUTTONDOWN:
                for elem in self.interactables:
                    elem.checkClick()
                
           
    def updateCamera(self):
        self.camera.update()
 

    def draw(self):
        self.window.fill(pg.Color(210, 218, 226))
        self.physicsWindow.fill("white")
        self.updateCamera()
        for elem in self.uiElements:
            elem.draw()
        pg.display.update()


    def run(self):
        clock = pg.time.Clock()
        while self.running:
            self.eventHandler(pg.event.get())

            self.draw()
            self.env.step(self.dt)
            clock.tick(self.fps)
        pg.display.quit()
        pg.quit()


def setup():
    pg.init()
    app = App()
    app.run()


if __name__ == "__main__":
    setup()