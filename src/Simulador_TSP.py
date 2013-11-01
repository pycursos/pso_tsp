import random
import math
import sys
import os
from Leitor import Leitor
from Relatorio import Relatorio
from utils import Util

NUMERO_PARTICULAS = 100
VELOCIDADE_MAX =  30
NUMERO_ITERACOES = 1000
NUMERO_CIDADES = 280

CONTADOR_EXTINCAO = 10
MAXIMO_EXTINCAO_POR_INERCIA = 5
MAXIMO_INERCIA_POR_ITERACAO = 10

mapa = []

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

class Cidade:
    def __init__(self):
        self.mX = 0
        self.mY = 0
    
    def get_x(self):
        return self.mX
    
    def set_x(self, xCoordenada):
        self.mX = xCoordenada
    
    def get_y(self):
        return self.mY
    
    def set_y(self, yCoordenada):
        self.mY = yCoordenada

class Particula(object):
    def __init__(self):
        self.posicao = range(0, NUMERO_CIDADES)
        random.shuffle(self.posicao)
        self.fitness = 0.0
        self.velocidade = [0] * NUMERO_CIDADES
        self.pBest = None
        self.fitBest = None
        self.iniciar_velocidade()
        #print self.fitness, self.pBest, self.fitBest, self.velocidade


    def iniciar_velocidade(self):
        for i in xrange(NUMERO_CIDADES):
            self.velocidade[i] = random.randint(-VELOCIDADE_MAX, VELOCIDADE_MAX)
        
        self.calcular_fitness()
        self.pBest = self.posicao
        self.fitBest = self.fitness

    def calcular_fitness(self):
        self.fitness = 0.0

        for i in xrange(NUMERO_CIDADES):
            if  i == NUMERO_CIDADES - 1:
                X1X2 = math.pow(mapa[self.posicao[i]].get_x() - mapa[self.posicao[0]].get_x(), 2)
                Y1Y2 = math.pow(mapa[self.posicao[i]].get_y() - mapa[self.posicao[0]].get_y(), 2)
                self.fitness += math.sqrt(X1X2 + Y1Y2)
            else:
                X1X2 = math.pow(mapa[self.posicao[i]].get_x() - mapa[self.posicao[i+1]].get_x(), 2)
                Y1Y2 = math.pow(mapa[self.posicao[i]].get_y() - mapa[self.posicao[i+1]].get_y(), 2)
                self.fitness += math.sqrt(X1X2 + Y1Y2)
 
        if self.fitness < self.fitBest:
            self.pBest = self.posicao
            self.fitBest = self.fitness   

    def get_posicao(self, index):
        return self.posicao[index]

    def set_posicao(self, index, value):
        self.posicao[index] = value

    def get_fitness(self):
        return self.fitness

    def set_fitness(self, value):
        self.fitness = value

    def get_velocidade(self):
        return self.velocidade

    def set_velocidade(self, velocityScore):
        self.velocidade = velocityScore

    def atualizar_velocidade(self, gpBest):
        w = 0.5
        c1 = 2
        c2 = 2
        r1 = random.randrange(0, 100) / 100.0
        r2 = random.randrange(0, 100) / 100.0

        distancias_particulas = self.calcular_distancia(self.posicao, self.pBest)
        distancias_globais = self.calcular_distancia(self.posicao, gpBest)

        for i in xrange(NUMERO_CIDADES):
            self.velocidade[i] = w * self.velocidade[i] + c1 * r1 + distancias_particulas[i] + c2 * r2 * distancias_globais[i]
  
    def calcular_distancia(self, posicaoOrigem, posicaoDestino):
        resultado = []
        for i in xrange(NUMERO_CIDADES):
            resultado.append(posicaoDestino.index(posicaoOrigem[i]) - i)
        return resultado

    def troca_posicoes(self, nova_posicao, nova_velocidade, i, novoSlot):
        direcao = random.randint(0,1)
        rangex = 1

        novoSlot = self.fronteiras(novoSlot)

        while (nova_posicao[novoSlot] != None) or ((novoSlot > NUMERO_CIDADES - 1) or (novoSlot < 0)):
            if direcao == 0:
                novoSlot -= rangex
                direcao = 1
            else:
                novoSlot += rangex
                direcao = 0
            rangex+=1

            if novoSlot > NUMERO_CIDADES - 1:
                novoSlot = 0
            elif novoSlot < 0:
                novoSlot = NUMERO_CIDADES - 1

        print nova_posicao

        nova_posicao[novoSlot] = self.posicao[i]
        nova_velocidade[novoSlot] = self.velocidade[i]

    def fronteiras(self, novoSlot):
        if novoSlot > NUMERO_CIDADES -1:
            return NUMERO_CIDADES - 1
        elif novoSlot < 0:
            return 0
        else:
            return novoSlot
    

    def aplicar_velocidade(self):
        ordem = range(0, NUMERO_CIDADES)
        random.shuffle(ordem)

        nova_velocidade = [None] * NUMERO_CIDADES
        nova_posicao = [None] * NUMERO_CIDADES

        for i in xrange(NUMERO_CIDADES):
            if self.velocidade[ordem[i]] > 0:
                novoSlot = ordem[i] + 1
            elif self.velocidade[ordem[i]] < 0:
                novoSlot = ordem[i]  - 1
            else:
                novoSlot = ordem[i]

            self.troca_posicoes(nova_posicao, nova_velocidade, ordem[i], novoSlot)

        self.posicao = nova_posicao
        self.velocidade = nova_velocidade


