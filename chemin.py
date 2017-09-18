import sys, string

class monChemin:
    def __init__(self):
        self.numero=0
        self.genre=0
        self.taille=0
        self.x=[]
        self.y=[]
    
    def getXY(self,timer):
        if timer<self.taille:
            return ([self.x[timer],self.y[timer]])
        else:
            return([0,0])