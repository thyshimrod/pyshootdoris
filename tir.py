import os, sys
import pygame
from pygame.locals import *

C_TIR_TYPE_MISSILE=1
C_TIR_TYPE_SIDESHOOT_L=2
C_TIR_TYPE_SIDESHOOT_R=3
C_TIR_TYPE_REARSHOOT=4
C_TIR_TYPE_DIAGOSHOOT_L=5
C_TIR_TYPE_DIAGOSHOOT_R=6
C_TIR_MONSTRE_VERTICAL1=20
C_TIR_MONSTRE_DIAGO_L=21
C_TIR_MONSTRE_DIAGO_R=22

class Tir:
    def __init__(self,mySurface,screen,x,y,tir=C_TIR_TYPE_MISSILE):
        self.screen=screen
        self.surface=mySurface
        self.sprite=[]
        self.x=x
        self.y=y
        self.typeTir=tir
        self.speed=[0,0]
        self.myrect=None
        self.pair=0
        self.nbetat=0
        self.chargeSprite()
        self.ticks=0
        
    def chargeSprite(self):
        if self.typeTir==C_TIR_TYPE_MISSILE:
            self.sprite.append(self.surface.subsurface(pygame.Rect(1,156,14,20)))
            self.sprite.append(self.surface.subsurface(pygame.Rect(15,156,14,20)))
            self.myrect=Rect(self.x,self.y,20,14)
            self.speed=[0,-2]
            self.nbetat=2
        elif self.typeTir==C_TIR_TYPE_DIAGOSHOOT_L:
            self.sprite.append(pygame.transform.rotate(self.surface.subsurface(pygame.Rect(1,156,14,20)),45))
            self.sprite.append(pygame.transform.rotate(self.surface.subsurface(pygame.Rect(15,156,14,20)),45))
            self.myrect=Rect(self.x,self.y,20,14)
            self.speed=[-2,-2]
            self.nbetat=2
        elif self.typeTir==C_TIR_TYPE_DIAGOSHOOT_R:
            self.sprite.append(pygame.transform.rotate(self.surface.subsurface(pygame.Rect(1,156,14,20)),-45))
            self.sprite.append(pygame.transform.rotate(self.surface.subsurface(pygame.Rect(15,156,14,20)),-45))
            self.myrect=Rect(self.x,self.y,20,14)
            self.speed=[2,-2]
            self.nbetat=2
        elif self.typeTir==C_TIR_TYPE_SIDESHOOT_L:
            self.sprite.append(self.surface.subsurface(pygame.Rect(64,160,14,14)))
            self.sprite.append(self.surface.subsurface(pygame.Rect(78,160,14,14)))
            self.myrect=Rect(self.x,self.y,14,14)
            self.speed=[2,0]
            self.nbetat=2
        elif self.typeTir==C_TIR_TYPE_SIDESHOOT_R:
            self.sprite.append(self.surface.subsurface(pygame.Rect(64,160,14,14)))
            self.sprite.append(self.surface.subsurface(pygame.Rect(78,160,14,14)))
            self.myrect=Rect(self.x,self.y,14,14)
            self.speed=[-2,0]
            self.nbetat=2
        elif self.typeTir==C_TIR_TYPE_REARSHOOT:
            self.sprite.append(self.surface.subsurface(pygame.Rect(64,160,14,14)))
            self.sprite.append(self.surface.subsurface(pygame.Rect(78,160,14,14)))
            self.myrect=Rect(self.x,self.y,20,14)
            self.speed=[0,2]
            self.nbetat=2
        elif self.typeTir==C_TIR_MONSTRE_VERTICAL1:
            self.sprite.append(self.surface.subsurface(pygame.Rect(31,159,16,15)))
            self.sprite.append(self.surface.subsurface(pygame.Rect(47,159,16,15)))
            self.myrect=Rect(self.x,self.y,16,15)
            self.speed=[0,2]
            self.nbetat=2
        elif self.typeTir==C_TIR_MONSTRE_DIAGO_L:
            self.sprite.append(self.surface.subsurface(pygame.Rect(31,159,16,15)))
            self.sprite.append(self.surface.subsurface(pygame.Rect(47,159,16,15)))
            self.myrect=Rect(self.x,self.y,16,15)
            self.speed=[2,-2]
            self.nbetat=2
        elif self.typeTir==C_TIR_MONSTRE_DIAGO_R:
            self.sprite.append(self.surface.subsurface(pygame.Rect(31,159,16,15)))
            self.sprite.append(self.surface.subsurface(pygame.Rect(47,159,16,15)))
            self.myrect=Rect(self.x,self.y,16,15)
            self.speed=[2,2]
            self.nbetat=2
        
    def move(self):
        self.myrect=self.myrect.move(self.speed)
        if (self.myrect.top-1)<0:
            return 0
        if (self.myrect.bottom+1)>self.screen.get_height():
            return 0
        if (self.myrect.left-1)<0:
            return 0
        if (self.myrect.right+1)>self.screen.get_width():
            return 0
        return 1
            
    def draw(self):
        self.ticks+=1
        self.ticks%=10
        if self.ticks==0:
            self.pair+=1
            self.pair%=self.nbetat
        
        self.screen.blit(self.sprite[self.pair],self.myrect)
