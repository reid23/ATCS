import numpy as np
import numpy.linalg
import re
class letters:
    mapping = dict(zip('0123456789ABCDEFGHIJKLMNOP', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
    def __init__(self):
        self.n = -1
    def __iter__(self):
        self.n = -1
        return self
    def __next__(self):
        self.n += 1
        return str([letters.mapping[char] for char in np.base_repr(self.n, 26)])
    
class GraphAdjMatrix:
    # __init__():  initialize your graph
    # addEdge(u,v): adds the edge between vertices u and v to 
    #   the graph (one or both of the vertices may not be part 
    #   of the graph yet, so you need to add them)
    # deleteEdge(u,v): deletes the edge between vertices u and 
    #   v. If that edge doesn’t exist, it should return an error 
    #   message.
    # getNeighbors(u): returns a LIST of the neighbors of vertex 
    #   u (note that it’s returning a list and not a pointer to 
    #   the head of the linked list of neighbors)
    # isAdjacent(u,v): returns True if u and v are adjacent and 
    #   False otherwise
    def __init__(self):
        self.mat = np.array([[]], dtype = int)
        self.v = {}
    def addEdge(self, u, v):
        if not (u in self.v):
            self.v[u] = self.mat.shape[1]
            self.mat = np.append(self.mat, np.zeros((self.mat.shape[0], 1), dtype = int), axis=1)
            if not self.mat.shape[1] == 1:
                self.mat = np.append(self.mat, np.zeros((1, self.mat.shape[1]), dtype = int), axis=0)
        if not (v in self.v):
            self.v[v] = self.mat.shape[1]
            self.mat = np.append(self.mat, np.zeros((self.mat.shape[0], 1), dtype = int), axis=1)
            if not self.mat.shape[1] == 1:
                self.mat = np.append(self.mat, np.zeros((1, self.mat.shape[1]), dtype = int), axis=0)
        self.mat[self.v[u], self.v[v]] = 1
    def deleteEdge(self, u, v):
        try:
            self.mat[self.v[u], self.v[v]] = 0
        except KeyError:
            raise Exception(f'One or both of {v} or {u} is not a valid vertex.')
    def getNeighbors(self, u):
        return np.array(list(self.v.keys()))[self.mat[self.v[u]].astype(bool)]
    def isAdjacent(self, u, v):
        return bool(self.mat[u, v])
    def __str__(self):
        out = '```mermaid\ngraph\n'
        l = letters()
        for key in self.v.keys():
            connected = " & ".join([str(i) for i in self.getNeighbors(key)])
            if len(connected) == 0: continue 
            out += f'    {key}---{connected};\n'
        return out + '```'

from llist import llist
l = llist()
class GraphAdjList:
    def __init__(self):
        self.adjlist = []
        self.v = {}
    def addEdge(self, u, v):
        if not u in self.v: 
            self.v[u] = len(self.adjlist)
            self.adjlist.append(llist(u, v))
        else:
            print(self.adjlist[self.v[u]].insert(v))

        if not v in self.v: 
            self.v[v] = len(self.adjlist)
            self.adjlist.append(llist(v, u))
        else:
            print(self.adjlist[self.v[v]].insert(u))
    def deleteEdge(self, u, v):
        try:
            self.adjlist[self.v[u]].delete(v)
            self.adjlist[self.v[v]].delete(u)
        except KeyError:
            raise Exception(f'One or both of {u} and {v} is not a valid vertex.')
        except ValueError:
            raise Exception(f'No edge exists between {u} and {v}.')
    def getNeighbors(self, u):
        return list(self.adjlist[self.v[u]].itervalues())
    def isAdjacent(self, u, v):
        return v in self.adjlist[self.v[u]]
    def __str__(self):
        out = '```mermaid\ngraph;\n'
        seen = []
        for counter, node in enumerate(self.v.keys()):
            seen.append(node)
            for i in self.adjlist[self.v[node]]:
                print(i, seen)
                this_node = ''
                if not i in seen:
                    this_node+=f'---{i}'
                if not this_node: continue
                out += f'    {node}{this_node};'+'\n'
        return out + '```'


g = GraphAdjList()
g.addEdge('A', 'B')
g.addEdge('A', 'C')
g.addEdge('A', 'D')
g.addEdge('B', 'D')
g.addEdge('E', 'B')
g.addEdge('E', 'C')
g.addEdge('E', 'D')

print(str(g))
print(*[repr(i) for i in g.adjlist], sep = '\n')

graph = np.array([
#    A B C D
    [0  ,0.5,1  ,0.5],
    [0.5,0  ,0  ,0.5],
    [0.5,0  ,0  ,0],
    [0  ,0.5,0  ,0]
])
# A ---- B
# |  \   |
# |   \  |
# |    \ |
# C      D
# start = np.array([[1],[0],[0],[0]])
# for i in range(100):
#     start = graph@start
#     # start = start/np.linalg.norm(start)
#     print(start)
    



