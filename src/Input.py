'''
Created on 22/01/2014

@author: periclesmiranda
'''
import os

class Input(object):

    CAMINHO = os.path.dirname(os.path.realpath(__file__)) + '\\data\\'

    problemas = {
                 'STUB': (None, 'C', 82.0),
                 'A280': (CAMINHO + 'a280.tsp', 'C', 500.0),
                 'BR17': (CAMINHO + 'br17.atsp', 'M', 60.0),
                 'BRAZIL58': (CAMINHO + 'brazil58.tsp', 'N', 750.0)
                 }

