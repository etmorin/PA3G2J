import pymunk as pm
import pymunk.pygame_util
import pygame as pg
import numpy as np
import matplotlib.pyplot as plt
import random
import time
import ui
from env import Env
from camera import Camera
from positionTracker import *
from members import *
from genetique import *
import pandas as pd
import os
from datetime import datetime


class App:
    def __init__(self) -> None:
        self.WIDTH = 1920
        self.HEIGHT = 1080
        self.fps = 60
        self.dt = 1/self.fps
        self.window = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        self.physicsWindow = self.window.subsurface(pg.Rect(self.WIDTH/8,self.HEIGHT/20,self.WIDTH/1.3,self.HEIGHT/1.3))
        self.env = Env(self.physicsWindow)
        self.drawOptions = pymunk.pygame_util.DrawOptions(self.physicsWindow)
        self.camera = Camera()
        self.camera.setDrawOptions(self.drawOptions)
        self.camera.setEnv(self.env)
        self.running = True
        self.genSize = 10
        self.genTime = 15
        self.currentGen = 0
        self.genHistory = []
        self.maxGen = 100
        self.selectionStrat = "bestFirst"
        self.population = None
        self.startTime = None
        self.currentTime = None
        
        self.uiElements = {}
        self.interactables = {}
        self.setupUI()

    def start(self):
        self.population = Generation(self.currentGen, self.genSize, self.env.space)
        self.currentGen += 1
        self.startTime = time.time()
        
        timer = ui.GenTimer(self.physicsWindow)
        self.uiElements["timer"] = timer
        counter = ui.GenCounter(self.window)
        counter.next()
        self.uiElements["genCounter"] = counter
        self.uiElements["obstacleToggle"].lock()
        self.uiElements["selectionToggle"].lock()
            
        
        
    
    def startNextGen(self):
        # check if score hasn't improved in 10 gen
        parents = None
        if self.currentGen > 10:
            multigenAvg = 0
            for  i in range(-1,-11,-1):
                genScore = self.genHistory[i].findBestIndividual(1)[0].get_bestScore()
                multigenAvg += genScore
            multigenAvg = multigenAvg/10
            # if so, roll back 10 gen to gen new parents
            if self.population.findBestIndividual(1)[0].get_bestScore() < multigenAvg:
                parents = self.genHistory[-10].findBestIndividual(2) if self.selectionStrat == "bestFirst" else self.genHistory[-10].get_individualList()
        # else continue
        self.genHistory.append(self.population)
        if not parents:
            parents = self.population.findBestIndividual(2) if self.selectionStrat == "bestFirst" else self.population.get_individualList()
        newPopulation = self.population.createNextGeneration(self.genSize, parents)
        self.population = newPopulation
        self.currentGen += 1
        self.uiElements["genCounter"].next()
        self.env.reset()
        i = 0
        for individual in self.population.get_individualList():
            individual.createBody(self.env.space, 0, 200, 2**i)
            i += 1
        self.startTime = time.time()

    def reset(self):
        del self.uiElements["timer"]
        self.uiElements["distanceCounter"].reset()
        self.uiElements["genCounter"].reset()
        self.uiElements["obstacleToggle"].unlock()
        self.uiElements["selectionToggle"].unlock()
        self.population = None
        self.currentGen = 0
        self.env.reset()
        self.run()
    
    def changeSelectionStrat(self,strat):
        self.selectionStrat = strat
    
    def setupUI(self):
        startButton = ui.ToggleButton("Start", "Reset", (1780,950),(100,50), self.window, lambda:self.start(), lambda:self.reset())
        self.interactables["startButton"] = startButton
        self.uiElements["startButton"] = startButton
        distanceCounter = ui.DistanceCounter(self.window)
        self.uiElements["distanceCounter"] = distanceCounter
        obstacleToggle = ui.cycleButton("Changer les obstacles", (self.WIDTH/2-190,self.HEIGHT-180),(380,50), self.window)
        obstacleToggle.addFunc(lambda:self.env.createObstacleSet("hedges"), "Aucun")
        obstacleToggle.addFunc(lambda:self.env.createObstacleSet("incline") , "100m haies")
        obstacleToggle.addFunc(lambda:self.env.resetObstacles(), "pente")
        
        self.uiElements["obstacleToggle"] = obstacleToggle
        self.interactables["obstacleToggle"] = obstacleToggle
        
        selectionToggle = ui.cycleButton("Mode de Sélection : Meilleur Toujours", (self.WIDTH/2-380, self.HEIGHT-125),(760,50), self.window)
        selectionToggle.addFunc(lambda:self.changeSelectionStrat("bestFirst"), "Mode de Sélection : Performances Pondérées")
        selectionToggle.addFunc(lambda:self.changeSelectionStrat("weighted") , "Mode de Sélection : Meilleur Toujours")
        
        self.uiElements["selectionToggle"] = selectionToggle
        self.interactables["selectionToggle"] = selectionToggle

    
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
        if not self.population or self.currentGen > self.maxGen:
            self.endingHandler()
            return
        self.currentTime = time.time()
        self.uiElements["timer"].update(self.startTime, self.currentTime, self.genTime)
        if self.currentTime >= self.startTime + self.genTime:
            self.startNextGen()
            
    
    def endingHandler(self):

        if self.currentGen <= self.maxGen:
            return
        
        self.saveHistory()
        bestScores = []
        avgScores = []
        i = 1
        for gen in self.genHistory:
            genBestScore = gen.findBestIndividual(1)[0].get_bestScore()
            totalScore = 0
            individialList = gen.get_individualList()
            for individial in individialList:
                totalScore += individial.get_bestScore()
            genAvgScore = totalScore / len(individialList)
            bestScores.append(genBestScore)
            avgScores.append(genAvgScore)

        bestScores_smoothed = pd.Series(bestScores).expanding().mean()
       
        averageScores_smoothed = pd.Series(bestScores).expanding().mean()
        
        plt.plot(range(1,len(bestScores)+1), bestScores)
        plt.plot(range(1, len(bestScores_smoothed)+1), bestScores_smoothed, label="Moyenne Mobile")

        plt.title("Évolution du meilleur score au fil des générations")
        plt.autoscale(True)
        plt.xticks(np.arange(1,self.maxGen+1,1))
        plt.ylabel("Meilleur Score")
        plt.xlabel("Génération")
        plt.show()
        
        plt.plot(range(1,len(avgScores)+1), avgScores)
        plt.plot(range(1, len(averageScores_smoothed)+1), averageScores_smoothed, label="Moyenne Mobile")

        plt.title("Évolution du score moyen au fil des générations")
        plt.autoscale(True)
        plt.xticks(np.arange(1,self.maxGen+1,1))
        plt.ylabel("Score Moyen")
        plt.xlabel("Génération")
        plt.show()  
        self.uiElements["startButton"].toggled = False
        self.uiElements["startButton"].draw()
        self.reset()
                 
        
        
           
    def updateCamera(self):
        if self.population:
            bestScore = -100.0
            bestIndividual = None
            for individual in self.population.get_individualList():
                 score = individual.get_currentScore()
                 if score > bestScore:
                     bestScore = score
                     bestIndividual = individual
            self.camera.setObjectToFollow(bestIndividual.get_bodyInSpace().getCenterShape())
            self.uiElements["distanceCounter"].setObjectToFollow(bestIndividual)
        self.camera.update()    
 

    def draw(self):
        self.window.fill(pg.Color(210, 218, 226))
        self.physicsWindow.fill("white")
        self.updateCamera()
        for elem in self.uiElements:
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
    
    def saveHistory(self):

        
        best = None
        bestIndividual = None

        if not os.path.exists("history"):
            os.makedirs("history")

        currentTime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        filename = f"history/simulation_{currentTime}.txt"

        with open(filename,'w') as file:

            file.write(f"Simulation from {currentTime} \n")

            for generation in self.genHistory:
                file.write(f"Entering generation : {generation.generationDepth} \n")
                for individual in range(self.genSize):
                    currentIndividual = generation.individualsList[individual]
                    currentDna = currentIndividual.dna
                    file.write(f"{currentDna.geneString } with best score of {currentIndividual.bestScore}\n")
                    if not best or currentIndividual.bestScore > best :
                        best = currentIndividual.bestScore
                        bestIndividual = currentIndividual

            file.write(f"Best overall individual is \n {bestIndividual.dna.geneString} with a score of {best}")





def setup():
    pg.init()
    app = App()
    app.run()


if __name__ == "__main__":
    setup()