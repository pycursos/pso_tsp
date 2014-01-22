'''
Created on 11/12/2013

@author: periclesmiranda
'''

import copy

class Topologia(object):

    def __init__(self):
        self.bestP = None

    def _setG(self, bestP):
        self.bestP = bestP

    def getG(self, passaro=None, enxame=None):
        pass
    
    def bestOfBests(self, bando):
        bando_ordenado = sorted(bando, key = lambda p: p.p_fitness);
        melhor_passaro = bando_ordenado[0];

        g = copy.deepcopy(melhor_passaro);
        return g;
