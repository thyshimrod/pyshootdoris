import os, sys
import pygame
from pygame.locals import *
import random

C_BONUS_UPGRADE=1
C_BONUS_SPEEDUP_TIR=2
C_BONUS_MULTI_TIR=3
C_BONUS_SIDESHOOT=4
C_BONUS_REARSHOOT=5
C_BONUS_LIFE=6
C_BONUS_MODULE=7
C_BONUS_SHIELD_3=8
C_BONUS_SHIELD_5=9

class Doris:
    def __init__(self,screen,x,y,typeBonus=0):
        self.speed=[1,1]
        self.screen=screen
        self.sprite=pygame.image.load("doris.gif").convert()
        self.myrect=Rect(x,y,31,24)
        self.bonus=typeBonus
        if self.bonus==0:
            self.bonus=random.randint(1,9)
            #~ self.bonus=8
        self.tick=0
        
    def move(self):
        self.myrect=self.myrect.move(self.speed)
        if self.myrect.left<0 or self.myrect.right>self.screen.get_width():
            self.speed[0]=-self.speed[0]
        if self.myrect.top<0 or self.myrect.bottom>self.screen.get_height():
            self.speed[1]=-self.speed[1]
            
    def draw(self):
        self.screen.blit(self.sprite,self.myrect)
        self.tick+=1
        self.tick%=20
        if self.tick<10:
            font = pygame.font.Font(None, 50)                    
            text = font.render("Hurry !!! Catch the Doris", 1, (224, 60, 60))
            textpos=text.get_rect(centerx=self.screen.get_width()/2,centery=self.screen.get_height()/2)
            self.screen.blit(text,textpos)