from Controller.Handlers import *
import pygame as pg
from OpenGL.GL import *
import ctypes

class WindowManger:    
    def __init__(self, fullscreen=True, clock_rate=60):
        InitEvent.publish(status="Initializing", payload="| |-Initializing WindowManager...")

        pg.init()
        # Tell Pygame to request an OpenGL ES 3.1 Context
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_ES)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 1)

        if fullscreen:
            monitors = pg.display.get_desktop_sizes()
            self.resolution = (monitors[0][0], monitors[0][1])
        self.screen = pg.display.set_mode(self.resolution, pg.OPENGL | pg.DOUBLEBUF)
        glClearColor(0.3921,0.5843,0.9294,1.) #Cornflower blue default background ;)

        self.clock_rate = clock_rate
        self.clock = pg.time.Clock()

        InitEvent.publish(status="Complete", payload="Done.\n")

    def __call__(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                RuntimeEvent.publish(status="Running", payload="Quit")

        self.clock.tick(self.clock_rate)

        #glClear(GL_COLOR_BUFFER_BIT)
        pg.display.flip()

    def __del__(self):
        pg.quit()
        RuntimeEvent.publish(status="Stopped", payload="WindowManager Stopped.")
        
    