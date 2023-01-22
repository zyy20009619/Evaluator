import numpy as np
import networkx as nx
import math


class Chameleon:
    W = None
    Conn = None
    clusters = None
    MI = 0

    def __init__(self, datanum, mi):
        self.W = np.ones((datanum, datanum))
        self.Conn = np.zeros((datanum, datanum))
        self.datanum = datanum
        self.clusters = []
        self.MI = mi
        self.inter_EC = None

    def buildWeightMatrix(self, data):
        for i in range(data.shape[0]):
            row = data[i]
            temp = data - row
            temp = np.multiply(temp, temp)
            temp = np.sum(temp, axis=1)
            self.W[i] = 1 / np.sqrt(temp)
            self.W[i][i] = 1.0

    def buildSmallCluster(self):
        K = 2
        for i in range(self.W.shape[0]):
            row = self.W[i]
            index = np.argsort(row)
            index = index[-K:]
            index = list(index)
            self.Conn[i, index] = 1
            self.Conn[i][i] = 0

        nodes = []
        edges = []
        for i in range(len(self.Conn)):
            nodes.append(i)
            for j in range(len(self.Conn)):
                if self.Conn[i][j] == 1:
                    edges.append((i, j))
        
        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)

        C = sorted(nx.connected_components(G), key=len, reverse=True)
        for c in C:
            cluster = []
            for node in c:
                cluster.append(node)
            self.clusters.append(cluster)

    def printClusters(self):
        for i in range(len(self.clusters)):
            item = self.clusters[i]
            print(item)

    def cluster(self):
        self.interConnectivity()
        l = len(self.clusters)
        end = True
        i = 0
        while i < l:
            EC_i = self.inter_EC[i]
            j = i + 1
            while j < l:
                EC_j = self.inter_EC[j]
                vec1 = self.clusters[i]
                vec2 = self.clusters[j]
                EC = 0.0
                for k in range(len(vec1)):
                    for m in range(len(vec2)):
                        EC += self.W[vec1[k]][vec2[m]] 
                    
                RI = 2 * EC / (EC_i + EC_j)
                RC = (len(vec1) + len(vec2)) * EC / (len(vec2) * EC_i + len(vec1) * EC_j)
                if RI * math.pow(RC, 2) > self.MI:
                    self.mergeClusters(i, j)
                    l -= 1
                    end = False
                    break
                j = j + 1
            i = i + 1
        if not end:
            self.cluster()
        return self.clusters
            
    def interConnectivity(self):
        l = len(self.clusters)
        self.inter_EC = [0 for i in range(l)]
        for i in range(l):
            vec = self.clusters[i]
            for j in range(len(vec)):
                for k in range(len(vec)):
                    self.inter_EC[i] += self.W[vec[j]][vec[k]]

    def mergeClusters(self, a, b):
        item = self.clusters[b]
        self.clusters.pop(b)
        self.clusters[a].extend(item)


def getCoChangeCluster(data):
    cham = Chameleon(data.shape[0], 0.3)
    cham.buildWeightMatrix(data)
    cham.buildSmallCluster()
    cluster = cham.cluster()

    return cluster