import pymunk as pm
import pymunk.pygame_util
import pygame as pg
import math
from env import *


class App:
    def __init__(self) -> None:
        self.WIDTH = 980
        self.HEIGHT = 720
        self.fps = 60
        self.dt = 1/self.fps
        self.window = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        self.physicsWindow = self.window.subsurface(pg.Rect(self.WIDTH/4,self.HEIGHT/20,self.WIDTH/2,self.HEIGHT/2))
        self.cameraStart = None
        self.shapeToFollow = None
        self.cameraOffset = pg.Vector2((0,0))
        self.draw_options = pymunk.pygame_util.DrawOptions(self.physicsWindow)
        self.running = True
        self.env = Env(self.physicsWindow)

    

    def eventHandler(self, events):
        for event in events:
            if event.type == pg.QUIT:
                self.running = False
                break
            if event.type == pg.KEYDOWN:
                pressed = pg.key.get_pressed()
                if pressed[pg.K_LEFT]: self.env.space._shapes[2].body.apply_force_at_local_point((-10000,0), (0,0))
                if pressed[pg.K_RIGHT]: self.env.space._shapes[2].body.apply_force_at_local_point((10000,0), (0,0))
            
    def updateCamera(self):
        if not self.cameraStart:
            self.cameraStart = self.env.space._shapes[2].body.position
        if not self.shapeToFollow:
            self.shapeToFollow = self.env.space._shapes[2]
        mainBodyPos = self.shapeToFollow.body.position
        self.cameraOffset = pm.Vec2d(-(mainBodyPos.x - self.cameraStart.x), -(mainBodyPos.y - self.cameraStart.y))
        print(self.cameraOffset)
        """
        pressed = pg.key.get_pressed()
        camera_move = pg.Vector2()
        if pressed[pg.K_UP]: camera_move += (0, 1)
        if pressed[pg.K_LEFT]: camera_move += (1, 0)
        if pressed[pg.K_DOWN]: camera_move += (0, -1)
        if pressed[pg.K_RIGHT]: camera_move += (-1, 0)
        if camera_move.length() > 0: camera_move.normalize_ip()
        self.cameraOffset += camera_move
        """    

    def draw(self):
        self.window.fill(pg.Color(210, 218, 226))
        self.physicsWindow.fill("white")
        self.updateCamera()
        self.draw_options.transform = pm.Transform.translation(self.cameraOffset.x,self.cameraOffset.y)
        self.env.space.debug_draw(self.draw_options)
        pg.display.update()

  
    def run(self):
        clock = pg.time.Clock()
        self.env.addObject()
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