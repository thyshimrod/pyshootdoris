import sys, string
from xml.sax import handler, make_parser
from evenement import *
    

class MySaxDocumentHandler(handler.ContentHandler):             
    def __init__(self, outfile):                                
        self.outfile = outfile
        self.element=""
        self.mesEvents=[]
        self.nbEvent=-1
    def startDocument(self):                                    
        pass
    def endDocument(self):                                      
        pass
    def startElement(self, name, attrs):
        self.element=name
        if self.element=="event":
            self.nbEvent+=1
            self.mesEvents.append(monEvent())
    def characters(self,chrs):
        if self.element=="evt":
            self.mesEvents[self.nbEvent].evt=chrs
        if self.element=="message":
            self.mesEvents[self.nbEvent].message=chrs
        if self.element=="duree":
            self.mesEvents[self.nbEvent].duree=int(chrs)
        if self.element=="effect":
            self.mesEvents[self.nbEvent].effect=int(chrs)
        if self.element=="fontsize":
            self.mesEvents[self.nbEvent].fontsize=int(chrs)
        if self.element=="timer":
            self.mesEvents[self.nbEvent].timer=int(chrs)
        if self.element=="x":
            self.mesEvents[self.nbEvent].x=int(chrs)
        if self.element=="y":
            self.mesEvents[self.nbEvent].y=int(chrs)
        if self.element=="monstertype":
            self.mesEvents[self.nbEvent].monsterType=int(chrs)
        if self.element=="typemvt":
            self.mesEvents[self.nbEvent].mvtType=int(chrs)
        if self.element=="ecart":
            self.mesEvents[self.nbEvent].ecart=int(chrs)
        if self.element=="nombre":
            self.mesEvents[self.nbEvent].nombre=int(chrs)
    def endElement(self, name):                                 
        self.element=""
    def getEvents(self):
        return self.mesEvents