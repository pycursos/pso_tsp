'''
Created on 22/01/2014

@author: periclesmiranda
'''
from Input import Input
from TSP import Leitor, Cidade
import PSO
from Constants import TSPConstants, TSPClanConstants
from PSO import TSP_PSO, TSP_PSO_Clan
from topologias.Estrela import Estrela
from topologias.Local import Local
from topologias.Focal import Focal
from topologias.VonNeumann import VonNeumann
from topologias.Clan import Clan
from Relatorio import Relatorio

class Simulador(object):

    def executar(self, nome_topologia, nome_problema, numero_iteracoes, numero_particulas):
        TSPConstants.NUMERO_ITERACOES = numero_iteracoes
        TSPConstants.TAM_BANDO = numero_particulas
        
        if nome_problema in Input.problemas.keys():
            
            problema = Input.problemas[nome_problema]
            PSO.cria_mapa(problema[0], problema[1])
            
        else:
            print 'Nome do problema invalido. Veja nomes disponiveis no pacote "input/Dados."'
    
        
        TSPConstants.N_DIMENSION = len(PSO.mapa)
        algoritmo = None
        
        if nome_topologia == 'ESTRELA':
            algoritmo = TSP_PSO(PSO.mapa, Estrela)
        elif nome_topologia == 'LOCAL':
            algoritmo = TSP_PSO(PSO.mapa, Local)
        elif nome_topologia == 'FOCAL':
            algoritmo = TSP_PSO(PSO.mapa, Focal)
        elif nome_topologia == 'VONNEUMANN':
            algoritmo = TSP_PSO(PSO.mapa, VonNeumann)
        elif nome_topologia == 'CLAN':
            TSPClanConstants.N_DIMENSION = len(PSO.mapa)
            algoritmo = TSP_PSO_Clan(PSO.mapa, Clan)
        else:
            print 'Nao existe topologia com este nome.'
            
        if algoritmo != None:
            algoritmo.simular()
            
        if nome_problema == 'STUB':
            Relatorio.imprimir_resultado(PSO.melhores_particulas, 86.63)
        else:
            Relatorio.imprimir_resultado(PSO.melhores_particulas, None)
    
    
    def executar_grafico(self, nome_topologia, nome_problema, numero_iteracoes, numero_particulas):
        self.executar(nome_topologia, nome_problema, numero_iteracoes, numero_particulas)
        
        Relatorio.imprimir_grafico(range(TSPConstants.NUMERO_ITERACOES), PSO.fitnesses)
        
        