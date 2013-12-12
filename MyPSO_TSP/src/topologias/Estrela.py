'''
Created on 18/08/2012

@author: periclesmiranda
'''
import copy
from Topologia import Topologia

class Estrela(Topologia):

    def __init__(self):
        pass

    #Seleciona a melhor solucao do enxame.
    def getG(self, bando):
        bando_ordenado = sorted(bando, key = lambda passaro: passaro.fitness);
        melhor_passaro = bando_ordenado[0];
        
        self.g = copy.deepcopy(melhor_passaro);
        return self.g;
    
    def _getG(self):
        return self.g;
    
    def _setG(self, passaro):
        self.g = copy.deepcopy(passaro);
            

        