class Enxame(object):
    
    def __init__(self):
        self.enxame = [Particula() for i in xrange(NUMERO_PARTICULAS)]
        self.contador_inercia = 0
        self.gBestFit = None
        self.pBest = None
        self.historico = []
        self.iniciar_gBest()

    def resetar_velocidade(self, insticao):
        for particle in self.enxame:
            particle.iniciar_velocidade()

    def atualizar_velocidade(self):
        for i in xrange(NUMERO_PARTICULAS):
            self.enxame[i].atualizar_velocidade(self.pBest)

    def iniciar_gBest(self):
        self.calcular_particulas_fitness()
        self.gBestFit = self.enxame[0].fitness
        self.pBest = self.enxame[0].posicao
        self.procurar_gBest()

    def limpeza_geral(self):
        self.enxame = [Particula()] * NUMERO_PARTICULAS
        self.iniciar_gBest()

    def procurar_gBest(self):
        progressou = False
        for i in xrange(NUMERO_PARTICULAS):
            if self.enxame[i].get_fitness() < self.gBestFit:
                self.gBestFit = self.enxame[i].fitness
                self.pBest = self.enxame[i].posicao
                progressou = True
        
        if progressou:
            self.contador_inercia = 0
        else:
            self.contador_inercia +=1

        print self.gBestFit
        self.historico.append(self.gBestFit)

    
    def aplicar_velocidade(self):
        for i in xrange(NUMERO_PARTICULAS):
            self.enxame[i].aplicar_velocidade()


    def calcular_particulas_fitness(self):
        for i in xrange(NUMERO_PARTICULAS):
            self.enxame[i].calcular_fitness()
 
class PSO(object):

    def run(self):
        #import pdb; pdb.set_trace()
        enxame = Enxame()
        extincao_por_inercia = 0
        extincao_em_massa = 0
        result = (enxame.pBest, enxame.gBestFit)
    
        for extincao in xrange(CONTADOR_EXTINCAO):
            if extincao > 0 and extincao_por_inercia < MAXIMO_EXTINCAO_POR_INERCIA:
                enxame.resetar_velocidade(extincao)
                enxame.contador_inercia =  0
            elif extincao > 0 and extincao_por_inercia > MAXIMO_EXTINCAO_POR_INERCIA -1:
                enxame.limpeza_geral(extincao)
                enxame.contador_inercia = 0
                extincao_por_inercia = 0
                extincao_em_massa +=1
        
            for i in xrange(NUMERO_ITERACOES):
                enxame.atualizar_velocidade()
                enxame.aplicar_velocidade()
                enxame.calcular_particulas_fitness()
                sys.stdout.write("Iteracao " + str(i) + ": " + str(result[1]) + "\n")
                enxame.procurar_gBest()

                if enxame.contador_inercia > MAXIMO_INERCIA_POR_ITERACAO:
                    enxame.contador_inercia = 0
                    break

            if extincao == 0 or enxame.gBestFit < result[1]:
                result = (enxame.pBest, enxame.gBestFit)
                extincao_por_inercia = 0
            else:
                extincao_por_inercia +=1


        fitness_history = enxame.historico

        print fitness_history
        


if __name__ == '__main__':
    path = os.path.abspath(os.path.dirname(sys.argv[0])) 
    cria_mapa(path+ '/data/a280.tsp', 'C')
    pso = PSO()
    pso.run()


