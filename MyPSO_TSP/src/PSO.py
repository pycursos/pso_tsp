#-*- coding: utf-8 -*-
'''
Created on 18/08/2012


@author: periclesmiranda, marcelcaraciolo
'''

import math
import random

from Passaro import Passaro
from Constants import TSPConstants, TSPClanConstants

from topologias.Estrela import Estrela
from topologias.Local import Local
from topologias.Focal import Focal

from topologias.Clan import Clan


from Util import Util
from TSP import Leitor, Cidade

from Relatorio import Relatorio
from topologias import Clan
from topologias.VonNeumann import VonNeumann

''''Variaveis Globais'''
melhores_particulas = []
fitnesses = [];
mapa  = []


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



class TSP_PSO_Clan(TSP_PSO):

    def __init__(self, data, topologia):

        self.passaros = self.inicializarBando()

        self.clans = self.inicializarClans()

        self.topologia = topologia(self.clans)

        for idx, topology in enumerate(self.topologia.topology_bands):
            topology._setG(topology.getG(bando=self.clans[idx]))

        self.conference = self.topologia.getClanLeaders(bandos=self.clans)
        self.topologia.clansTopology._setG((self.topologia.clansTopology.getG(bando=self.conference)))
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

    def simular(self):
        for i in range(0, TSPClanConstants.NUMERO_ITERACOES):
            self._executar();
            print "Simulacao " + str((float(i) / TSPClanConstants.NUMERO_ITERACOES) * 100) + "%";

            melhor_passaro = self.topologia.bestOfBests(bando=self.passaros);

            melhores_particulas.append(melhor_passaro)
            fitnesses.append(melhor_passaro.p_fitness);

        print fitnesses

    def _executar(self):
        #Atualizando as infos de cada clan intra.
        for i in range(0, TSPClanConstants.NUMBER_OF_CLANS):
            bando = self.clans[i]
            for j in range(0, len(bando)):
                self.atualizaInformacaoBando(bando, i, j);
                bando[j].fitness =  TSP.evaluate(bando[j].posicao)
                bando[j].atualizaP()

        #Atualizando as infos dos clans
        self.conference = self.topologia.getClanLeaders(bandos=self.clans)
        for i in range(0, len(self.conference)):
            self.atualizaInformacaoConference(self.conference, i);
            self.conference[i].fitness = TSP.evaluate(self.conference[i].posicao)
            self.conference[i].atualizaP();

    def atualizaInformacaoConference(self, bando, indice_passaro):
        g_best = self.topologia.clansTopology.getG(indice_passaro, bando)
        for i in range(0, TSPConstants.N_DIMENSION):
            self.__atualizaVelocidade(bando[indice_passaro], g_best, i);

        self.__atualizaPosicao(bando[indice_passaro]);

    def atualizaInformacaoBando(self, bando, indice_no_bando, indice_passaro):
        clan_best = self.topologia.getClanLeader(indice_no_bando, bando)
        for i in range(0, TSPClanConstants.N_DIMENSION):
            self.__atualizaVelocidade(bando[indice_passaro], clan_best, i);

        self.__atualizaPosicao(bando[indice_passaro]);

    def __atualizaPosicao(self, passaro):
        velocidade_atual = sum(passaro.velocidade)/TSPConstants.N_DIMENSION;

        #A velocidade atual vai definir o numero de mudan�as que v�o precisar ser feitas
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

        passaro.velocidade[i] = nova_velocidade;
