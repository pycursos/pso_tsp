#-*- coding: utf-8 -*-


import unittest
from Leitor import Leitor


class TesteLeitor(unittest.TestCase):


    def test_leitor(self):
        data = Leitor.ler_arquivo('./data/a280.tsp')
        print data

        data = Leitor.ler_arquivo('./data/br17.atsp','M')
        print data
        self.assertRaises(KeyError,data.distance2cities,1 ,1)
        self.assertEquals(data.distance2cities(1,17), 5)
        self.assertEquals(data.distance2cities(17,1), 5)
        
        print data.distance_from(1)

        data = Leitor.ler_arquivo('./data/brazil58.tsp', 'N')
        print data

if __name__ == '__main__':
    unittest.main()
