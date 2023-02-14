import pymunk as pm
import pymunk.pygame_util
import pygame as pg
import ui
from env import Env
from camera import Camera
from walker import Walker


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
        
        self.uiElements = []
        self.setupUI()


    def start(self):
        self.walker = Walker(self.env.space).create(self.env.space)
        self.camera.setObjectToFollow(self.walker)
        
    def reset(self):
        self.env.space.remove(self.walker)
    
    def setupUI(self):
        startButton = ui.ToggleButton("Start", "Reset", (860,650),(100,50), self.window, lambda:self.start(), lambda:self.reset())
        self.uiElements.append(startButton)


    def eventHandler(self, events):
        for event in events:
            if event.type == pg.QUIT:
                self.running = False
                break
            
            if event.type == pg.KEYDOWN:
                pressed = pg.key.get_pressed()
                # temporaire
                if pressed[pg.K_LEFT]: self.env.space._shapes[2].body.apply_force_at_local_point((-10000,0), (0,0))
                if pressed[pg.K_RIGHT]: self.env.space._shapes[2].body.apply_force_at_local_point((10000,0), (0,0))
                
            if event.type == pg.MOUSEBUTTONDOWN:
                for elem in self.uiElements:
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