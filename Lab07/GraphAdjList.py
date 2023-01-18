'''
Author: Reid Dye

This is my adjacency list implementation.
'''

from llist import llist

class GraphAdjList:
    def __init__(self):
        """Initializes an empty GraphAdjList
        """
        self.adjlist = []
        self.v = {} # stores mapping of user's node names : adjlist indices
    def nodes(self):
        """gets a list of the nodes in this graph.

        Returns:
            list: all the nodes in this graph.
        """
        return list(self.v.keys())
    def addEdge(self, u, v):
        """adds and edge between u and v

        Args:
            u (any): vertex to connect
            v (any): vertex to connect

        Returns:
            GraphAdjList: self with the changes made. All changes are in-place, but this allows chaining.
        """
        # first check if u is a vertex already
        if not u in self.v: 
            # if not, make it one, appending it onto the end
            self.v[u] = len(self.adjlist)
            self.adjlist.append(llist(u, v)) #pre-connect it to v
        else:
            # otherwise just set v as a connection
            self.adjlist[self.v[u]] = self.adjlist[self.v[u]].insert(v) 
            # have to do assignment bc of some quirks with llist
            # essentially inserting at the beginning doesn't work in-place because 
            # you can't overwrite self, even if you do self.__dict__ = other.__dict___
            # something something __slots__ something something metaclass something something idk

        # now do the same thing for v
        if not v in self.v: 
            self.v[v] = len(self.adjlist)
            self.adjlist.append(llist(v, u))
        else:
            self.adjlist[self.v[v]] = self.adjlist[self.v[v]].insert(u)

        return self # allows chaining of add/delete edges
    def deleteEdge(self, u, v):
        """deletes the edge between u and v.

        Args:
            u (hashable): first vertex
            v (hashable): other vertex

        Raises:
            KeyError: If u or v are not valid vertices
            ValueError: If there is no edge between u and v

        Returns:
            GraphAdjList: self with changes made. Changes are made in-place as well.
        """
        try: # try to just delete them from each other's lists
            self.adjlist[self.v[u]] = self.adjlist[self.v[u]].delete(v) #reassignment again bc of 
            self.adjlist[self.v[v]] = self.adjlist[self.v[v]].delete(u) #llist weirdness
        except KeyError: # if that fails bc u or v doesn't exist
            raise KeyError(f'One or both of {u} and {v} is not a valid vertex.')
        except ValueError: # if that fails bc u and v aren't connected
            raise ValueError(f'No edge exists between {u} and {v}.')
        return self #again, for chaining
    def getNeighbors(self, u) -> list:
        """gets neighbors of u

        Args:
            u (hashable): the node to find the neighbors of
        
        Raises:
            KeyError: if u is not a valid vertex

        Returns:
            list: a list of the neighbors of u
        """
        try:
            return list(self.adjlist[self.v[u]])
        except KeyError:
            raise KeyError(f'{u} is not a valid index.')
    def isAdjacent(self, u, v) -> bool:
        """checks whether u and v are neighbors

        Args:
            u (hashable): first node
            v (hashable): second node

        Raises:
            KeyError: if u or v are not valid verties

        Returns:
            bool: whether u and v are neighbors
        """
        if not (u in self.v and v in self.v): raise KeyError(f'One or both of {u} and {v} are not valid vertices')
        return v in self.adjlist[self.v[u]]

    def __str__(self) -> str:
        """pretty printing for this graph

        Returns:
            str: a string representation of this graph
        """
        out = '```mermaid\ngraph TD;\n'
        seen = []
        for node in self.v.keys():
            seen.append(node)
            this_node = ''
            for i in self.adjlist[self.v[node]]:
                if not i in seen:
                    this_node+=f'---{i}' if not this_node else f' & {i}'
            if this_node: out += f'    {node}{this_node};'+'\n'
        return out + '```'

if __name__=='__main__':
    graph = (GraphAdjList().addEdge('A', 'B')
                           .addEdge('A', 'C')
                           .addEdge('A', 'D')
                           .addEdge('B', 'D')
                           .addEdge('E', 'B')
                           .addEdge('E', 'C')
                           .addEdge('E', 'D'))
    print(graph)
    graph.deleteEdge('E', 'C')
    print(graph)
