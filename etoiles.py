import os, sys
import pygame
from pygame.locals import *
import random


class Etoile:
    def __init__(self,screen,x,y,color):
        self.screen=screen
        self.speed=[0,4/color]
        self.myrect=Rect(x,y,2,2)
        self.color=(255/color,255/color,255/color)
    
    def move(self):
        self.myrect=self.myrect.move(self.speed)
                
    def draw(self):
        pygame.draw.rect(self.screen,self.color,self.myrect)
        

    