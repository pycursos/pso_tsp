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
    
    ''''(1)TOPOLOGIA DESEJADA (2)PROBLEMA A SER RESOLVIDO (3)NUMERO DE ITERACOES (4) numero de individuos'''
    simulador.executar_grafico('ESTRELA', 'BRAZIL58', 100, 30)