'''
Created on 11/12/2013

@author: periclesmiranda
'''
import copy
from topologias.Topologia import Topologia

class Local(Topologia):

    #Seleciona a melhor solucao entre os vizinhos.
    def getG(self, passaro_indice=None, bando=None):
        
        if passaro_indice != None:
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
            
            #Prestar atencao...pois ordena em ordem crescente!!! Valido apenas para problemas de minimizacao!!
            bando_ordenado = sorted(vizinhos, key = lambda p: p.p_fitness);
            melhor_passaro = bando_ordenado[0];
            
            g = copy.deepcopy(melhor_passaro);
            return g;
        else:
            return None
        