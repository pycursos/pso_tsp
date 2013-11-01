import random
import math
import sys
import os
from Leitor import Leitor
from Relatorio import Relatorio
from utils import Util

'''Parametros'''

parametros = {'a280': {'NUMERO_PARTICULAS': 1000, 'VELOCIDADE_MAX': 30, 
                    'NUMERO_ITERACOES': 500, 'NUMERO_CIDADES': 280, 'ALVO': 2800},
                'br17' : {'NUMERO_PARTICULAS': 30, 'VELOCIDADE_MAX': 60,
                    'NUMERO_ITERACOES': 500, 'NUMERO_CIDADES': 500, 'ALVO': 86.63},
                'brazil58': {'NUMERO_PARTICULAS': 30, 'VELOCIDADE_MAX': 60,
                    'NUMERO_ITERACOES': 500, 'NUMERO_CIDADES': 500, 'ALVO': 86.63}}


NUMERO_PARTICULAS = VELOCIDADE_MAX = NUMERO_ITERACOES = NUMERO_CIDADES = ALVO = None
# Velocidade maxima representa o maximo numero de mudancas.  Intervalo: 0 >= VELOCIDADE_MAX < Numero de cidades

''''Variaveis Globais'''
particulas = []
melhores_particulas = []

mapa = []
get_distancia = None

class Particula:
    def __init__(self):
        self.posicao = [0] * NUMERO_CIDADES
        self.fitness = 0
        self.velocidade = 0.0

    def get_posicao(self, index):
        return self.posicao[index]

    def set_posicao(self, index, value):
        self.posicao[index] = value

    def get_fitness(self):
        return self.fitness

    def set_fitness(self, value):
        self.fitness = value

    def get_velocidade(self):
        return self.velocidade

    def set_velocidade(self, velocityScore):
        self.velocidade = velocityScore

class Cidade:
    def __init__(self):
        self.mX = 0
        self.mY = 0
    
    def get_x(self):
        return self.mX
    
    def set_x(self, xCoordenada):
        self.mX = xCoordenada
    
    def get_y(self):
        return self.mY
    
    def set_y(self, yCoordenada):
        self.mY = yCoordenada

def get_distancia_coords(cidade1, cidade2):
    cidadeA = mapa[cidade1]
    cidadeB = mapa[cidade2]
    a2 = math.pow(math.fabs(cidadeA.get_x() - cidadeB.get_x()), 2)
    b2 = math.pow(math.fabs(cidadeA.get_y() - cidadeB.get_y()), 2)
    return math.sqrt(a2 + b2)

def get_distancia_distances(cidade1, cidade2):
    dist = mapa[cidade1][cidade2]
    return dist

def get_distancia_total(index):
    particulas[index].set_fitness(0.0)
    
    for i in range(NUMERO_CIDADES):
        if i == NUMERO_CIDADES - 1:
            particulas[index].set_fitness(particulas[index].get_fitness() + get_distancia(particulas[index].get_posicao(NUMERO_CIDADES - 1), particulas[index].get_posicao(0))) # Complete trip.
        else:
            particulas[index].set_fitness(particulas[index].get_fitness() + get_distancia(particulas[index].get_posicao(i), particulas[index].get_posicao(i + 1)))
    
    return

def cria_mapa(caminho=None, tipo_arquivo=None):
    global mapa, get_distancia
    data = Leitor.cria_coordenadas(caminho, tipo_arquivo)

    if tipo_arquivo == 'C':
        XLocs = data.x_coords
        YLocs = data.y_coords

        get_distancia = get_distancia_coords
        
        numero_cidades = len(data.cities)
        
        for i in range(numero_cidades):
            nova_cidade = Cidade() 
            nova_cidade.set_x(XLocs[i])
            nova_cidade.set_y(YLocs[i])
            mapa.append(nova_cidade)
    
    elif tipo_arquivo in ['M', 'N']:
        mapa = data.distances
        get_distancia = get_distancia_distances
        
    return

def dispor_aleatoriamente(index = 0):
    cidadeA = random.randrange(0, NUMERO_CIDADES)
    cidadeB = 0
    fim = False
    
    while not fim:
        cidadeB = random.randrange(0, NUMERO_CIDADES)
        if cidadeB != cidadeA:
            fim =     True
    
    # swap cidadeA and cidadeB.
    temp = particulas[index].get_posicao(cidadeA)
    particulas[index].set_posicao(cidadeA, particulas[index].get_posicao(cidadeB))
    particulas[index].set_posicao(cidadeB, temp)
    return

def criar_particulas():
    for i in range(NUMERO_PARTICULAS):
        nova_particula = Particula()
        
        for j in range(NUMERO_CIDADES):
            nova_particula.set_posicao(j, j)
        
        particulas.append(nova_particula)
        
        for j in range(NUMERO_CIDADES): # just any number of times to randomize them.
            dispor_aleatoriamente(len(particulas) - 1)
        
        get_distancia_total(len(particulas) - 1)
    
    return


