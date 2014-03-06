#-*- coding: utf-8 -*-
'''
Created on 18/08/2012


@author: periclesmiranda, marcelcaraciolo
'''

import math
import random

from Passaro import Passaro
from Constants import TSPConstants, TSPClanConstants
from Util import Util
from TSP import Leitor, Cidade

''''Variaveis Globais'''
fitnesses = []
best_particle = []
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

class TSP_Distances(object):
    @staticmethod
    def evaluate(posicao):
        fitness = 0.0
        for i in xrange(TSPConstants.N_DIMENSION):
            if i == TSPConstants.N_DIMENSION - 1:
                #print posicao[i], posicao[0]
                #print mapa[posicao[i]+1]
                fitness += mapa[posicao[i]+1][posicao[0]+1]
            else:
                #print posicao[i], posicao[i+1]
                #print mapa[posicao[i]]
                fitness += mapa[posicao[i]+1][posicao[i+1]+1]

        return fitness

#evaluation function to choose: TSP_Distances for br17 and brazil58 and TSP for a280.tsp
fitness_function = TSP


def cria_mapa(caminho=None, tipo_arquivo=None):
    global mapa, fitness_function
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
        fitness_function = TSP

    if tipo_arquivo == 'M':
        mapa = data.distances
        fitness_function = TSP_Distances
    if tipo_arquivo == 'N':
        mapa = data.distances
        fitness_function = TSP_Distances


class TSP_PSO():
    def __init__(self, data, topologia, dispersion=False, iteration_criteria=False):
        self.passaros = self.inicializarBando()
        self.topologia = topologia()

        self.topologia._setG(self.topologia.getG(None, bando=self.passaros))

        self.dispersion =  dispersion

        self.best_fitness = 100000000

        self.iteration_criteria = iteration_criteria

    def inicializarBando(self):
        global fitness_function
        passaros = []
        for i in range(0, TSPConstants.TAM_BANDO):
            passaro = Passaro();
            velocity_init = [0.0]*TSPConstants.N_DIMENSION

            passaro.velocidade = velocity_init;
            passaro.posicao = range(TSPConstants.N_DIMENSION)
            random.shuffle(passaro.posicao)

            passaro.p = passaro.posicao[::];
            passaro.g = passaro.posicao[::];
            passaro.fitness = fitness_function.evaluate(passaro.posicao)
            passaro.p_fitness = passaro.fitness;

            passaros.append(passaro);

        return passaros

    def reiniciarBando(self, bando):
        global fitness_function
        passaros = []
        for i in range(len(bando)):
            passaro = Passaro();
            velocity_init = [0.0]*TSPConstants.N_DIMENSION

            passaro.velocidade = velocity_init;
            passaro.posicao = range(TSPConstants.N_DIMENSION)
            random.shuffle(passaro.posicao)

            passaro.p = passaro.posicao[::];
            passaro.g = passaro.posicao[::];
            passaro.fitness = fitness_function.evaluate(passaro.posicao)
            passaro.p_fitness = passaro.fitness;

            passaros.append(passaro);

        return passaros

    def stop_criteria(self):
        print 'Minimo ate agora encontrado:', self.best_fitness, 'Minimo Global:', TSPConstants.STOP_CRITERIA
        if self.best_fitness > TSPConstants.STOP_CRITERIA:
            return False
        else:
            return True

    def simular(self):
        if self.iteration_criteria:
            for i in range(0, TSPConstants.NUMERO_ITERACOES):
                print i
                if self.dispersion:
                    if (i % TSPConstants.DISPERSION_ITERACAO == 0) and i != 0:
                        #get the top 10 best particles, store it, and initialize the rest.
                        #only for minimization problems
                        bando_ordenado = sorted(self.passaros, key = lambda p: p.p_fitness)
                        self.passaros =  bando_ordenado[:10] +  self.reiniciarBando(bando_ordenado[10:])
                        print 'reinicializado o bando'
                        assert len(self.passaros) == TSPConstants.TAM_BANDO

                self._executar();
                print "Simulacao " + str((float(i) / TSPConstants.NUMERO_ITERACOES) * 100) + "%";

                melhor_passaro = self.topologia.bestOfBests(bando=self.passaros);

                fitnesses.append(melhor_passaro.p_fitness);

                self.best_fitness = melhor_passaro.p_fitness

            best_particle.append(melhor_passaro)

        else:
            i = 0
            while not self.stop_criteria():
                if self.dispersion:
                    if (i % TSPConstants.DISPERSION_ITERACAO == 0) and i != 0:
                        #get the top 10 best particles, store it, and initialize the rest.
                        #only for minimization problems
                        bando_ordenado = sorted(self.passaros, key = lambda p: p.p_fitness)
                        self.passaros =  bando_ordenado[:10] +  self.reiniciarBando(bando_ordenado[10:])
                        print 'reinicializado o bando'
                        assert len(self.passaros) == TSPConstants.TAM_BANDO

                self._executar();
                #print "Simulacao " + str((float(i) / TSPConstants.NUMERO_ITERACOES) * 100) + "";

                melhor_passaro = self.topologia.bestOfBests(bando=self.passaros);

                fitnesses.append(melhor_passaro.p_fitness);

                self.best_fitness = melhor_passaro.p_fitness

                i+=1

            best_particle.append(melhor_passaro)

            print 'A simulacao atingiu o minimo na iteracao %d'  %  i

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

        passaro.velocidade[i] = abs(nova_velocidade);

    def _executar(self):
        global fitness_function
        for i in range(0, TSPConstants.TAM_BANDO):
            self.atualizaInformacao(i);

            self.passaros[i].fitness = fitness_function.evaluate(self.passaros[i].posicao)

            self.passaros[i].atualizaP();



