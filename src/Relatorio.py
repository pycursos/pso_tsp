'''
Created on 28/10/2013

@author: periclesmiranda
'''

import sys
import matplotlib.pyplot as plt
import numpy

class Relatorio(object):
    
    @staticmethod
    def imprimir_resultado(particulas, fitnesses, melhores_posicoes, alvo=None):
        
        if alvo != None:
            print ""
            if particulas[-1].p_fitness <= alvo:
                sys.stdout.write("Alvo alcancado.\n")
            else:
                sys.stdout.write("Alvo nao alcancado.\n")
        
        print ""
        print "------------RELATORIO---------------"
        print ""
        print "Evolucao das rotas:"
        for item in melhores_posicoes:
            print item
        
        print ""
        print "Evolucao do fitness por iteracao:"
        print fitnesses
        
        print ""
        sys.stdout.write("Menor caminho: ")
        for j in range(len(particulas[0].posicao)):
            sys.stdout.write(str(particulas[-1].posicao[j]) + ", ")
        
        print ""
        sys.stdout.write("Distancia do menor caminho: " + str(particulas[-1].p_fitness) + "\n")
        return
    
    @staticmethod
    def imprimir_resultado_final(fitness_best, fitnesses_evolution, best_particles, tempo):
        mean = []
        
        
        print ""
        print "Evolucao media do fitness por iteracao:"
        
        sums = numpy.sum(fitnesses_evolution, 0)#vector
        
        for i in range(len(fitnesses_evolution[0])):
            mean.append(sums[i] / len(fitnesses_evolution))
        
        print mean
        
        print ""
        print "Media dos melhores fitness ao final de cada simulacao: " + str(numpy.mean(fitness_best))
        print "Desvio padrao: "+ str(numpy.std(fitness_best))
        
        print ""
        sys.stdout.write("Menor caminho da simulacao: ")
        ordered = sorted(best_particles, key = lambda p: p.p_fitness);
        print ordered[0].p
        
        print ""
        sys.stdout.write("Distancia do menor caminho: " + str(ordered[0].p_fitness) + "\n")
        
        print ""
        print "Tempo de execucao medio (segundos): " + str(tempo)
        
        return mean
    
    
    @staticmethod
    def imprimir_grafico(iterations, melhores_particulas):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(iterations,melhores_particulas, 'k')
        
        ax.grid(True)
        ax.set_ylabel('Fitness',fontsize=14)
        ax.set_xlabel('Iteracoes', fontsize=14)
        
        plt.show()