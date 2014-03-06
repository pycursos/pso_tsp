'''
Created on 22/01/2014

@author: periclesmiranda
'''
from Input import Input
from TSP import Leitor, Cidade
import PSO
from Constants import TSPConstants, TSPClanConstants
from topologias.Estrela import Estrela
from topologias.Local import Local
from topologias.Focal import Focal
from topologias.VonNeumann import VonNeumann
from topologias.Clan import Clan
from Relatorio import Relatorio
from PSO import TSP_PSO, TSP_PSO_Clan
from time import time

mean_fitnesses_evolution = []#Armazena o fitness da melhor particula em cada iteracao de todas as simulacoes
fitnesses_of_best = []#Armazena o fitness final da melhor particula em cada simulacao
best_particles = []

mean_simulation = []

class Simulador(object):

    def executar(self, nome_topologia, nome_problema, numero_iteracoes, numero_particulas, executions, dispersion , \
                dispersion_iteration, iteration_criteria):
        #Calculando o tempo
        time_inicio = time()

        TSPConstants.NUMERO_ITERACOES = numero_iteracoes
        TSPConstants.TAM_BANDO = numero_particulas
        TSPConstants.DISPERSION_ITERACAO = dispersion_iteration

        if nome_problema in Input.problemas.keys():

            problema = Input.problemas[nome_problema]
            PSO.cria_mapa(problema[0], problema[1])
            TSPConstants.STOP_CRITERIA = problema[2]

        else:
            print 'Nome do problema invalido. Veja nomes disponiveis no pacote "input/Dados."'


        TSPConstants.N_DIMENSION = len(PSO.mapa)
        algoritmo = None


        for i in range(executions):

            if nome_topologia == 'ESTRELA':
                algoritmo = TSP_PSO(PSO.mapa, Estrela, dispersion, iteration_criteria)
            elif nome_topologia == 'LOCAL':
                algoritmo = TSP_PSO(PSO.mapa, Local, dispersion, iteration_criteria)
            elif nome_topologia == 'FOCAL':
                algoritmo = TSP_PSO(PSO.mapa, Focal, dispersion, iteration_criteria)
            elif nome_topologia == 'VONNEUMANN':
                algoritmo = TSP_PSO(PSO.mapa, VonNeumann, dispersion, iteration_criteria)
            elif nome_topologia == 'CLAN':
                TSPClanConstants.N_DIMENSION = len(PSO.mapa)
                algoritmo = TSP_PSO_Clan(PSO.mapa, Clan, dispersion, iteration_criteria)
            else:
                print 'Nao existe topologia com este nome.'

            if algoritmo != None:
                algoritmo.simular()

                mean_fitnesses_evolution.append(PSO.fitnesses)
                fitnesses_of_best.append(PSO.fitnesses[-1])
                best_particles.append(PSO.best_particle[0])

                PSO.fitnesses = []
                PSO.best_particle = []

        time_fim = time()
        time_total = float(time_fim - time_inicio)/executions


        mean_simulation.append(Relatorio.imprimir_resultado_final(fitnesses_of_best, mean_fitnesses_evolution, best_particles, time_total))


    def executar_grafico(self, nome_topologia, nome_problema, numero_iteracoes, numero_particulas, executions, dispersion, dispersion_iteration, iteration_stop_criteria):
        self.executar(nome_topologia, nome_problema, numero_iteracoes, numero_particulas, executions, dispersion, dispersion_iteration, iteration_stop_criteria)

        if iteration_stop_criteria:
            Relatorio.imprimir_grafico(range(TSPConstants.NUMERO_ITERACOES), mean_simulation[0])

        else:
            Relatorio.imprimir_grafico(range(len(mean_simulation[0])), mean_simulation[0])

