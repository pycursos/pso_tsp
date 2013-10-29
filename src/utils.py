'''
Created on 28/10/2013

@author: periclesmiranda
'''

class Util(object):
    
    @staticmethod
    def quicksort(array, esquerda, direita):
        pivot = Util.quicksort_partition(array, esquerda, direita)
        
        if esquerda < pivot:
            Util.quicksort(array, esquerda, pivot - 1)
        
        if direita > pivot:
            Util.quicksort(array, pivot + 1, direita)
        
        return array

    @staticmethod
    def quicksort_partition(numeros, esquerda, direita):
        # The comparison is on each particle's pBest value.
        I_hold = esquerda
        r_hold = direita
        pivot = numeros[esquerda]
        
        while esquerda < direita:
            while (numeros[direita].get_fitness() >= pivot.get_fitness()) and (esquerda < direita):
                direita -= 1
            
            if esquerda != direita:
                numeros[esquerda] = numeros[direita]
                esquerda += 1
            
            while (numeros[esquerda].get_fitness() <= pivot.get_fitness()) and (esquerda < direita):
                esquerda += 1
            
            if esquerda != direita:
                numeros[direita] = numeros[esquerda]
                direita -= 1
        
        numeros[esquerda] = pivot
        pivot = esquerda
        esquerda = I_hold
        direita = r_hold
        
        return pivot
        
