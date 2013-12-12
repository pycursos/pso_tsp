'''
Created on 11/12/2013

@author: periclesmiranda
'''
import copy
from Topologia import Topologia

class Local(Topologia):

    def __init__(self):
        pass
            
    def getG(self, bando):
        pass
    
    def _getG(self):
        return self.g;
    
    def _setG(self, passaro):
        self.g = copy.deepcopy(passaro);
        