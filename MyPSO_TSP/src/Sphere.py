#-*- coding:utf-8-*-

'''
Created on 18/08/2012

@author: periclesmiranda
'''

'''Extends Problem class'''
class Sphere():

    @staticmethod
    def evaluate(values):
        total = 0.0
        for value in values:
            total += (value ** 2.0)

        return total
