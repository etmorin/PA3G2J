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
        self.fps = 54
        self.dt = 1/self.fps
        self.window = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        self.physicsWindow = self.window.subsurface(pg.Rect(self.WIDTH/8,self.HEIGHT/20,self.WIDTH/1.3,self.HEIGHT/1.3))
        self.env = Env(self.physicsWindow)
        self.drawOptions = pymunk.pygame_util.DrawOptions(self.physicsWindow)
        self.camera = Camera()
        self.camera.setDrawOptions(self.drawOptions)
        self.camera.setEnv(self.env)
        self.running = True
        self.genSize = 6
        self.genTime = 10
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

    def display_input_window(self):

        input_window = pg.display.set_mode((400, 300))
        pg.display.set_caption("Input Parameters")

        font = pg.font.Font(None, 32)
        self.input_boxes = [
            ui.InputBox(150, 30, 140, 32, font, "Gen Size"),
            ui.InputBox(150, 90, 140, 32, font, "Gen Time"),
            ui.InputBox(150, 150, 140, 32, font, "Max Gen"),
        ]
        submit_button = ui.Button("Submit", (150, 210), (100, 50), input_window, self.submit)

        self.done = False
        self.submitted = False

        while not self.done:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.done = True
                    self.submitted = False
                for box in self.input_boxes:
                    box.handle_event(event)

                if submit_button.checkClick2(event):
                    self.submit()

            input_window.fill((255, 255, 255))
            for box in self.input_boxes:
                box.draw(input_window)
            submit_button.draw()
            pg.display.flip()
            pg.time.Clock().tick(30)

        pg.display.set_caption("Main Window")
        print("exiting submitted prompt window")
        return self.submitted

    def submit(self):
        genSize_input = int(self.input_boxes[0].text)
        genTime_input = int(self.input_boxes[1].text)
        maxGen_input = int(self.input_boxes[2].text)
        if genSize_input > 0 and genTime_input > 0 and maxGen_input > 0:
            self.genSize = genSize_input
            self.genTime = genTime_input
            self.maxGen = maxGen_input
            self.done = True
            self.submitted = True
        

    def start(self):
        """
        Starts the simulation with the setting set before pressing start
        """
        
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
        # check if score hasn't improved in 5 gen
        parents = None
        if self.currentGen > 5:
            multigenAvg = 0
            for  i in range(-1,-6,-1):
                genScore = self.genHistory[i].findBestIndividual(1)[0].get_bestScore()
                multigenAvg += genScore
            multigenAvg = multigenAvg/5
            # if so, roll back 5 gen to gen new parents
            if self.population.findBestIndividual(1)[0].get_bestScore() < multigenAvg:
                parents = self.genHistory[-5].findBestIndividual(2) if self.selectionStrat == "bestFirst" else self.genHistory[-5].get_individualList()
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
            individual.createBody(self.env.space, 0, 350, 2**i)
            i += 1
        self.startTime = time.time()

    def reset(self):
        
        """        if self.population and self.currentGen > 0:
            self.saveHistory()
            self.displayGraphs()"""


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
        obstacleToggle.addFunc(lambda:self.env.createObstacleSet("Aucun"), "pente")
        
        self.uiElements["obstacleToggle"] = obstacleToggle
        self.interactables["obstacleToggle"] = obstacleToggle
        
        selectionToggle = ui.cycleButton("Mode de Sélection : Meilleur Toujours", (self.WIDTH/2-380, self.HEIGHT-125),(760,50), self.window)
        selectionToggle.addFunc(lambda:self.changeSelectionStrat("weighted") , "Mode de Sélection : Meilleur Toujours")
        selectionToggle.addFunc(lambda:self.changeSelectionStrat("bestFirst"), "Mode de Sélection : Performances Pondérées")
        
        
        self.uiElements["selectionToggle"] = selectionToggle
        self.interactables["selectionToggle"] = selectionToggle

    def eventHandler(self, events):
        for event in events:
            if event.type == pg.QUIT:
                self.onExit()
                self.running = False
                break
            
            if event.type == pg.KEYDOWN:
                pressed = pg.key.get_pressed()
                
            if event.type == pg.MOUSEBUTTONDOWN:
                for elem in self.interactables:
                    self.interactables[elem].checkClick()
    
    def onExit(self):
        if not self.population or self.currentGen > self.maxGen:
            self.endingHandler()
            return
        self.saveHistory()
        self.displayGraphs()

    def displayGraphs(self):
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

        plt.plot(range(1, len(bestScores) + 1), bestScores)
        plt.plot(range(1, len(bestScores_smoothed) + 1), bestScores_smoothed, label="Moyenne Mobile")
        plt.title("Évolution du meilleur score au fil des générations")
        plt.autoscale(True)
        plt.xticks(np.arange(1, self.maxGen + 1, 1))
        plt.ylabel("Meilleur Score")
        plt.xlabel("Génération")
        plt.show()

        plt.plot(range(1, len(avgScores) + 1), avgScores)
        plt.plot(range(1, len(averageScores_smoothed) + 1), averageScores_smoothed, label="Moyenne Mobile")
        plt.title("Évolution du score moyen au fil des générations")
        plt.autoscale(True)
        plt.xticks(np.arange(1, self.maxGen + 1, 1))
        plt.ylabel("Score Moyen")
        plt.xlabel("Génération")
        plt.show()
        

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
        self.displayGraphs()
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

        if not self.display_input_window():
            print("test entering displayinput")
            self.running = False
        else:
            self.running = True

        print("entering main run loop")
        print(f"{self.genSize} and {self.genTime} and {self.maxGen}")
        self.window = pg.display.set_mode((self.WIDTH, self.HEIGHT))
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