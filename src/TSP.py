#-*- coding: utf-8  -*-
'''

Codigo para leitura das cidades

'''

import re

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

class DataCoords(object):

    def __init__(self, cities, x_coords, y_coords, docs):
        self.cities = cities
        self.x_coords = x_coords
        self.y_coords = y_coords
        self.docs = docs

    def coords(self, city):
        return zip(self.x_coords, self.y_coords)[self.cities.index(city)]

    def __repr__(self):
        return '\n'.join([self.docs, 'Number of Cities: %d' % len(self.cities)])

class DataDistances(object):
    def __init__(self, distances, docs):
        self.distances = distances
        self.cities = self.distances.keys()
        self.docs = docs

    def distance2cities(self, from_city, to_city):
        return self.distances[from_city][to_city]

    def distance_from(self, from_city):
        return self.distances[from_city]

    def __repr__(self):
        return '\n'.join([self.docs, 'Number of Cities: %d' % len(self.cities)])


class Leitor(object):

    @staticmethod
    def ler_arquivo(caminho, modo='C'):
        '''
        Leitura dos arquivos de dados.

        Parametros
        ----------

        caminho:  str
        Caminho onde esta armazenado o arquivo a ser lido.

        mode: str
        Tipo de arquivo a ser lido. Pode ser um dos seguintes
        modos:

        'C':  3 colunas: a primeira é o ID das cidades, a segunda e
        terceira colunas são as coordenadas X e Y respectivamente.

        'M': uma matriz triangular superior, desconsiderando a diagonal
        que seria a distancia da cidade a ela mesma, a inferior seria
        apenas a transposta desta. Os valores representam as distâncias
        entre as cidades.

        'N':  matriz NxN onde N é o número de cidades. Os valores são as
        distâncias entre as cidades.

    '''
        input_file = open(caminho)
        docs = ""
        cities = []
        x_coords = []
        y_coords = []
        distances = {}

        if modo == 'C':
            for line, content in enumerate(input_file):
                if any([ x in content for x in ['NAME', 'COMMENT', 'TYPE', 'DIMENSION',
                                'EDGE', 'NODE']]):
                    docs += content
                    continue
                if content.strip() and 'EOF' not in content:
                    city_id, X, Y = map(int,re.findall(r'(\d+)', content))
                    cities.append(cities)
                    x_coords.append(X)
                    y_coords.append(Y)
            return DataCoords(cities, x_coords, y_coords, docs)

        elif modo == 'M':
            nro = 1
            for line, content in enumerate(input_file):
                if any([ x in content for x in ['NAME', 'COMMENT', 'TYPE', 'DIMENSION',
                                'EDGE', 'NODE']]):
                    docs += content
                    continue
                if content.strip() and 'EOF' not in content:
                    d = map(int,re.findall(r'(\d+)', content))
                    distances.setdefault(nro, {})
                    for idx, distance in enumerate(d):
                        if idx + 1 == nro:
                            continue
                        distances[nro][idx+1] = distance
                        distances.setdefault(idx+1, {})
                        distances[idx+1][nro] = distance
                    nro +=1
            return DataDistances(distances,docs)

        elif modo == 'N':
            nro = 1
            for line, content in enumerate(input_file):
                if any([ x in content for x in ['NAME', 'COMMENT', 'TYPE', 'DIMENSION',
                                'EDGE', 'NODE']]):
                    docs += content
                    continue
                if content.strip() and 'EOF' not in content:
                    d = map(int,re.findall(r'(\d+)', content))
                    distances.setdefault(nro, {})
                    start = nro + 1
                    for idx, distance in enumerate(d):
                        distances[nro][start+idx] = distance
                        distances.setdefault(start+idx, {})
                        distances[start+idx][nro] = distance
                    nro +=1
            return DataDistances(distances,docs)

    @staticmethod
    def cria_coordenadas(caminho=None, tipo_arquivo=None):
        if caminho == None:
            return Leitor.stub()
        else:
            return Leitor.ler_arquivo(caminho, tipo_arquivo)


    @staticmethod
    def stub():
        XLocs = [30, 40, 40, 29, 19, 9, 9, 20]
        YLocs = [5, 10, 20, 25, 25, 19, 9, 5]
        return DataCoords(range(len(XLocs)),XLocs, YLocs, None)


if __name__ == '__main__':
    import os,sys

    path = os.path.abspath(os.path.dirname(sys.argv[1]))
    data = Leitor.cria_coordenadas(path+ '/data/a280.tsp', 'C')
    print data
    data = Leitor.cria_coordenadas(path+ '/data/br17.atsp', 'M')
    print data
    data = Leitor.cria_coordenadas(path+ '/data/brazil58.tsp', 'N')
    print data



