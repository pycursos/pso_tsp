'''
Created on 28/10/2013

@author: periclesmiranda
'''

import sys
import matplotlib.pyplot as plt

class Relatorio(object):
    
    @staticmethod
    def imprimir_resultado(particulas, alvo=None):
        if particulas[-1].p_fitness <= alvo:
            sys.stdout.write("Alvo alcancado.\n")
        else:
            sys.stdout.write("Alvo nao alcancado.\n")
        
        sys.stdout.write("Menor caminho: ")
        for j in range(len(particulas[0].posicao)):
            sys.stdout.write(str(particulas[-1].posicao[j]) + ", ")
        
        sys.stdout.write("Distancia: " + str(particulas[-1].p_fitness) + "\n")
        return
    
    @staticmethod
    def imprimir_grafico(iterations, melhores_particulas):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(iterations,melhores_particulas, 'k')
        
        ax.grid(True)
        ax.set_ylabel('Fitness',fontsize=14)
        ax.set_xlabel('Iteracoes', fontsize=14)
        
        plt.show()