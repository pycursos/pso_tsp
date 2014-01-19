'''
Created on 11/12/2013

@author: periclesmiranda
'''

class Topologia(object):

    def __init__(self):
        pass

    def atualizaInformacao(self, passaro):
        if(passaro.p_fitness < self.g.p_fitness):
            self._setG(passaro)
