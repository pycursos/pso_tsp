'''
Created on 22/01/2014

@author: periclesmiranda
'''
from Simulador import Simulador

'''''
PROBLEMAS EXISTENTES

    'STUB'
    'A280'
    'BR17'
    'BRAZIL58'

TOPOLOGIA EXISTENTES

    ESTRELA
    LOCAL
    FOCAL
    VONNEUMANN
    CLAN
'''''

if __name__ == '__main__':

    simulador = Simulador()

    ''''(1)TOPOLOGIA DESEJADA (2)PROBLEMA A SER RESOLVIDO (3)NUMERO DE ITERACOES (4) numero de individuos (5) numero de vezes que simulacao vai executar
        (6) DISPERSAO (True ou False)  (7) DISPERSION ITERATION (A quants iteracoes ele realiza o procedimento de reinicializacao)
    '''
    simulador.executar_grafico('CLAN', 'BR17', 50, 30, 3, True, 20)

