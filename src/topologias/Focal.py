'''
Created on 11/12/2013

@author: periclesmiranda
'''
import copy
from topologias.Topologia import Topologia
import random
from Constants import Constants

class Focal(Topologia):

    def __init__(self):
        self.particula_focal_indice = random.randint(0, Constants.TAM_BANDO-1)
    
    #Seleciona a melhor solucao do enxame.
    def getG(self, passaro_indice=None, bando=None):
        
        melhor_passaro = None
        
        if passaro_indice != None:
            if passaro_indice == self.particula_focal_indice:
                #Prestar atencao...pois ordena em ordem crescente!!! Valido apenas para problemas de minimizacao!!
                bando_ordenado = sorted(bando, key = lambda p: p.p_fitness);
                melhor_passaro = bando_ordenado[0];
                
            else:
                if bando[passaro_indice].p_fitness < bando[self.particula_focal_indice].p_fitness:
                    melhor_passaro = bando[passaro_indice]
                else:
                    melhor_passaro = bando[self.particula_focal_indice]
            
            g = copy.deepcopy(melhor_passaro);
            return g;
        else:
            return None
        