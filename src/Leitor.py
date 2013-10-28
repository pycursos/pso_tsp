'''
Created on 28/10/2013

@author: periclesmiranda
'''

class Leitor(object):
    
    @staticmethod
    def ler_arquivo(path):
        pass
    
    @staticmethod
    def cria_matriz():
        return Leitor.stub()
        
    @staticmethod
    def stub():
        
        XLocs = [30, 40, 40, 29, 19, 9, 9, 20]  
        YLocs = [5, 10, 20, 25, 25, 19, 9, 5]
        
        return XLocs, YLocs