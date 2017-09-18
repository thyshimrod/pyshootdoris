       # -*- coding:cp1252 -*-
try: import psyco;psyco.full()
except:pass

import os, sys
from string import *
import pygame
from pygame.locals import *

black = 0, 0, 0

class myPoint:
    def __init__(self):
        self.x=0
        self.y=0

class PyEditeur:
    def __init__(self, width=800,height=600):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Edit the Catch The doris Mouvement")
        self.points=[]

    def MainLoop(self):
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    sys.exit()
                elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_ESCAPE:
                        sys.exit()
            self.screen.fill(black)
            x,y=pygame.mouse.get_pos()
            font = pygame.font.Font(None, 20)
            text = font.render("X = " + str(x) + " Y = " + str(y), 1, (24,116,205))
            textpos=Rect(300,50,text.get_width(),text.get_height())
            self.screen.blit(text,textpos)
            
            i=0
            self.points.append(myPoint())
            for point in self.points:
                text = font.render(str(point.x) + "," + str(point.y), 1, (24,116,205))
                textpos=Rect(50,10*i,text.get_width(),text.get_height())
                self.screen.blit(text,textpos)
                i+=1
            pygame.display.flip()


if __name__ == "__main__":
    MainWindow = PyEditeur()

    #~ import profile
    #~ profile.run('MainWindow.MainLoop()')
    MainWindow.MainLoop()

