'''
Created on 11/12/2013

@author: periclesmiranda
'''
import copy
from topologias import Topologia

class Local(Topologia):

    def __init__(self):
        pass
            
    #Seleciona a melhor solucao entre os vizinhos.
    def getG(self, passaro_indice=None, bando=None):
        
        vizinhos = []
        
        if passaro_indice == 0:
            vizinhos.append(bando[-1])
            vizinhos.append(bando[passaro_indice+1])
        elif passaro_indice == (len(bando)-1):
            vizinhos.append(bando[-2])
            vizinhos.append(bando[0])
        else:
            vizinhos.append(bando[passaro_indice-1])
            vizinhos.append(bando[passaro_indice+1])
        
        #Prestar atenção...pois ordena em ordem crescente!!! Válido apenas para problemas de minimização!!
        bando_ordenado = sorted(vizinhos, key = lambda p: p.p_fitness);
        melhor_passaro = bando_ordenado[0];
        
        g = copy.deepcopy(melhor_passaro);
        return g;
        