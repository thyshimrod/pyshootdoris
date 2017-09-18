import os, sys
import pygame
from pygame.locals import *
from tir import *
import random

C_TIR_MISSILE_MONSTRE_1=1
C_TIR_MISSILE_MONSTRE_2=2
C_TIR_MISSILE_MONSTRE_3=3
C_TIR_MONSTRE_DIAGO_L=21
C_TIR_MONSTRE_DIAGO_R=22

class Monster:
    def __init__(self,mySurface,screen,x,y,chemin=None,typeMonster=1):
        self.screen=screen
        self.mySurface=mySurface
        self.sprite=[]
        self.speed=[0,0]
        self.point=0
        self.etat=0
        self.ticks=0
        self.nbEtat=0
        self.typeMonster=typeMonster
        self.pdv=0
        self.myrect=None
        self.chemin=chemin
        self.mvt=0
        self.armes=[]
        self.speedTir=400
        self.last_tir=pygame.time.get_ticks()-random.randint(0,200)
        self.collision=0
        self.chargeMonster(mySurface,x,y)
        
    
    def move(self):
        tirs=[]
        if self.typeMonster>0:
            if self.chemin:
                self.myrect=self.myrect.move(self.chemin.getXY(self.mvt))
                self.mvt+=1
                if self.mvt>self.chemin.taille:
                    self.mvt=0
            else:
                if self.typeMonster<100:
                    self.myrect=self.myrect.move(self.speed)
                else:
                    self.myrect=self.myrect.move(self.speed)
                    if self.myrect.left<0 or self.myrect.right>self.screen.get_width():
                        self.speed[0]=-self.speed[0]
                    if self.myrect.top<0 or self.myrect.bottom>self.screen.get_height():
                        self.speed[1]=-self.speed[1]
            
            for arme in self.armes:
                if arme==C_TIR_MISSILE_MONSTRE_1:
                    if (pygame.time.get_ticks()-self.last_tir)>self.speedTir:
                        if self.myrect.left>0 and self.myrect.right<self.screen.get_width() and self.myrect.top>0 and self.myrect.bottom<self.screen.get_height():
                            tirs.append(Tir(self.mySurface,self.screen,self.myrect.left+5,self.myrect.bottom-20,C_TIR_MONSTRE_VERTICAL1))
                            self.last_tir=pygame.time.get_ticks()
                if arme==C_TIR_MISSILE_MONSTRE_2:
                    if (pygame.time.get_ticks()-self.last_tir)>self.speedTir:
                        if self.myrect.left>0 and self.myrect.right<self.screen.get_width() and self.myrect.top>0 and self.myrect.bottom<self.screen.get_height():
                            tirs.append(Tir(self.mySurface,self.screen,self.myrect.left,self.myrect.bottom-20,C_TIR_MONSTRE_VERTICAL1))
                            tirs.append(Tir(self.mySurface,self.screen,self.myrect.right,self.myrect.bottom-20,C_TIR_MONSTRE_VERTICAL1))
                            self.last_tir=pygame.time.get_ticks()
                if arme==C_TIR_MONSTRE_DIAGO_L:
                  
                  pass
        return tirs
                
    def draw(self):
        if self.typeMonster>0:
            self.ticks+=1
            self.ticks%=10
            if self.ticks==0:
                self.etat+=1
                self.etat%=self.nbEtat
            self.screen.blit(self.sprite[self.etat],self.myrect)
        

    def chargeMonster(self,mySurface,x,y):
        if self.typeMonster==1:
            self.sprite.append(mySurface.subsurface(pygame.Rect(326,20,31,24)))
            self.sprite.append(mySurface.subsurface(pygame.Rect(357,20,31,24)))
            self.myrect=Rect(x,y,31,24)
            self.speed=[1,1]
            self.points=10
            self.nbEtat=2
            self.pdv=1
            self.collision=1
        elif self.typeMonster==2:
            self.sprite.append(mySurface.subsurface(pygame.Rect(0,20,35,24)))
            self.sprite.append(mySurface.subsurface(pygame.Rect(35,20,35,24)))
            self.myrect=Rect(x,y,35,24)
            self.speed=[1,1]
            self.points=10
            self.nbEtat=2
            self.pdv=1
            self.armes.append(C_TIR_MISSILE_MONSTRE_1)
            self.speedTir=1000
            self.collision=1
        elif self.typeMonster==3:
            self.sprite.append(mySurface.subsurface(pygame.Rect(72,20,28,24)))
            self.sprite.append(mySurface.subsurface(pygame.Rect(100,20,28,24)))
            self.myrect=Rect(x,y,28,24)
            self.speed=[1,1]
            self.points=10
            self.nbEtat=2
            self.pdv=1
            self.armes.append(C_TIR_MONSTRE_DIAGO_L)
            self.armes.append(C_TIR_MONSTRE_DIAGO_R)
            self.armes.append(C_TIR_MISSILE_MONSTRE_1)
            self.speedTir=1000
            self.collision=1
        elif self.typeMonster==4:
            self.sprite.append(mySurface.subsurface(pygame.Rect(140,20,30,24)))
            self.sprite.append(mySurface.subsurface(pygame.Rect(170,20,30,24)))
            self.myrect=Rect(x,y,30,24)
            self.speed=[1,1]
            self.points=10
            self.nbEtat=2
            self.pdv=1
            self.collision=1
        elif self.typeMonster==5:
            self.sprite.append(mySurface.subsurface(pygame.Rect(209,20,27,24)))
            self.sprite.append(mySurface.subsurface(pygame.Rect(236,20,27,24)))
            self.myrect=Rect(x,y,27,24)
            self.speed=[1,1]
            self.points=10
            self.nbEtat=2
            self.pdv=1
            self.collision=1
        elif self.typeMonster==6:
            self.sprite.append(mySurface.subsurface(pygame.Rect(270,20,26,24)))
            self.sprite.append(mySurface.subsurface(pygame.Rect(296,20,26,24)))
            self.myrect=Rect(x,y,26,24)
            self.speed=[1,1]
            self.points=10
            self.nbEtat=2
            self.pdv=1
            self.collision=1
        elif self.typeMonster==50:
            #type nuage:
            self.sprite.append(mySurface.subsurface(pygame.Rect(0,267,90,40)))
            self.myrect=Rect(x,y,90,40)
            self.speed=[0,5]
            self.points=0
            self.nbEtat=1
            self.pdv=0
            self.collision=0
        elif self.typeMonster==51:
            #type meteore1:
            self.sprite.append(mySurface.subsurface(pygame.Rect(0,211,33,35)))
            self.sprite.append(mySurface.subsurface(pygame.Rect(33,211,33,35)))
            self.sprite.append(mySurface.subsurface(pygame.Rect(66,211,33,35)))
            self.myrect=Rect(x,y,33,35)
            self.speed=[0,3]
            self.points=0
            self.nbEtat=3
            self.pdv=5
            self.collision=1
        elif self.typeMonster==52:
            #type meteore2:
            self.sprite.append(mySurface.subsurface(pygame.Rect(105,209,51,57)))
            self.myrect=Rect(x,y,51,57)
            self.speed=[0,4]
            self.points=0
            self.nbEtat=1
            self.pdv=5
            self.collision=1
        elif self.typeMonster==53:
            #type meteore3:
            self.sprite.append(mySurface.subsurface(pygame.Rect(156,210,30,56)))
            self.myrect=Rect(x,y,30,56)
            self.speed=[0,3]
            self.points=0
            self.nbEtat=1
            self.pdv=5
            self.collision=1
        elif self.typeMonster==54:
            #type meteore4:
            self.sprite.append(mySurface.subsurface(pygame.Rect(348,218,31,36)))
            self.myrect=Rect(x,y,31,36)
            self.speed=[0,3]
            self.points=0
            self.nbEtat=1
            self.pdv=5
            self.collision=1
        elif self.typeMonster==55:
            #type meteore5:
            self.sprite.append(mySurface.subsurface(pygame.Rect(400,217,29,36)))
            self.myrect=Rect(x,y,29,36)
            self.speed=[0,3]
            self.points=0
            self.nbEtat=1
            self.pdv=5
            self.collision=1    
        elif self.typeMonster==100:
            #type Boss1:
            self.sprite.append(mySurface.subsurface(pygame.Rect(0,346,107,75)))
            self.sprite.append(mySurface.subsurface(pygame.Rect(107,346,107,75)))
            self.myrect=Rect(x,y,107,75)
            self.speed=[2,3]
            self.points=200
            self.nbEtat=2
            self.pdv=20
            self.collision=1    
        elif self.typeMonster==101:
            #type Boss2:
            self.sprite.append(mySurface.subsurface(pygame.Rect(222,343,135,84)))
            self.sprite.append(mySurface.subsurface(pygame.Rect(357,343,135,84)))
            self.myrect=Rect(x,y,135,84)
            self.speed=[0,3]
            self.points=0
            self.nbEtat=2
            self.pdv=5
            self.collision=1    
        else:
            self.typeMonster=int(-1)