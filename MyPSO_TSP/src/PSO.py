#-*- coding: utf-8 -*-
'''
Created on 18/08/2012

@ author: periclesmiranda
'''
from Passaro import Passaro
import random
from Constants import TSPConstants

from topologias.Estrela import Estrela
from topologias.Local import Local

from Util import Util
from TSP import Leitor, Cidade


import math
from topologias.Focal import Focal
from Relatorio import Relatorio

''''Variaveis Globais'''
melhores_particulas = []
fitnesses = [];
mapa  = []


	
class TSP_PSO_Clan(TSP_PSO):

    def __init__(self, data):

        self.passaros = self.inicializarBando()

        self.clans = self.inicializarClans()

        self.topologia = Clan(self.clans)

        self.conference = self.topologia.getClanLeaders(bandos=self.clans)

        self.topologia._setG(self.topologia.getG(bando=self.conference))

    def inicializarClans(self):
        indices_passaros = range(len(self.passaros))
        random.shuffle(indices_passaros)

        assert TSPClanConstants.TAM_BANDO == TSPClanConstants.CLAN_SIZE * TSPClanConstants.NUMBER_OF_CLANS, 'TAM_BANDO = CLAN_SIZE * NUMBER_OF_CLANS'

        clans = []

        for i in range(TSPClanConstants.NUMBER_OF_CLANS):
            clans.append([])
            for j in range(TSPClanConstants.CLAN_SIZE):
                clans[i].append(self.passaros[indices_passaros.pop()])

        return clans
		

class TSP(object):
    @staticmethod
    def evaluate(posicao):
        fitness = 0.0

        for i in xrange(TSPConstants.N_DIMENSION):
            if  i == TSPConstants.N_DIMENSION - 1:
                X1X2 = math.pow(mapa[posicao[i]].get_x() - mapa[posicao[0]].get_x(), 2)
                Y1Y2 = math.pow(mapa[posicao[i]].get_y() - mapa[posicao[0]].get_y(), 2)
                fitness += math.sqrt(X1X2 + Y1Y2)
            else:
                X1X2 = math.pow(mapa[posicao[i]].get_x() - mapa[posicao[i+1]].get_x(), 2)
                Y1Y2 = math.pow(mapa[posicao[i]].get_y() - mapa[posicao[i+1]].get_y(), 2)
                fitness += math.sqrt(X1X2 + Y1Y2)

        return fitness


def cria_mapa(caminho=None, tipo_arquivo=None):
    global mapa
    data = Leitor.cria_coordenadas(caminho, tipo_arquivo)

    if tipo_arquivo == 'C':
        XLocs = data.x_coords
        YLocs = data.y_coords

        numero_cidades = len(data.cities)

        for i in range(numero_cidades):
            nova_cidade = Cidade()
            nova_cidade.set_x(XLocs[i])
            nova_cidade.set_y(YLocs[i])
            mapa.append(nova_cidade)
            
    if tipo_arquivo == 'M':
        pass
    if tipo_arquivo == 'N':
        pass


