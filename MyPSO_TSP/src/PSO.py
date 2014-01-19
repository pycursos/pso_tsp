#-*- coding: utf-8 -*-
'''
Created on 18/08/2012

@ author: periclesmiranda
'''
from Passaro import Passaro
import random
from Constants import Constants, TSPConstants
from Sphere import Sphere
from topologias.Estrela import Estrela
from Util import Util
from TSP import Leitor, Cidade


import math

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


class PSO(object):

    def __init__(self):
        self.passaros = self.inicializarBando();
        self.topologia = Estrela();

        self.topologia._setG(self.topologia.getG(self.passaros));

    def inicializarBando(self):
        passaros = []
        for i in range(0, Constants.TAM_BANDO):
            passaro = Passaro();
            velocity_init = [0]*Constants.N_DIMENSION;
            position_init = velocity_init[::];

            passaro.velocidade = velocity_init;
            passaro.posicao = self.__rand_uniform(position_init, Constants.LIMITE_ESPACO_BUSCA[0], Constants.LIMITE_ESPACO_BUSCA[1]);
            passaro.p = passaro.posicao[::];
            passaro.g = passaro.posicao[::];
            passaro.fitness = Sphere.evaluate(passaro.posicao)
            passaro.p_fitness = passaro.fitness;

            passaros.append(passaro);

        return passaros;

    def simular(self):

        fitnesses = [];

        for i in range(0, Constants.NUMERO_ITERACOES):
            self._executar();
            print "Simulacao " + str((float(i) / Constants.NUMERO_ITERACOES) * 100) + "%";

            melhor_passaro = self.topologia._getG().p_fitness;
            fitnesses.append(melhor_passaro);

        print fitnesses

    def _executar(self):
        for i in range(0, Constants.TAM_BANDO):
            self.atualizaInformacao(i);

            self.passaros[i].fitness = Sphere.evaluate(self.passaros[i].posicao)

            self.passaros[i].atualizaP();

    def atualizaInformacao(self, indice_passaro):
        g_best = self.topologia.getG(indice_passaro, self.passaros)

        for i in range(0, Constants.N_DIMENSION):
            self.__atualizaVelocidade(self.passaros[indice_passaro], g_best, i);

        self.__atualizaPosicao(self.passaros[indice_passaro]);

    def __atualizaPosicao(self, passaro):
        velocidade_atual = sum(passaro.velocidade)/Constants.N_DIMENSION;

        #A velocidade atual vai definir o numero de mudanças que vão precisar ser feitas
        for j in range(int(velocidade_atual)):
            # 50/50 chance.
            if random.random() > 0.5:
                Util.dispor_aleatoriamente(passaro)

            # Push it closer to it's best neighbor.
            Util.copiar_da_particula(passaro.g, passaro.posicao)

    def __atualizaVelocidade(self, passaro, g_best, i):
        c1 = Constants.C1;
        c2 = Constants.C2;

        velocidade_atual = passaro.velocidade[i];

        posicao_atual = passaro.posicao[i];
        p = passaro.p[i];

        passaro.g = g_best.p[::];

        nova_velocidade = 0.4*velocidade_atual + c1*random.random()*(p - posicao_atual) + c2*random.random()*(passaro.g[i] - posicao_atual);

        if(nova_velocidade > Constants.LIMITE_VELOCIDADE[1]):
            nova_velocidade = Constants.LIMITE_VELOCIDADE[1];
        elif(nova_velocidade < Constants.LIMITE_VELOCIDADE[0]):
            nova_velocidade = Constants.LIMITE_VELOCIDADE[0];

        passaro.velocidade[i] = nova_velocidade;

    def __rand_uniform(self, vector, inferior_limit, superior_limit):
        for i in range(len(vector)):
            randomReal = random.uniform(inferior_limit,
                                        superior_limit)
            vector[i] = randomReal;
        return vector;



class TSP_PSO(PSO):
    def __init__(self, data, topologia):
        self.passaros = self.inicializarBando()
        self.topologia = topologia()

        self.topologia._setG(self.topologia.getG(bando=self.passaros))

    def inicializarBando(self):
        passaros = []
        for i in range(0, TSPConstants.TAM_BANDO):
            passaro = Passaro();
            velocity_init = [0.0]*TSPConstants.N_DIMENSION

            passaro.velocidade = velocity_init;
            passaro.posicao = range(TSPConstants.N_DIMENSION)
            random.shuffle(passaro.posicao)

            #self.__rand_uniform(position_init, TSPConstants.LIMITE_ESPACO_BUSCA[0], TSPConstants.LIMITE_ESPACO_BUSCA[1]);
            passaro.p = passaro.posicao[::];
            passaro.g = passaro.posicao[::];
            passaro.fitness = TSP.evaluate(passaro.posicao)
            passaro.p_fitness = passaro.fitness;

            passaros.append(passaro);

        return passaros

    def simular(self):
        fitnesses = [];

        for i in range(0, TSPConstants.NUMERO_ITERACOES):
            self._executar();
            print "Simulacao " + str((float(i) / TSPConstants.NUMERO_ITERACOES) * 100) + "%";

            melhor_passaro = self.topologia.getG().p_fitness;
            fitnesses.append(melhor_passaro);

        print fitnesses

    def atualizaInformacao(self, indice_passaro):
        g_best = self.topologia.getG(indice_passaro, self.passaros)

        for i in range(0, TSPConstants.N_DIMENSION):
            self.__atualizaVelocidade(self.passaros[indice_passaro], g_best, i);

        self.__atualizaPosicao(self.passaros[indice_passaro]);

    def __atualizaPosicao(self, passaro):
        velocidade_atual = sum(passaro.velocidade)/TSPConstants.N_DIMENSION;

        #A velocidade atual vai definir o numero de mudanças que vão precisar ser feitas
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

        if(nova_velocidade > TSPConstants.LIMITE_VELOCIDADE[1]):
            nova_velocidade = TSPConstants.LIMITE_VELOCIDADE[1];
        elif(nova_velocidade < TSPConstants.LIMITE_VELOCIDADE[0]):
            nova_velocidade = TSPConstants.LIMITE_VELOCIDADE[0];

        passaro.velocidade[i] = nova_velocidade;

    def _executar(self):
        for i in range(0, TSPConstants.TAM_BANDO):
            self.atualizaInformacao(i);

            self.passaros[i].fitness = Sphere.evaluate(self.passaros[i].posicao)

            self.passaros[i].atualizaP();


if __name__ == '__main__':
    import os, sys
    path = os.path.abspath(os.path.dirname(sys.argv[1]))
    cria_mapa(path+ '/data/a280.tsp', 'C')
    TSPConstants.N_DIMENSION = len(mapa)

    algorithm = TSP_PSO(mapa, Estrela)
    algorithm.simular()
