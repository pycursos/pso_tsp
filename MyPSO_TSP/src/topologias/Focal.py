'''
Created on 11/12/2013

@author: periclesmiranda
'''
import copy
from Topologia import Topologia

class Focal(Topologia):

    def __init__(self):
        pass
    
    #Seleciona posicao fixa do bando.
    def getG(self, bando):
        return bando[0]
    
    def _getG(self):
        return self.g;
    
    def _setG(self, passaro):
        self.g = copy.deepcopy(passaro);
        