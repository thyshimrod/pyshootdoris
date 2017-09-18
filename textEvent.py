import os, sys
import pygame
from pygame.locals import *

C_EFFECT_NONE=0
C_EFFECT_BLINK=1

class textEvent:
    def __init__(self,screen,message,ticks,duree,effect=C_EFFECT_NONE,x=-1,y=-1,font=36,r=255,g=196,b=34):
        self.screen=screen
        self.ticks=ticks
        self.duree=duree
        self.effect=effect
        self.x=int(x)
        self.y=int(y)
        self.r=r
        self.g=g
        self.b=b
        self.font=36
        self.message=message
        self.text=None
        self.rectText=None
        self.timer=0
        self.creerText()
        
    def creerText(self):
        if self.x==-1:
            self.x=self.screen.get_width()/2
        
        if self.y==-1:
            self.y=self.screen.get_height()/2
        elif self.y==-2:
            self.y=self.screen.get_height()-50
        font = pygame.font.Font(None, self.font)
        self.text = font.render(self.message, 1, (self.r, self.g, self.b))
        self.rectText=self.text.get_rect(center=(self.x,self.y))
        
    def draw(self,newTicks):
        if self.effect==C_EFFECT_NONE:
            self.screen.blit(self.text,self.rectText)
        elif self.effect==C_EFFECT_BLINK:
            self.timer+=1
            self.timer%=20
            if self.timer<10:
                self.screen.blit(self.text,self.rectText)
        
        if newTicks<(self.ticks+self.duree):
            return 1
        else:
            return 0