def get_velocidade():
    pior_resultado = 0.0
    vValue = 0.0
    
    # After sorting, worst will be last in list.
    pior_resultado = particulas[NUMERO_PARTICULAS - 1].get_fitness()
    
    for i in range(NUMERO_PARTICULAS):
        vValue = (VELOCIDADE_MAX * particulas[i].get_fitness()) / pior_resultado
        
        if vValue > VELOCIDADE_MAX:
            particulas[i].set_velocidade(VELOCIDADE_MAX)
        elif vValue < 0.0:
            particulas[i].set_velocidade(0.0)
        else:
            particulas[i].set_velocidade(vValue)
    
    return

def copiar_da_particula(fonte, destino):
    # push destino's data points closer to fonte's data points.
    alvoA = random.randrange(0, NUMERO_CIDADES) # fonte's city to target.
    alvoB = 0
    indiceA = 0
    indiceB = 0
    tempIndice = 0
    
    # alvoB will be fonte's neighbor immediately succeeding alvoA (circular).
    for i in range(NUMERO_CIDADES):
        if particulas[fonte].get_posicao(i) == alvoA:
            if i == NUMERO_CIDADES - 1:
                alvoB = particulas[fonte].get_posicao(0) # if end of array, take from beginning.
            else:
                alvoB = particulas[fonte].get_posicao(i + 1)
            
            break
    
    # Move alvoB next to alvoA by switching values.
    for j in range(NUMERO_CIDADES):
        if particulas[destino].get_posicao(j) == alvoA:
            indiceA = j
        
        if particulas[destino].get_posicao(j) == alvoB:
            indiceB = j
    
    # get temp index succeeding indiceA.
    if indiceA == NUMERO_CIDADES - 1:
        tempIndice = 0
    else:
        tempIndice = indiceA + 1
    
    # Switch indexB value with tempIndex value.
    temp = particulas[destino].get_posicao(tempIndice)
    particulas[destino].set_posicao(tempIndice, particulas[destino].get_posicao(indiceB))
    particulas[destino].set_posicao(indiceB, temp)
    
    return

def atualiza_particulas():
    # Best was previously sorted to index 0, so start from the second best.
    for i in range(NUMERO_PARTICULAS):
        if i > 0:
            # The higher the velocity score, the more n_mudancas it will need.
            n_mudancas = math.floor(math.fabs(particulas[i].get_velocidade()))
            
            #sys.stdout.write("Mudancas para a particula " + str(i) + ": " + str(n_mudancas) + "\n")
            
            for j in range(n_mudancas):
                # 50/50 chance.
                if random.random() > 0.5:
                    dispor_aleatoriamente(i)
                
                # Push it closer to it's best neighbor.
                copiar_da_particula(0, i)
            
            # Update pBest value.
            get_distancia_total(i)
    
    return

def executar_DPSO():
    iteracao = 0
    fim = False
    
    criar_particulas()
    
    while not fim:
        # Two conditions can end this loop:
        # if the maximum number of epochs allowed has been reached, or,
        # if the Target value has been found.
        if iteracao < NUMERO_ITERACOES:
            for i in range(NUMERO_PARTICULAS):
                #sys.stdout.write("Rota: ")
                
                for j in range(NUMERO_CIDADES):
                    #sys.stdout.write(str(particulas[i].get_posicao(j)) + ", ")
                    pass
                
                get_distancia_total(i)
                #sys.stdout.write("Distancia: " + str(particulas[i].get_fitness()) + "\n")
                
                if particulas[i].get_fitness() <= ALVO:
                    fim = True
            
            Util.quicksort(particulas, 0, len(particulas) - 1)
            # list has to sorted in order for get_velocidade() to work.
            
            sys.stdout.write("Iteracao " + str(iteracao) + ": " + str(particulas[0].get_fitness()) + "\n")
            
            melhores_particulas.append(particulas[0].get_fitness())
            
            get_velocidade()
            
            atualiza_particulas()
            
            #sys.stdout.write("Iteracao: " + str(iteracao) + "\n")
            
            iteracao += 1
        
        else:
            fim = True
    
    return iteracao


if __name__ == '__main__':
    global NUMERO_PARTICULAS, VELOCIDADE_MAX, NUMERO_ITERACOES, NUMERO_CIDADES, ALVO

    path = os.path.abspath(os.path.dirname(sys.argv[0]))
    cria_mapa(path+ '/data/a280.tsp', 'C')
    NUMERO_PARTICULAS = parametros['a280']['NUMERO_PARTICULAS']
    VELOCIDADE_MAX = parametros['a280']['VELOCIDADE_MAX']
    NUMERO_ITERACOES = parametros['a280']['NUMERO_ITERACOES']
    NUMERO_CIDADES = parametros['a280']['NUMERO_CIDADES']
    ALVO = parametros['a280']['ALVO']

    simulacao1 = 'Simulador rodando com %d particulas, %d iteracoes, Velocidade Maxima: %d e com numero de cidades %d'
    print NUMERO_PARTICULAS, VELOCIDADE_MAX, NUMERO_ITERACOES, NUMERO_CIDADES, ALVO

    print simulacao1 % (NUMERO_PARTICULAS, NUMERO_ITERACOES, VELOCIDADE_MAX, NUMERO_CIDADES)
    total_iteracoes = executar_DPSO()
    Relatorio.imprimir_resultado(particulas, ALVO, NUMERO_CIDADES)
    Relatorio.imprimir_grafico(range(total_iteracoes), melhores_particulas)

