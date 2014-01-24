'''
Created on 22/01/2014

@author: periclesmiranda
'''
import os

class Input(object):

    CAMINHO = os.path.dirname(os.path.realpath(__file__)) + '\\data\\'
    
    problemas = {
                 'STUB': (None, 'C'),
                 'A280': (CAMINHO + 'a280.tsp', 'C'),
                 'BR17': (CAMINHO + 'br17.atsp', 'N'),
                 'BRAZIL58': (CAMINHO + 'brazil58.tsp', 'M')
                 }
        