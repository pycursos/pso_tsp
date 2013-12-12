'''
Created on 11/12/2013

@author: periclesmiranda
'''
from random import Random
from Constants import Constants
import random

class Util(object):


    @staticmethod
    def copiar_da_particula(fonte, destino):
        # push destino's data points closer to fonte's data points.
        alvoA = Random.randrange(0, Constants.N_DIMENSION) # fonte's city to target.
        alvoB = 0
        indiceA = 0
        indiceB = 0
        tempIndice = 0
        
        # alvoB will be fonte's neighbor immediately succeeding alvoA (circular).
        for i in range(Constants.N_DIMENSION):
            if fonte.posicao[i] == alvoA:
                if i == Constants.N_DIMENSION - 1:
                    alvoB = fonte.posicao[0] # if end of array, take from beginning.
                else:
                    alvoB = fonte.posicao[i + 1]
                
                break
        
        # Move alvoB next to alvoA by switching values.
        for j in range(Constants.N_DIMENSION):
            if destino.posicao[j] == alvoA:
                indiceA = j
            
            if destino.posicao[j] == alvoB:
                indiceB = j
        
        # get temp index succeeding indiceA.
        if indiceA == Constants.N_DIMENSION - 1:
            tempIndice = 0
        else:
            tempIndice = indiceA + 1
        
        # Switch indexB value with tempIndex value.
        temp = destino.posicao[tempIndice]
        destino.posicao[tempIndice] = destino.posicao[indiceB]
        destino.posicao[indiceB] = temp
        
        return
    
    @staticmethod
    def dispor_aleatoriamente(passaro):
        cidadeA = random.randrange(0, Constants.N_DIMENSION)
        cidadeB = 0
        fim = False
        
        while not fim:
            cidadeB = random.randrange(0, Constants.N_DIMENSION)
            if cidadeB != cidadeA:
                fim =     True
        
        # swap cidadeA and cidadeB.
        temp = passaro.posicao[cidadeA]
        passaro.posicao[cidadeA] = passaro.posicao[cidadeB]
        passaro.posicao[cidadeB] = temp
        return 