class TSP_PSO():
    def __init__(self, data, topologia):
        self.passaros = self.inicializarBando()
        self.topologia = topologia()

        self.topologia._setG(self.topologia.getG(None, bando=self.passaros))

    def inicializarBando(self):
        passaros = []
        for i in range(0, TSPConstants.TAM_BANDO):
            passaro = Passaro();
            velocity_init = [0.0]*TSPConstants.N_DIMENSION

            passaro.velocidade = velocity_init;
            passaro.posicao = range(TSPConstants.N_DIMENSION)
            random.shuffle(passaro.posicao)

            passaro.p = passaro.posicao[::];
            passaro.g = passaro.posicao[::];
            passaro.fitness = TSP.evaluate(passaro.posicao)
            passaro.p_fitness = passaro.fitness;

            passaros.append(passaro);

        return passaros

    def simular(self):
        for i in range(0, TSPConstants.NUMERO_ITERACOES):
            self._executar();
            print "Simulacao " + str((float(i) / TSPConstants.NUMERO_ITERACOES) * 100) + "%";

            melhor_passaro = self.topologia.bestOfBests(bando=self.passaros);
            
            melhores_particulas.append(melhor_passaro)
            fitnesses.append(melhor_passaro.p_fitness);

        print fitnesses

    def atualizaInformacao(self, indice_passaro):
        g_best = self.topologia.getG(indice_passaro, self.passaros)

        for i in range(0, TSPConstants.N_DIMENSION):
            self.__atualizaVelocidade(self.passaros[indice_passaro], g_best, i);

        self.__atualizaPosicao(self.passaros[indice_passaro]);

    def __atualizaPosicao(self, passaro):
        velocidade_atual = sum(passaro.velocidade)/TSPConstants.N_DIMENSION/2;

        #A velocidade atual vai definir o numero de mudancas que vao precisar ser feitas        
        for j in range(int(velocidade_atual)):
            # 50/50 chance.
            if random.random() > 0.5:
                Util.dispor_aleatoriamente(passaro)

            # Push it closer to it's best neighbor.
            Util.copiar_da_particula(passaro.g, passaro.posicao)


    def __atualizaVelocidade(self, passaro, g_best, i):
        c1 = TSPConstants.C1;
        c2 = TSPConstants.C2;

        velocidade_atual = passaro.velocidade[i];

        posicao_atual = passaro.posicao[i];
        p = passaro.p[i];

        passaro.g = g_best.p[::];

        nova_velocidade = 0.4*velocidade_atual + c1*random.random()*(p - posicao_atual) + c2*random.random()*(passaro.g[i] - posicao_atual);

        '''
        if(nova_velocidade > TSPConstants.LIMITE_VELOCIDADE[1]):
            nova_velocidade = TSPConstants.LIMITE_VELOCIDADE[1];
        elif(nova_velocidade < TSPConstants.LIMITE_VELOCIDADE[0]):
            nova_velocidade = TSPConstants.LIMITE_VELOCIDADE[0];
        '''

        passaro.velocidade[i] = abs(nova_velocidade);

    def _executar(self):
        for i in range(0, TSPConstants.TAM_BANDO):
            self.atualizaInformacao(i);

            self.passaros[i].fitness = TSP.evaluate(self.passaros[i].posicao)

            self.passaros[i].atualizaP();


if __name__ == '__main__':
    import os, sys
    #path = os.path.abspath(os.path.dirname())
    path_a280 = 'C:/Documents and Settings/periclesmiranda/Meus documentos/eclipse-jee-ganymede-SR2-win32/Projects/AATSP_Simulador/src/data/a280.tsp'
    path_br17 = 'C:/Documents and Settings/periclesmiranda/Meus documentos/eclipse-jee-ganymede-SR2-win32/Projects/AATSP_Simulador/src/data/br17.atsp'
    path_brazil58 = 'C:/Documents and Settings/periclesmiranda/Meus documentos/eclipse-jee-ganymede-SR2-win32/Projects/AATSP_Simulador/src/data/brazil58.tsp' 
    
    #Roda stub
    #cria_mapa(None, None)
    
    #Roda a280.tsp
    #cria_mapa(path_a280, 'C')
    
    #Roda br17.tsp
    #cria_mapa(path_br17, 'N')
    
    #Roda brazil58.tsp
    cria_mapa(path_brazil58, 'M')
    
    TSPConstants.N_DIMENSION = len(mapa)

    algorithm = TSP_PSO(mapa, Estrela)
    algorithm.simular()
    
    #Roda stub
    #Relatorio.imprimir_resultado(melhores_particulas, 86.63)
    
    Relatorio.imprimir_resultado(melhores_particulas, None)
    Relatorio.imprimir_grafico(range(TSPConstants.NUMERO_ITERACOES), fitnesses)

