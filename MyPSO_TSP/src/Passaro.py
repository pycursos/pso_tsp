'''
Created on 18/08/2012

@author: periclesmiranda
'''

class Passaro(object):

    def __init__(self):
        self.posicao = [];
        self.velocidade = [];
        self.p = [];
        self.g = [];
        self.fitness = 0;
        self.p_fitness = 0;

    def atualizaP(self):
        if self.fitness < self.p_fitness:
            self.p = self.posicao[::];
            self.p_fitness = self.fitness;



    pass

