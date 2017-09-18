       # -*- coding:cp1252 -*-
try: import psyco;psyco.full()
except:pass

import os, sys
from string import *
import pygame
from pygame.locals import *
from ship import  *
from tir import *
from creature import *
from explosion import *
from doris import *
from evenement import *
from xmlhandler import *
from chemin import *
from textEvent import *
from etoiles import *

ID_STATEGAME_MENU=1
ID_STATEGAME_JEU=2
ID_STATEGAME_GAMEOVER=3

C_VITESSE_DEFILEMENT_NORMAL=3
C_VITESSE_AVANCEMENT_TICK=1

C_CHOIX_QUITTER=3
C_CHOIX_CREDITS=2
C_CHOIX_AIDE=1
C_CHOIX_JOUER=0


black = 0, 0, 0

class PyShoot:
    def __init__(self, width=800,height=600):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Cath the Doris")
        self.mySpriteSurface=pygame.image.load("shoot.gif").convert()
        self.fond=pygame.image.load("fond4.bmp").convert()
        self.chemins=[]
        self.status=ID_STATEGAME_MENU
        self.loadChemin("chemin2.dat")
        self.monsters=[]
        self.ship=None
        self.explosions=[]
        self.events=[]
        self.vitesseTicks=C_VITESSE_AVANCEMENT_TICK
        self.ticks=0
        self.bonus=[]
        self.message=[]
        self.vitesseDefil=C_VITESSE_DEFILEMENT_NORMAL
        self.defilx=0
        self.tirsMonstre=[]
        self.world=[]
        self.actualWorld=0
        #~ self.chargeWorld()
        self.etoiles=[]
        self.boss=[]
        self.highscore=0
        self.readHighScore()
        self.internalticks=0


    def readHighScore(self):
        f=open('high','r')
        data=f.readline()
        if data:
            self.highscore=int(data)
        f.close()

    def chargeWorld(self):
        f=open('world','r')
        data=f.readline()
        while data:
            self.world.append(data.strip('\n'))
            data=f.readline()
        f.close()

    def gameOver(self):
        self.monsters=[]
        self.explosions=[]
        self.ticks=0
        self.internalticks=0
        self.bonus=[]
        self.message=[]
        self.defilx=0
        self.tirsMonstre=[]
        self.boss=[]
        if self.highscore<self.ship.score:
            f=open('high','w')
            f.write(str(self.ship.score))
            f.close()
            self.highscore=self.ship.score


    def loadChemin(self,fic):
        f=open(fic,'r')
        data=f.readline()
        while data:
            if data.strip('\n')=='A':
                self.chemins.append(monChemin())
                data=f.readline()
                self.chemins[len(self.chemins)-1].numero=len(self.chemins)
                data=f.readline()
                self.chemins[len(self.chemins)-1].genre=int(data.strip("\n"))
                data=f.readline()
                self.chemins[len(self.chemins)-1].taille=int(data.strip("\n"))
                j=0
                while j<int(self.chemins[len(self.chemins)-1].taille):
                    data=f.readline()
                    self.chemins[len(self.chemins)-1].x.append(int(data.strip("\n")))
                    data=f.readline()
                    self.chemins[len(self.chemins)-1].y.append(int(data.strip("\n")))
                    j+=1
            data=f.readline()
        f.close()

    def splash(self):
        imgSplash=pygame.image.load("shimrod3.jpg").convert()
        imgPy=pygame.image.load("pygame_logo.jpg").convert()
        notfini=1
        ticks=0
        j=0
        while notfini:
            ticks+=1
            j+=0.01
            #~ j=j%3
            if ticks>550:
                notfini=0
            self.screen.fill(black)
            if ticks<200:
                tp=pygame.transform.rotozoom(imgSplash,1,j)
                x=self.screen.get_width()/2-tp.get_width()/2
                y=self.screen.get_height()/2-tp.get_height()/2
                self.screen.blit(tp,Rect(x,y,tp.get_width(),tp.get_height()))
            if ticks==200:
                j=0
            if ticks>200 and ticks<250:
                tp=pygame.transform.rotozoom(imgPy,1,j)
                x=self.screen.get_width()/2-tp.get_width()/2
                y=self.screen.get_height()/2-tp.get_height()/2
                self.screen.blit(tp,Rect(x,y,tp.get_width(),tp.get_height()))
            if ticks>250 and ticks<400:
                x=self.screen.get_width()/2
                y=self.screen.get_height()/2
                font = pygame.font.Font(None, 40)
                text = font.render("Presente", 1, (24, 116, 205))
                rectText=text.get_rect(center=(x,y))
                self.screen.blit(text,rectText)
            if ticks>400:
                x=self.screen.get_width()/2
                y=self.screen.get_height()/2
                font = pygame.font.Font(None, 80)
                text = font.render("Catch The Doris", 1, (24, 116, 205))
                rectText=text.get_rect(center=(x,y))
                self.screen.blit(text,rectText)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    notfini=0
                elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_ESCAPE:
                        notfini=0
                    elif event.key==pygame.K_RETURN:
                        notfini=0

    def menu(self):
        menu=[]
        menu.append("Jouer")
        menu.append("Aide")
        menu.append("Credits")
        menu.append("Quitter")
        notfini=1
        monchoix=0
        while notfini:
            self.screen.fill(black)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_ESCAPE:
                        return C_CHOIX_QUITTER
                    elif event.key==pygame.K_RETURN:
                        return monchoix
                    elif event.key==pygame.K_UP:
                        monchoix-=1
                        monchoix%=len(menu)
                    elif event.key==pygame.K_DOWN:
                        monchoix+=1
                        monchoix%=len(menu)
            x=self.screen.get_width()/2
            y=self.screen.get_height()/2
            for i in range(len(menu)):
                font = pygame.font.Font(None, 40)
                if i==monchoix:
                    color=(24,235,205)
                else:
                    color=(24,116,205)
                text = font.render(menu[i], 1, color)
                textpos=text.get_rect(center=(x,y+i*45))
                self.screen.blit(text,textpos)
            pygame.display.flip()

    def aide(self):
        menu=[]
        menu.append("Les fleches : D�placements")
        menu.append("Espace : Tir")
        menu.append("Escape : Quitter")
        menu.append("")
        menu.append("Quand une Doris passe, attraper la pour obtenir un bonus")
        notfini=1
        monchoix=0
        while notfini:
            self.screen.fill(black)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_ESCAPE:
                        notfini=0
                    elif event.key==pygame.K_RETURN:
                        notfini=0
            x=self.screen.get_width()/2
            y=self.screen.get_height()/2
            for i in range(len(menu)):
                font = pygame.font.Font(None, 40)
                color=(24,116,205)
                text = font.render(menu[i], 1, color)
                textpos=text.get_rect(center=(x,y+i*45))
                self.screen.blit(text,textpos)
            pygame.display.flip()

    def credits(self):
        menu=[]
        menu.append("CREDITS")
        menu.append("")
        menu.append("Developper : Shimrod")
        menu.append("Star guest : Ln ( aka Doris)")
        notfini=1
        monchoix=0
        while notfini:
            self.screen.fill(black)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_ESCAPE:
                        notfini=0
                    elif event.key==pygame.K_RETURN:
                        notfini=0
            x=self.screen.get_width()/2
            y=self.screen.get_height()/2
            for i in range(len(menu)):
                font = pygame.font.Font(None, 40)
                color=(24,116,205)
                text = font.render(menu[i], 1, color)
                textpos=text.get_rect(center=(x,y+i*45))
                self.screen.blit(text,textpos)
            pygame.display.flip()

    def afficheText(self):
        font = pygame.font.Font(None, 20)
        #~ text = font.render("Player's score : " + str(self.ship.score) + "             ticks=" + str(self.ticks), 1, (224, 60, 60))
        #~ text = font.render("Player's score : " + str(self.ship.score) + "             ticks=" + str(self.ticks), 1, (24,116,205))
        text = font.render("Player's score : " + str(self.ship.score) , 1, (24,116,205))
        textpos=text.get_rect()

        coeur=self.mySpriteSurface.subsurface(Rect(77,315,24,24))
        for i in range(self.ship.vie):
            self.screen.blit(coeur,Rect(150+i*25,0,coeur.get_width(),coeur.get_height()))
        self.screen.blit(text,textpos)
        text = font.render("Ticks = " + str(self.ticks) , 1, (24,116,205))
        textpos=Rect(500,0,text.get_width(),text.get_height())
        self.screen.blit(text,textpos)
        text = font.render("HighScore = " + str(self.highscore) , 1, (24,116,205))
        textpos=Rect(700,0,text.get_width(),text.get_height())
        self.screen.blit(text,textpos)

    def gererEvents(self):
        if len(self.events)==0:
            self.actualWorld+=1

            if self.actualWorld>=(len(self.world)):
                self.actualWorld=0
            else:
                self.chargeEvents(self.world[self.actualWorld])
                self.internalTicks+=self.ticks
                self.ticks=0
        eventsToRemove=[]
        for event in self.events:
            if int(event.timer)==int(self.ticks):
                if event.evt=="monster":
                    if event.monsterType>=100:
                        temp=Monster(self.mySpriteSurface,self.screen,event.x,event.y,None,event.monsterType)
                        self.boss.append(temp)
                        self.monsters.append(temp)
                    else:
                        monChemin=None
                        for lechemin in self.chemins:
                            if event.mvtType==lechemin.genre:
                                monChemin=lechemin

                        for i in range(int(event.nombre)):
                            self.monsters.append(Monster(self.mySpriteSurface,self.screen,event.x+event.ecart*i,event.y,monChemin,event.monsterType))

                if event.evt=="bonus":
                    self.bonus.append(Doris(self.screen,event.x,event.y,event.monsterType))
                if event.evt=="text":
                    self.message.append(textEvent(self.screen,event.message,self.internalTicks+self.ticks,event.duree,event.effect,event.x,event.y,event.fontsize))

                eventsToRemove.append(event)
            else:
                if int(event.timer)<int(self.ticks):
                    eventsToRemove.append(event)
        for etr in eventsToRemove:
            try:
                if self.events.index(etr) !=1:
                    self.events.remove(etr)
            except:
                pass

    def gererBonus(self,bonus):
        self.ship.upgrade(bonus)
        if bonus==C_BONUS_UPGRADE:
            self.message.append(textEvent(self.screen,"UPGRADE..... SPEEEEEEED UP!!!",self.internalTicks+self.ticks,200,C_EFFECT_BLINK,self.screen.get_width()/2,self.screen.get_height()-50))
        elif bonus==C_BONUS_SPEEDUP_TIR:
            self.message.append(textEvent(self.screen,"SPEEEEEEED UP YOUR FIRE!!!",self.internalTicks+self.ticks,200,C_EFFECT_BLINK,self.screen.get_width()/2,self.screen.get_height()-50))
        elif bonus==C_BONUS_MULTI_TIR:
            self.message.append(textEvent(self.screen,"MULTI FIRE !!!!",self.internalTicks+self.ticks,200,C_EFFECT_BLINK,self.screen.get_width()/2,self.screen.get_height()-50))
        elif bonus==C_BONUS_SIDESHOOT:
            self.message.append(textEvent(self.screen,"SIDE FIRE !!!!",self.internalTicks+self.ticks,200,C_EFFECT_BLINK,self.screen.get_width()/2,self.screen.get_height()-50))
        elif bonus==C_BONUS_REARSHOOT:
            self.message.append(textEvent(self.screen,"REAR FIRE !!!!",self.internalTicks+self.ticks,200,C_EFFECT_BLINK,self.screen.get_width()/2,self.screen.get_height()-50))
        elif bonus==C_BONUS_LIFE:
            self.message.append(textEvent(self.screen,"1 UP !!!!",self.internalTicks+self.ticks,200,C_EFFECT_BLINK,self.screen.get_width()/2,self.screen.get_height()-50))
        elif bonus==C_BONUS_MODULE:
            self.message.append(textEvent(self.screen,"Module!!!! Provides You Some Help",self.internalTicks+self.ticks,200,C_EFFECT_BLINK,self.screen.get_width()/2,self.screen.get_height()-50))
        elif bonus==C_BONUS_SHIELD_3:
            self.message.append(textEvent(self.screen,"Shield UP!!!! Protects You 3 times",self.internalTicks+self.ticks,200,C_EFFECT_BLINK,self.screen.get_width()/2,self.screen.get_height()-50))
        elif bonus==C_BONUS_SHIELD_5:
            self.message.append(textEvent(self.screen,"Shield UP!!!! Protects You 5 times",self.internalTicks+self.ticks,200,C_EFFECT_BLINK,self.screen.get_width()/2,self.screen.get_height()-50))

    def defileFond(self,viDefil):
        #code permettant le defilement d'une image
        #~ self.defilx+=viDefil
        #~ self.defilx%=self.fond.get_height()
        #~ self.screen.blit(self.fond,Rect(0,self.defilx,self.fond.get_width(),self.fond.get_width()))
        #~ self.screen.blit(self.fond,Rect(0,-(self.fond.get_height()-self.defilx),self.fond.get_width(),self.fond.get_width()))
        if viDefil>0:
            tempo=random.randint(1,50)
            if tempo>10:
                color=random.randint(1,4)
                position=random.randint(0,800)
                self.etoiles.append(Etoile(self.screen,position,0,color))
            etoileToRemove=[]
            for etoile in self.etoiles:
                    etoile.move()
                    etoile.draw()
                    if etoile.myrect.bottom>self.screen.get_height():
                        etoileToRemove.append(etoile)

            for etoile in etoileToRemove:
                self.etoiles.remove(etoile)
        else:
            for etoile in self.etoiles:
                etoile.draw()

    def chargeEvents(self,file):
        outFile = sys.stdout
        handler = MySaxDocumentHandler(outFile)
        parser = make_parser()
        parser.setContentHandler(handler)
        inFile = open(file, 'r')
        parser.parse(inFile)
        inFile.close()
        MainWindow.events=handler.getEvents()

    def jeu(self):
        self.status=ID_STATEGAME_JEU
        self.ship=SpaceShip(self.mySpriteSurface,self.screen, 350,350)
        self.ticks=0
        self.internalTicks=0
        self.actualWorld=0
        self.chargeWorld()
        self.chargeEvents(self.world[self.actualWorld])
        while 1:
            if self.status==ID_STATEGAME_GAMEOVER:
                self.screen.fill(black)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    elif event.type==pygame.KEYDOWN:
                        if event.key==pygame.K_ESCAPE:
                            sys.exit()
                        elif event.key==pygame.K_RETURN:
                            return 1

                if self.status==ID_STATEGAME_GAMEOVER:
                    font = pygame.font.Font(None, 50)
                    text = font.render("Game Over", 1, (24,116,205))
                    textpos=text.get_rect(centerx=self.screen.get_width()/2,centery=self.screen.get_height()/2-40)
                    self.screen.blit(text,textpos)

                font = pygame.font.Font(None, 36)
                text = font.render("Presser Entr�e pour continuer", 1, (24,116,205))
                textpos=text.get_rect(centerx=self.screen.get_width()/2,centery=self.screen.get_height()/2)
                self.screen.blit(text,textpos)
                pygame.display.flip()
            elif self.status==ID_STATEGAME_JEU:
                if len(self.boss)==0:
                    self.ticks+=self.vitesseTicks
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    elif event.type==pygame.KEYDOWN:
                        if event.key==pygame.K_ESCAPE:
                            sys.exit()

                self.screen.fill(black)
                if len(self.boss)==0:
                    self.defileFond(self.vitesseDefil)
                else:
                    self.defileFond(0)
                self.gererEvents()
                monsterToRemove=[]

                bonusToRemove=[]
                for bonus in self.bonus:
                    bonus.move()
                    bonus.draw()
                    if bonus.myrect.colliderect(self.ship.myRect):
                        bonusToRemove.append(bonus)
                        self.gererBonus(bonus.bonus)

                for bonus in bonusToRemove:
                    self.bonus.remove(bonus)
                bossToRemove=[]
                for monster in self.monsters:
                    if monster.typeMonster>0:
                        self.tirsMonstre.extend(monster.move())
                        monster.draw()
                        if monster.collision==1:
                            if self.ship.collision==1:
                                if monster.myrect.colliderect(self.ship.myRect):
                                    self.ship.touche()
                                    self.explosions.append(Explosion(self.mySpriteSurface,self.screen,self.ship.myRect.left,self.ship.myRect.top))
                            tirToRemove=[]
                            for tir in self.ship.tirs:
                                if monster.myrect.colliderect(tir.myrect):
                                    monster.pdv-=1
                                    self.explosions.append(Explosion(self.mySpriteSurface,self.screen,tir.myrect.left,tir.myrect.top))
                                    tirToRemove.append(tir)
                                    if monster.pdv<1:
                                        self.ship.score+=monster.points
                                        monsterToRemove.append(monster)
                                        if monster.typeMonster>=100:
                                            bossToRemove.append(monster)
                            for tir in tirToRemove:
                                self.ship.tirs.remove(tir)

                        if monster.myrect.left<-100 or monster.myrect.right>self.screen.get_width()+100 or monster.myrect.top<-100 or monster.myrect.bottom>self.screen.get_height()+100:
                            monsterToRemove.append(monster)
                    else:
                        monsterToRemove.append(monster)

                for mtr in monsterToRemove:
                    try:
                        index=self.monsters.index(mtr)
                        self.monsters.remove(mtr)
                    except:
                        pass

                for boss in bossToRemove:
                    try:
                        index=self.boss.index(boss)
                        self.boss.remove(boss)
                    except:
                        pass

                for myTir in self.tirsMonstre:
                    if not myTir.move():
                        self.tirsMonstre.remove(myTir)
                    else:
                        myTir.draw()
                        if self.ship.collision==1:
                            if self.ship.myRect.colliderect(myTir.myrect):
                                self.ship.touche()
                                self.explosions.append(Explosion(self.mySpriteSurface,self.screen,self.ship.myRect.left,self.ship.myRect.top))
                                self.tirsMonstre.remove(myTir)


                for explosion in self.explosions:
                    if explosion.move():
                        explosion.draw()
                    else:
                        self.explosions.remove(explosion)

                messageToRemove=[]
                for message in self.message:
                    if (message.draw(self.internalTicks+self.ticks)==0):
                        messageToRemove.append(message)

                for mtr in messageToRemove:
                    self.message.remove(mtr)

                if self.ship.destroy!=1:
                    self.ship.move()
                    self.ship.draw()
                else:
                    self.status=ID_STATEGAME_GAMEOVER
                    self.gameOver()
                self.afficheText()
                pygame.display.flip()

    def MainLoop(self):
        self.splash()
        while 1:
            lechoix=self.menu()
            if lechoix==C_CHOIX_QUITTER:
                sys.exit()
            elif lechoix==C_CHOIX_AIDE:
                self.aide()
            elif lechoix==C_CHOIX_JOUER:
                self.jeu()
            elif lechoix==C_CHOIX_CREDITS:
                self.credits()



if __name__ == "__main__":
    MainWindow = PyShoot()

    #~ import profile
    #~ profile.run('MainWindow.MainLoop()')
    MainWindow.MainLoop()


#~ TODO LIST
#~ mettre des boss
