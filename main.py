import pymunk as pm
import pymunk.pygame_util
import pygame as pg
import math


class App:
    def __init__(self, env) -> None:
        self.WIDTH = 980
        self.HEIGHT = 720
        self.fps = 60
        self.dt = 1/self.fps
        self.window = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        self.physicsWindow = self.window.subsurface(pg.Rect(self.WIDTH/4,self.HEIGHT/20,self.WIDTH/2,self.HEIGHT/2))
        self.cameraOffset = pg.Vector2((0,0))
        self.draw_options = pymunk.pygame_util.DrawOptions(self.physicsWindow)
        self.running = True
        self.env = env

    def addObject(self):
        body = pm.Body()
        body.position = (self.physicsWindow.get_width()/2, self.physicsWindow.get_height() - 100)
        shape = pm.Circle(body, 20)
        shape.mass = 10
        self.env.space.add(body,shape)

    def eventHandler(self, events):
        for event in events:
            if event.type == pg.QUIT:
                self.running = False
                break
            
    def updateCamera(self):
        pressed = pygame.key.get_pressed()
        camera_move = pygame.Vector2()
        if pressed[pygame.K_UP]: camera_move += (0, 1)
        if pressed[pygame.K_LEFT]: camera_move += (1, 0)
        if pressed[pygame.K_DOWN]: camera_move += (0, -1)
        if pressed[pygame.K_RIGHT]: camera_move += (-1, 0)
        if camera_move.length() > 0: camera_move.normalize_ip()
        camera += camera_move*(dt/5)
            

    def draw(self):
        self.window.fill(pg.Color(210, 218, 226))
        self.physicsWindow.fill("white")
        self.updateCamera()
        self.draw_options.transform = pm.Transform.translation(self.cameraOffset.x,self.cameraOffset.y)
        self.env.space.debug_draw(self.draw_options)
        pg.display.update()
        
        
    def createFloor(self):
        body = pm.Body(body_type=pm.Body.STATIC)
        body.position = (self.physicsWindow.get_width()/2, 20)
        shape = pm.Poly.create_box(body, (self.WIDTH, 20))
        self.env.space.add(body, shape)
        #body.angle += 0.2
        #self.env.space.reindex_shape(shape)
    
    def run(self):
        clock = pg.time.Clock()
        self.createFloor()
        self.addObject()
        while self.running:
            self.eventHandler(pg.event.get())

            self.draw()
            self.env.step(self.dt)
            clock.tick(self.fps)
        pg.display.quit()
        pg.quit()


class Env:
    def __init__(self) -> None:
        self.space = pm.Space()
        self.space.gravity =(0, -981)
        pymunk.pygame_util.positive_y_is_up = True
        
    def step(self,dt):
        self.space.step(dt)


def setup():
    pg.init()
    env = Env()
    app = App(env)
    app.run()



if __name__ == "__main__":
    setup()