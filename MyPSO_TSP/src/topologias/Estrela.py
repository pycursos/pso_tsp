'''
Created on 18/08/2012

@author: periclesmiranda
'''
import copy
from topologias import Topologia

class Estrela(Topologia):

    def __init__(self):
        pass

    #Seleciona a melhor solucao do enxame.
    def getG(self, passaro_indice=None, bando=None):
        
        #Prestar aten��o...pois ordena em ordem crescente!!! V�lido apenas para problemas de minimiza��o!!
        bando_ordenado = sorted(bando, key = lambda p: p.p_fitness);
        melhor_passaro = bando_ordenado[0];
        
        g = copy.deepcopy(melhor_passaro);
        return g;
            

        