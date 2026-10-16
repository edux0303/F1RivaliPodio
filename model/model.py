import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._nodes = []
        self.idMap = {}
        self._solBest = []
        self._pesoBest = 0

    # ---------- PUNTO 1 ----------
    def buildGraph(self, anno1,anno2):
        self._grafo.clear()
        self.idMap = {}

        self._nodes = DAO.getNodi(anno1,anno2)
        for n in self._nodes:
            self.idMap[n.driverId] = n

        self._grafo.add_nodes_from(self._nodes)

        for s1, s2,dato in DAO.getCoppie(anno1,anno2):
            if s1 in self.idMap and s2 in self.idMap :
                self._grafo.add_edge(self.idMap[s1], self.idMap[s2],weight=dato)





    def getNodes(self):
        return self._nodes

    def getNumNodi(self):
        return len(self._grafo.nodes)

    def getNumArchi(self):
        return len(self._grafo.edges)
    def getNodiOrdinati(self):
        return sorted(self._grafo.nodes, key=lambda x: (x.forename, x.surname))

    def getTop3(self):
        archi = []
        for u,v,dati in self._grafo.edges(data=True):
            nomi = sorted([u.forename, v.forename])
            archi.append((nomi[0],nomi[1],dati["weight"]))
        archi.sort(key=lambda x: (-x[2],x[0],x[1]))
        return archi[:3]


    def maxPodi(self):
        best = max(self._grafo.nodes, key=lambda x: x.podi)
        return best, best.podi

    def getGradoMax(self):
        best = max(self._grafo.nodes, key=lambda x: self._grafo.degree(x))
        return best, self._grafo.degree(best)


    def getCammino(self,partenza,lun):
        self._solBest = []
        self._pesoBest = -1
        self._ricorsione([partenza],0,lun)
        return self._solBest, self._pesoBest


    def _ricorsione(self,parziale,pesoParziale,lun):
        if len(parziale) - 1 == lun:
            if pesoParziale > self._pesoBest:
                self._pesoBest = pesoParziale
                self._solBest = list(parziale)
            return

        ultimo = parziale[-1]
        for vicino in self._grafo.neighbors(ultimo):
            if vicino in parziale or ultimo.nationality == vicino.nationality:
                continue
            peso = self._grafo[ultimo][vicino]["weight"]
            parziale.append(vicino)
            self._ricorsione(parziale,pesoParziale+peso,lun)
            parziale.pop()

    def getPeso(self, p1, p2):
        return self._grafo[p1][p2]["weight"]

    def getAnni(self):
        return DAO.getAllYears()