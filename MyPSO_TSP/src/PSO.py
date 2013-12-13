'''
Created on 18/08/2012

@author: periclesmiranda
'''
from Passaro import Passaro
import random
from Constants import Constants
from Sphere import Sphere
from topologias import Estrela
from Util import Util

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