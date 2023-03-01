import pymunk as pm
import pymunk.pygame_util
import pygame as pg
import numpy as np
import random
import time
import ui
from env import Env
from camera import Camera
from positionTracker import *
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
        self.genSize = 2
        self.genTime = 10
        self.currentGen = 0
        self.population = None
        self.startTime = None
        self.currentTime = None
        
        self.uiElements = {}
        self.interactables = {}
        self.setupUI()


    def start(self):
        
        self.population = Generation(self.currentGen, self.genSize, self.env.space)
        self.startTime = time.time()
        
        timer = ui.GenTimer(self.physicsWindow)
        self.uiElements["timer"] = timer

        distanceTracker = self.uiElements["distanceCounter"]
        distanceTracker.setObjectToFollow(self.population.get_individualList()[0].get_bodyInSpace().getCenterShape())


        """for i in range(self.genSize):
            creature = Creature(self.env.space, 0, 50, 20, 2, 40, 5, 5, 1, 2000, 2**i)
            positionTracker = PositionTracker()
            positionTracker.setObjectToFollow(creature.getCenterShape())
            dna = Dna(None).paramToDna(dict(zip(PARAMETERS,creature.parameters)))
            indinvidual = Individual(dna,creature)
            self.population.append(indinvidual)
            self.trackers.append(positionTracker)"""
        
        """weights = [tracker.getMaxRanDistance()*100 for tracker in self.trackers]
        for weight in weights:
            print("weight: {}, sum : {}".format(weight, sum(weights)))
            weight = weight/sum(weights)
        newGeneration = []
        for i in range(self.genSize):
            parent1, parent2 = np.random.choice(self.population,size=2,replace=False,p=weights)
            child = parent1.reproduce(parent2)
            newGeneration.append(child)
        self.env.reset()
        self.currentGen += 1
        self.population = newGeneration
        for individual in self.population:
            parameters = Dna.dnaToParam(indinvidual.get_dna())
            parameters["space"] = self.env.space
            parameters["posX"] = 0
            parameters["posY"] = 50
            individual.set_bodyInSpace(Creature(**parameters))"""
            
        
        
    
    def startNextGen(self):
        self.currentGen += 1
        newPopulation = self.population.createNextGeneration(self.genSize)
        self.population = newPopulation
        self.env.reset()
        i = 0
        for individual in self.population.get_individualList():
            individual.createBody(self.env.space, 0, 100, 2**i)
            i += 1
        self.startTime = time.time()

    def reset(self):
        del self.uiElements["timer"]
        self.uiElements["distanceCounter"].reset()
        self.population = None
        self.env.reset()
        self.run()
    
    def setupUI(self):
        startButton = ui.ToggleButton("Start", "Reset", (860,650),(100,50), self.window, lambda:self.start(), lambda:self.reset())
        self.interactables["startButton"] = startButton
        self.uiElements["startButton"] = startButton
        distanceCounter = ui.DistanceCounter(self.window)
        self.uiElements["distanceCounter"] = distanceCounter

    
    def eventHandler(self, events):
        for event in events:
            if event.type == pg.QUIT:
                self.running = False
                break
            
            if event.type == pg.KEYDOWN:
                pressed = pg.key.get_pressed()
                
            if event.type == pg.MOUSEBUTTONDOWN:
                for elem in self.interactables:
                    self.interactables[elem].checkClick()
    
    def genHandler(self):
        if not self.population:
            return
        self.currentTime = time.time()
        self.uiElements["timer"].update(self.startTime, self.currentTime, self.genTime)
        if self.currentTime >= self.startTime + self.genTime:
            self.startNextGen()
        
           
    def updateCamera(self):
        if self.population:
            bestScore = -100.0
            bestIndividual = None
            for individual in self.population.get_individualList():
                 score = individual.get_currentScore()
                 if score > bestScore:
                     bestIndividual = individual
            self.camera.setObjectToFollow(individual.get_bodyInSpace().getCenterShape())
        self.camera.update()
 

    def draw(self):
        self.window.fill(pg.Color(210, 218, 226))
        self.physicsWindow.fill("white")
        self.updateCamera()
        for elem in self.uiElements:
            print(elem)
            self.uiElements[elem].draw()
        pg.display.update()


    def run(self):
        clock = pg.time.Clock()
        while self.running:
            self.eventHandler(pg.event.get())
            self.genHandler()
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