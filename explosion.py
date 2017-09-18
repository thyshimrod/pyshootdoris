import os, sys
import pygame
from pygame.locals import *


class Explosion:
    def __init__(self,mySurface,screen,x,y):
        self.screen=screen
        self.sprite=[]
        self.sprite.append(mySurface.subsurface(pygame.Rect(0,177,32,29)))
        self.sprite.append(mySurface.subsurface(pygame.Rect(32,177,32,29)))
        self.sprite.append(mySurface.subsurface(pygame.Rect(64,177,32,29)))
        self.sprite.append(mySurface.subsurface(pygame.Rect(96,177,32,29)))
        self.sprite.append(mySurface.subsurface(pygame.Rect(128,177,32,29)))
        self.myrect=Rect(x,y,32,29)
        self.etat=0
        self.ticks=0
        
    def move(self):
        if (pygame.time.get_ticks()-self.ticks)>80:
            self.etat+=1
            if self.etat>=5:
                return 0
            self.ticks=pygame.time.get_ticks()
        return 1
            
    def draw(self):
        self.screen.blit(self.sprite[self.etat],self.myrect)