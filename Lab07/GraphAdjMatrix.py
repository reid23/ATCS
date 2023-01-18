'''
Author: Reid Dye

This is my adjacency matrix implementation.
'''

import numpy as np

class GraphAdjMatrix:
    def __init__(self):
        """Initialize new empty GraphAdjMatrix
        """
        self.mat = np.array([[]], dtype = int)
        self.v = {} # stores mapping of user_node_value : index
    def nodes(self) -> list: 
        """Get a list of the nodes in this graph

        Returns:
            list: all the nodes in this graph
        """
        return list(self.v.keys())
    def addEdge(self, u, v):
        """Adds and edge between u and v

        Args:
            u (hashable): one vertex of the pair to be connected
            v (hashable): the other vertex to be connected

        Returns:
            GraphAdjMatrix: self with the changes made. Changes are in-place, but this allows for chaining.
        """
        # first check if u is already a vertex
        if not (u in self.v):
            # if not, append it on to the end
            self.v[u] = self.mat.shape[1]
            self.mat = np.append(self.mat, np.zeros((self.mat.shape[0], 1), dtype = int), axis=1)
            if not self.mat.shape[1] == 1: #append another row/col (unless it's 1x1 where things break down a little)
                self.mat = np.append(self.mat, np.zeros((1, self.mat.shape[1]), dtype = int), axis=0)
        # do the same thing for v
        if not (v in self.v):
            self.v[v] = self.mat.shape[1]
            self.mat = np.append(self.mat, np.zeros((self.mat.shape[0], 1), dtype = int), axis=1)
            if not self.mat.shape[1] == 1:
                self.mat = np.append(self.mat, np.zeros((1, self.mat.shape[1]), dtype = int), axis=0)
        
        # now that they both definitely exist, set them to be connectedd
        self.mat[self.v[u], self.v[v]] = 1

        return self
    def deleteEdge(self, u, v):
        """deletes an edge between u and v, if it exists.

        Args:
            u (hashable): a vertex.
            v (hashable): the other vertex.

        Raises:
            KeyError: if u or v are not valid indices.

        Returns:
            GraphAdjMatrix: self with the changes made. Changes are made in place, but this allows chaining.
        """
        try: #try to just set it to zero
            self.mat[self.v[u], self.v[v]] = 0
        except KeyError: #handle the error and print it nicely
            raise KeyError(f'One or both of {u} or {v} is not a valid vertex.')
        return self #again, changes are made in-place, this just allows you to chain add/delete.
    def getNeighbors(self, u) -> list:
        """returns a list of the neighbors of u

        Args:
            u (hashable): the node to find the neighbors of

        Raises:
            KeyError: if u is not a valid node

        Returns:
            list: a list of u's neighbors
        """
        try:
            return np.array(list(self.v.keys()))[self.mat[self.v[u]].astype(bool) | self.mat.T[self.v[u]].astype(bool)]
        except KeyError:
            raise KeyError(f'{u} is not a valid vertex.')
    def isAdjacent(self, u, v) -> bool:
        """Checks whether u and v are adjacent.

        Args:
            u (hashable): first vertex
            v (hashable): second vertex

        Raises:
            KeyError: if u or v are not valid vertices

        Returns:
            bool: whether or not u and v are neighbors
        """
        try: #       check the matrix                           check the transpose
            return bool(self.mat[self.v[u], self.v[v]]) or bool(self.mat.T[self.v[u], self.v[v]])
        except KeyError:
            raise KeyError(f'One or both of {u} or {v} is not a valid vertex.')
    def __str__(self) -> str:
        """pretty print implementation

        Returns:
            str: string representation of this graph
        """
        out = '```mermaid\ngraph\n'
        for key in self.v.keys(): #                         can't use getNeighbors here bc we don't want repeats
            connected = " & ".join([str(i) for i in np.array(list(self.v.keys()))[self.mat[self.v[key]].astype(bool)]])
            if len(connected) == 0: continue 
            out += f'    {key}---{connected};\n'
        return out + '```'

if __name__ == '__main__':
    graph = (GraphAdjMatrix().addEdge('A', 'B')
                             .addEdge('A', 'C')
                             .addEdge('A', 'D')
                             .addEdge('B', 'D')
                             .addEdge('E', 'B')
                             .addEdge('E', 'C')
                             .addEdge('E', 'D'))

    print(graph)

    graph.deleteEdge('E', 'C')

    print(graph)
