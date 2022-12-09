import pymunk as pm
import pymunk.pygame_util
import pygame as pg
import math


class App:
    def __init__(self, env) -> None:
        self.WIDTH = 980
        self.HEIGHT = 720
        self.fps = 60
        self.window = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        self.draw_options = pymunk.pygame_util.DrawOptions(self.window)
        self.running = True
        self.env = env


    def eventHandler(self, events):
        for event in events:
            print(event.type)
            if event.type == pg.QUIT:
                print("closing")
                self.running = False
                break

    def draw(self):
        self.window.fill("white")
        self.env.space.debug_draw(self.draw_options)
    
    def run(self):
        clock = pg.time.Clock()

        while self.running:
            self.eventHandler(pg.event.get())

            self.draw()
            clock.tick(self.fps)
        print("quitting")
        pg.quit()


class Env:
    def __init__(self) -> None:
        self.space = pm.Space()
        self.space.gravity =(0, 981)


def setup():
    pg.init()
    env = Env()
    app = App(env)
    app.run()



if __name__ == "__main__":
    setup()