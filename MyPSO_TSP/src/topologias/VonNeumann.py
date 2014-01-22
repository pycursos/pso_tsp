'''
Created on 22/01/2014

@author: periclesmiranda
'''
from topologias.Topologia import Topologia
import copy

class VonNeumann(Topologia):

    #Seleciona a melhor solucao entre os vizinhos.
    #Na topologia VonNeumann adotamos 3 colunas e n linhas de particulas
    def getG(self, passaro_indice=None, bando=None):
        
        if passaro_indice != None:
            #vizinhos = [cima, baixo, esquerda, direita]
            vizinhos = []
            
            #definicao do cima
            indice_cima = passaro_indice - 3 
            if indice_cima < 0:
                indice_cima = indice_cima + len(bando)
            
            vizinhos.append(bando[indice_cima])
            
            #definicao do baixo
            indice_baixo = passaro_indice + 3
            if indice_baixo >= len(bando):
                indice_baixo = indice_baixo - len(bando)
                
            vizinhos.append(bando[indice_baixo])
            
            #definicao do esquerda
            indice_esquerda = passaro_indice - 1
            if passaro_indice % 3 == 0:
                indice_esquerda = passaro_indice + 2
                
            vizinhos.append(bando[indice_esquerda])
            
            #definicao do direita
            indice_direita = passaro_indice + 1
            if indice_direita % 3 == 0:
                indice_direita = passaro_indice - 2
                
            vizinhos.append(bando[indice_direita])
                
            #Prestar atencao...pois ordena em ordem crescente!!! Valido apenas para problemas de minimizacao!!
            bando_ordenado = sorted(vizinhos, key = lambda p: p.p_fitness);
            melhor_passaro = bando_ordenado[0];
            
            g = copy.deepcopy(melhor_passaro);
            return g;
        else:
            return None