'''
Created on 18/08/2012

@author: periclesmiranda
'''

'''Constants used to execute the algorithms.'''
class Constants(object):

    N_DIMENSION = 2;

    '''Number of iterations'''
    NUMERO_ITERACOES = 300;

    '''The number of particles which flies through the swarm'''
    TAM_BANDO = 30;

    '''The bounds of the search space'''
    LIMITE_ESPACO_BUSCA = [-5.12, 5.12];

    '''The inferior and superior bounds of the velocity'''
    LIMITE_VELOCIDADE = [-100, 100]

    C1 = 2.05;
    C2 = 2.05;

class TSPConstants(object):

    '''Numero de Cidades'''
    N_DIMENSION = 280

    '''Number of iterations'''
    NUMERO_ITERACOES = 500

    '''The number of particles which flies through the swarm'''
    TAM_BANDO = 30

    '''The inferior and superior bounds of the velocity'''
    LIMITE_VELOCIDADE = [-1000, 1000]

    C1 = 2.05
    C2 = 2.05


class TSPClanConstants(TSPConstants):

    '''
    The number of members for each clan
    '''
    CLAN_SIZE = 6

    '''
    The number of  clans
    '''
    NUMBER_OF_CLANS =  5