class TSP_PSO_Clan(TSP_PSO):

    def __init__(self, data, topologia, dispersion=False, iteration_criteria=False):

        self.passaros = self.inicializarBando()

        self.clans = self.inicializarClans()

        self.topologia = topologia(self.clans)

        self.dispersion = dispersion

        self.iteration_criteria = iteration_criteria

        for idx, topology in enumerate(self.topologia.topology_bands):
            topology._setG(topology.getG(bando=self.clans[idx]))

        self.conference = self.topologia.getClanLeaders(bandos=self.clans)
        self.topologia.clansTopology._setG((self.topologia.clansTopology.getG(bando=self.conference)))
        self.topologia._setG(self.topologia.getG(bando=self.conference))

        self.best_fitness = 100000000



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
        if self.iteration_criteria:
            for i in range(0, TSPClanConstants.NUMERO_ITERACOES):

                if self.dispersion:
                    if (i % TSPClanConstants.DISPERSION_ITERACAO == 0) and i != 0:
                        #get the top 10 best particles, store it, and initialize the rest.
                        #get the top 10 best particles, store it, and initialize the rest.
                        #only for minimization problems
                        bando_ordenado = sorted(self.passaros, key = lambda p: p.p_fitness)
                        self.passaros =  bando_ordenado[:10] +  self.reiniciarBando(bando_ordenado[10:])
                        print 'reinicializado o bando'
                        self.clans = self.inicializarClans()
                        assert len(self.passaros) == TSPConstants.TAM_BANDO


                self._executar();
                print "Simulacao " + str((float(i) / TSPClanConstants.NUMERO_ITERACOES) * 100) + "%";

                melhor_passaro = self.topologia.bestOfBests(bando=self.passaros);

                fitnesses.append(melhor_passaro.p_fitness);

                self.best_fitness = melhor_passaro.p_fitness

            best_particle.append(melhor_passaro)
        else:
            i = 0
            while not self.stop_criteria():
                if self.dispersion:
                    if (i % TSPClanConstants.DISPERSION_ITERACAO == 0) and i != 0:
                        #get the top 10 best particles, store it, and initialize the rest.
                        #get the top 10 best particles, store it, and initialize the rest.
                        #only for minimization problems
                        bando_ordenado = sorted(self.passaros, key = lambda p: p.p_fitness)
                        self.passaros =  bando_ordenado[:10] +  self.reiniciarBando(bando_ordenado[10:])
                        print 'reinicializado o bando'
                        self.clans = self.inicializarClans()
                        assert len(self.passaros) == TSPConstants.TAM_BANDO


                self._executar();
                #print "Simulacao " + str((float(i) / TSPClanConstants.NUMERO_ITERACOES) * 100) + "%";

                melhor_passaro = self.topologia.bestOfBests(bando=self.passaros);

                fitnesses.append(melhor_passaro.p_fitness);

                self.best_fitness = melhor_passaro.p_fitness

                i+=1

            best_particle.append(melhor_passaro)


    def _executar(self):
        global fitness_function
        #Atualizando as infos de cada clan intra.
        for i in range(0, TSPClanConstants.NUMBER_OF_CLANS):
            bando = self.clans[i]
            for j in range(0, len(bando)):
                self.atualizaInformacaoBando(bando, i, j);
                bando[j].fitness =  fitness_function.evaluate(bando[j].posicao)
                bando[j].atualizaP()

        #Atualizando as infos dos clans
        self.conference = self.topologia.getClanLeaders(bandos=self.clans)
        for i in range(0, len(self.conference)):
            self.atualizaInformacaoConference(self.conference, i);
            self.conference[i].fitness = fitness_function.evaluate(self.conference[i].posicao)
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

        passaro.velocidade[i] = nova_velocidade;

