import pymunk as pm
import pymunk.pygame_util
import pygame as pg
import math


class App:

    def __init__(self) -> None:
        self.WIDTH = 980
        self.HEIGHT = 720
        self.fps = 60
        self.window = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        self.draw_options = pymunk.pygame_util.DrawOptions(self.window)
        self.run = True


    def eventHandler(self, events: pg.List[pg.Event]):
        for event in events:
            if event.type == pg.QUIT:
                self.run = False
                break

    def draw(space, window)
    
    def run(self):
        clock = pg.time.Clock()

        while self.run:
            self.eventHandler(pg.event.get())

            clock.tick(self.fps)

        pg.quit()


class Env:
    def __init__(self) -> None:
        self.space = pm.Space()
        self.space.gravity((0, 981))


def setup():
    pg.init()
    env = Env()
    app = App()
    app.run()



if __name__ == "__main__":
    setup()