'''

Clan Topology

@author marcelcaraciolo

'''


from topologias.Topologia import Topologia
from topologias.Estrela import Estrela

class Clan(Topologia):

    def __init__(self, number_of_clans):
        Topologia.__init__(self)
        self.topology_bands = [Estrela() for i in range(len(number_of_clans))]
        self.clansTopology  =  Estrela()

    def getClanLeaders(self, bandos):
        leaders = []
        for idx, topology in enumerate(self.topology_bands):
            leaders.append(topology.getG(bando=bandos[idx]))

        return leaders

    def getG(self, passaro_indice=None, bando=None):
        return self.clansTopology.getG(passaro_indice, bando)

