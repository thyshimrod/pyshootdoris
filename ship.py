import os, sys
import pygame
from pygame.locals import *
from tir import *
from doris import *

C_TIR_UNTIR=1
C_TIR_DEUXTIR=2
C_TIR_TROISTIR=3
C_TIR_SIDESHOOT=10
C_TIR_SIDESHOOT2=11
C_TIR_REARSHOOT=20
C_TIR_REARSHOOT2=21

class SpaceShip:
    def __init__(self,mySurface,screen,x,y):
        self.screen=screen
        self.mySurface=mySurface
        self.myRect=Rect(x,y,22,25)
        self.sprite=[]        
        self.typeVaisseau=1
        self.nbEtat=2
        self.etat=0
        self.speedTir=500
        self.armes=[]
        self.armes.append(C_TIR_UNTIR)
        self.tirs=[]
        self.speed=2
        self.destroy=0
        self.last_tir=pygame.time.get_ticks()
        self.score=0
        self.ticks=0
        self.chargeSprite()
        self.collision=0
        self.blinking=200
        self.isblink=0
        self.vie=2
        self.shield=0
        self.modules=[]
        #~ self.modules.append(Rect(0,0,0,0))
        #~ self.modules.append(Rect(0,0,0,0))
        #~ self.modules.append(Rect(0,0,0,0))
        #~ self.modules.append(Rect(0,0,0,0))
        
        
    def move(self):
        keypressed=pygame.key.get_pressed()
        if keypressed[pygame.K_UP]:
            if (self.myRect.top-self.speed)>0:
                self.myRect=self.myRect.move(0,-self.speed)
        if keypressed[pygame.K_DOWN]:
            if (self.myRect.bottom+self.speed)<self.screen.get_height():
                self.myRect=self.myRect.move(0,self.speed)
        if keypressed[pygame.K_LEFT]:
            if (self.myRect.left-self.speed)>0:
                self.myRect=self.myRect.move(-self.speed,0)
        if keypressed[pygame.K_RIGHT]:
            if (self.myRect.right+self.speed)<self.screen.get_width():
                self.myRect=self.myRect.move(self.speed,0)
        if keypressed[pygame.K_SPACE]:
                self.tir()
        if keypressed[pygame.K_COMMA]:
                self.triche()
                
        for myTir in self.tirs:
            if not myTir.move():
                self.tirs.remove(myTir)
    

    
    def tir(self):
        if (pygame.time.get_ticks()-self.last_tir)>self.speedTir:
            for arme in self.armes:
                if arme==C_TIR_UNTIR:
                    self.tirs.append(Tir(self.mySurface,self.screen,self.myRect.left+((self.myRect.right-self.myRect.left)/2)-4,self.myRect.top-10))
                if arme==C_TIR_DEUXTIR:
                    self.tirs.append(Tir(self.mySurface,self.screen,self.myRect.left-5,self.myRect.top+7))
                    self.tirs.append(Tir(self.mySurface,self.screen,self.myRect.right-5,self.myRect.top+7))
                if arme==C_TIR_TROISTIR:
                    self.tirs.append(Tir(self.mySurface,self.screen,self.myRect.left+((self.myRect.right-self.myRect.left)/2)-4,self.myRect.top-10))
                    self.tirs.append(Tir(self.mySurface,self.screen,self.myRect.left-5,self.myRect.top+7))
                    self.tirs.append(Tir(self.mySurface,self.screen,self.myRect.right-5,self.myRect.top+7))
                if arme==C_TIR_SIDESHOOT:
                    self.tirs.append(Tir(self.mySurface,self.screen,self.myRect.right-7,self.myRect.bottom-20,C_TIR_TYPE_SIDESHOOT_L))
                    self.tirs.append(Tir(self.mySurface,self.screen,self.myRect.left-7,self.myRect.bottom-20,C_TIR_TYPE_SIDESHOOT_R))
                if arme==C_TIR_SIDESHOOT2:
                    self.tirs.append(Tir(self.mySurface,self.screen,self.myRect.right-7,self.myRect.top+30,C_TIR_TYPE_SIDESHOOT_L))
                    self.tirs.append(Tir(self.mySurface,self.screen,self.myRect.left-7,self.myRect.top+30,C_TIR_TYPE_SIDESHOOT_R))
                if arme==C_TIR_REARSHOOT:
                    if self.armes.count(C_TIR_REARSHOOT2)==0:
                        self.tirs.append(Tir(self.mySurface,self.screen,self.myRect.left+5,self.myRect.bottom-20,C_TIR_TYPE_REARSHOOT))
                    else:
                        self.tirs.append(Tir(self.mySurface,self.screen,self.myRect.left-5,self.myRect.bottom-20,C_TIR_TYPE_REARSHOOT))
                if arme==C_TIR_REARSHOOT2:
                    self.tirs.append(Tir(self.mySurface,self.screen,self.myRect.right-5,self.myRect.bottom-20,C_TIR_TYPE_REARSHOOT))
            for module in self.modules:
                if module.right>self.myRect.right:
                    self.tirs.append(Tir(self.mySurface,self.screen,module.right-(module.right-module.left)/2,module.top-(module.bottom-module.top)/2,C_TIR_TYPE_DIAGOSHOOT_R))
                else:
                    self.tirs.append(Tir(self.mySurface,self.screen,module.right-(module.right-module.left)/2,module.top-(module.bottom-module.top)/2,C_TIR_TYPE_DIAGOSHOOT_L))
            self.last_tir=pygame.time.get_ticks()
        
        
    def draw(self):
        if self.blinking>0:
            self.blinking-=1
            if self.blinking==0:
                self.collision=1
                self.isblink=0
            else:
                if self.blinking%10==0:
                    self.isblink+=1
                    self.isblink%=2
                    
        self.ticks+=1
        self.ticks%=10
        if self.ticks==0:
            self.etat+=1
            self.etat%=self.nbEtat
        if self.isblink==0:
            self.screen.blit(self.sprite[self.etat],self.myRect)
            for i in range(len(self.modules)):
                img=pygame.transform.rotozoom(self.sprite[self.etat],1,0.7)
                if i%2==0:
                    j=i/2
                    j+=1
                    x=self.myRect.left-img.get_width()*j-img.get_width()/2*j
                    y=self.myRect.bottom-img.get_height()
                if i%2==1:
                    j=i-1
                    j=j/2
                    j+=1
                    x=self.myRect.right+img.get_width()/2*j+img.get_width()*(j-1)
                    y=self.myRect.bottom-img.get_height()
                rect=Rect(x,y,img.get_width(),img.get_height())
                self.screen.blit(img,rect)
                self.modules[i]=rect
                
        if self.shield>0:
            pygame.draw.circle(self.screen,(255/self.shield,0,255-255/self.shield),(self.myRect.left+self.sprite[self.etat].get_width()/2,self.myRect.top+self.sprite[self.etat].get_height()/2),self.sprite[self.etat].get_width()+5,10-(10/self.shield)+2)
        
        for myTir in self.tirs:
            myTir.draw()
            
    def touche(self):
        if self.shield>0:
            self.shield-=1
            self.blinking=200
            self.collision=0
        else:
            self.vie-=1
            if self.vie<=0:
                self.destroy=1
            else:
                self.blinking=200
                self.collision=0
            for i in range(len(self.armes)):
                self.armes.pop()
            self.typeVaisseau=1
            self.speedTir=500
            self.chargeSprite()
            self.modules=[]
            self.armes.append(C_TIR_UNTIR)
            
    def upgrade(self,bonus):
        if bonus==C_BONUS_UPGRADE:
            self.typeVaisseau+=1
            self.speed+=1
            self.chargeSprite()
        elif bonus==C_BONUS_SPEEDUP_TIR:
            self.speedTir-=100
        elif bonus==C_BONUS_MULTI_TIR:
            index=-1
            i=0
            for arme in self.armes:
                if arme==C_TIR_UNTIR or arme==C_TIR_DEUXTIR:
                    index=i
                i+=1
            if index>-1:
                self.armes[index]+=1
        elif bonus==C_BONUS_SIDESHOOT:
            i=self.armes.count(C_TIR_SIDESHOOT)
            if i==0:
                self.armes.append(C_TIR_SIDESHOOT)
            else:
                self.armes.append(C_TIR_SIDESHOOT2)
        elif bonus==C_BONUS_REARSHOOT:
            i=self.armes.count(C_TIR_REARSHOOT)
            if i==0:
                self.armes.append(C_TIR_REARSHOOT)
            else:
                self.armes.append(C_TIR_REARSHOOT2)
        elif bonus==C_BONUS_LIFE:
            self.vie+=1
        elif bonus==C_BONUS_MODULE:
            self.modules.append(Rect(0,0,0,0))
        elif bonus==C_BONUS_SHIELD_3:
            self.shield=3
        elif bonus==C_BONUS_SHIELD_5:
            self.shield=5
            
    def triche(self):
        self.modules.append(Rect(0,0,0,0))
        self.modules.append(Rect(0,0,0,0))
        self.modules.append(Rect(0,0,0,0))
        self.modules.append(Rect(0,0,0,0))
        self.shield=5
        self.armes.append(C_TIR_REARSHOOT)
        self.armes.append(C_TIR_REARSHOOT2)
        self.armes.append(C_TIR_SIDESHOOT2)
        self.armes.append(C_TIR_SIDESHOOT)
        self.armes[0]=C_TIR_TROISTIR
            
    def chargeSprite(self):
        if self.typeVaisseau==1:
            self.sprite=[]
            self.sprite.append(self.mySurface.subsurface(pygame.Rect(1,49,22,25)))
            self.sprite.append(self.mySurface.subsurface(pygame.Rect(26,49,22,25)))
            self.myRect=Rect(self.myRect.left,self.myRect.top,22,25)
        elif self.typeVaisseau==2:
            self.sprite=[]
            self.sprite.append(self.mySurface.subsurface(pygame.Rect(79,47,35,26)))
            self.sprite.append(self.mySurface.subsurface(pygame.Rect(114,47,35,26)))
            self.myRect=Rect(self.myRect.left,self.myRect.top,35,26)
        elif self.typeVaisseau==3:
            self.sprite=[]
            self.sprite.append(self.mySurface.subsurface(pygame.Rect(184,45,51,25)))
            self.sprite.append(self.mySurface.subsurface(pygame.Rect(235,45,51,25)))
            self.myRect=Rect(self.myRect.left,self.myRect.top,51,25)
        elif self.typeVaisseau==4:
            self.sprite=[]
            self.sprite.append(self.mySurface.subsurface(pygame.Rect(348,46,32,25)))
            self.sprite.append(self.mySurface.subsurface(pygame.Rect(380,46,32,25)))
            self.myRect=Rect(self.myRect.left,self.myRect.top,32,25)
        elif self.typeVaisseau==5:
            self.sprite=[]
            self.sprite.append(self.mySurface.subsurface(pygame.Rect(457,46,32,35)))
            self.sprite.append(self.mySurface.subsurface(pygame.Rect(489,46,32,35)))
            self.myRect=Rect(self.myRect.left,self.myRect.top,32,35)
        