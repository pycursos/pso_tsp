'''
Created on 28/10/2013

@author: periclesmiranda
'''

import sys
import matplotlib.pyplot as plt

class Relatorio(object):
    
    @staticmethod
    def imprimir_resultado(particulas, alvo, n_cidades):
        if particulas[0].get_fitness() <= alvo:
            sys.stdout.write("Alvo alcancado.\n")
        else:
            sys.stdout.write("Alvo nao alcancado.\n")
        
        sys.stdout.write("Menor caminho: ")
        for j in range(n_cidades):
            sys.stdout.write(str(particulas[0].get_posicao(j)) + ", ")
        
        sys.stdout.write("Distancia: " + str(particulas[0].get_fitness()) + "\n")
        return
    
    @staticmethod
    def imprimir_grafico(iterations, melhores_particulas):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(iterations,melhores_particulas, 'k')
        
        #ax.legend("",'upper left', shadow=True)
        
        ax.set_yticks(range(0,150,10))
        ax.set_xticks(range(0,len(iterations),10))
        ax.grid(True)
        ax.set_ylabel('Fitness',fontsize=14)
        ax.set_xlabel('Iteracoes', fontsize=14)
        #ax.set_title('Mean of ' + str(metric_type) + ' per generation')
        
        plt.show()