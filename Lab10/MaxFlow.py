#%%
class Node:
    def __init__(self, label):
        self.label = label
        self.in_e = []
        self.out_e = []
    def add_in_edge(self, edge):
        self.in_e.append(edge)
        return self
    def add_out_edge(self, edge):
        self.out_e.append(edge)
        return self

    
class Edge:
    def __init__(self, start, end, capacity):
        self.start, self.end = start, end
        self.cap, self.flow = capacity, 0

# I started implementing this, but honestly
# it's more painful to do it this way
class Network_bad:
    def __init__(self):
        self.nodes = {
            'S': Node('S'),
            'T': Node('T')
        }
        self.edges = []
    def add_node(self, label):
        self.nodes[label] = Node(label)
        return self
    def add_edge(self, a, b, c):
        self.edges.append(Edge(self.nodes[a], self.nodes[b], c))
        self.nodes[a].add_out_edge(self.edges[-1])
        self.nodes[b].add_in_edge(self.edges[-1])
        return self
    def find_residual(self):
        pass

# I'm doing adjacency matrix instead
# this makes finding the residual graph very very easy,
# and from an encapsulated POV, it's the exact same.
import numpy as np

class Network:
    def __init__(self, flow_mat = None, caps_mat = None, nodes_dict = None):
        if flow_mat is None: flow_mat = np.zeros((2,2))
        if caps_mat is None: caps_mat = np.zeros((2,2))
        if nodes_dict == None: nodes_dict = {'S':0, 'T':1} #idk why but doing this in the function declaration is BAD and the dict was tracking stuff? idk
        self.flow = flow_mat # describes current flow: flow[a, b] is flow from a to b
        self.caps = caps_mat # describes edge capacity: caps[a, b] is capacity for flow from a to b
        self.nodes = nodes_dict # maps node label to index in flow/caps
        self.size = self.flow.shape[0] # how many nodes are in this graph (useful later)
    def add_node(self, label):
        self.nodes[label] = self.size # add another node to the index dict
        # resize flow and cap to add a row and column
        self.flow = np.resize(self.flow, (self.size+1, self.size+1))
        self.caps = np.resize(self.caps, (self.size+1, self.size+1))
        self.size += 1 # update size
    def add_edge(self, a, b, c):
        # check if we're given a and b as labels or indices
        if isinstance(a, str): a = self.nodes[a]
        if isinstance(b, str): b = self.nodes[b]
        # make that edge's capacity nonzero
        self.caps[a, b] = c
    def get_residual_network(self):
        print(self.flow)
        # get the residual network for the current graph
        # flow mat of new network has 2 parts: 
        # (caps-flow) and (flow.T)
        # caps-flow is how much flow we can still push through
        # flow.T is current flow in opposite direction
        # if we add them together we get the full residual network
        return Network(self.caps-self.flow+self.flow.T, 
                       self.caps, # stays the same (unused)
                       self.nodes) # stays the same
    def find_residual(self, current = 'S', visited = [0], min_capacity = np.Inf):
        # finds a residual path
        # call this function only on a network
        # obtained by Network.get_residual_network()

        # make sure current is an index
        if isinstance(current, str): current = self.nodes[current]

        #for each neighbor
        for idx, i in enumerate(self.flow[current]):
            # if this is a fake neighbor (if it's not connected), skip to the next neighbor
            if i==0: continue
            # if we've already visited this node, skip to the next neighbor
            if idx in visited: continue
            # update min capacity if needed
            if i<min_capacity: min_capacity = i
            # add this node to visited
            visited.append(idx)
            # if we've reached the target (our base case), return the path and capacity
            if idx == self.nodes['T']: return visited, min_capacity
            # otherwise recurse
            path, flow = self.find_residual(idx, visited, min_capacity)
            # and if flow is nonzero from the recursion, return it.
            # if it was zero, we don't return to make sure we explore all 
            # neighbors before returning 0
            if flow>0: return path, flow

        # now that we're definitely sure there's no path, we can safely return zero
        return ([],0)


    def solve_network(self):
        # actually solve the path for the maximum flow
        # modifies the network in-place

        # main loop: keep finding residual paths until there aren't any anymore
        while True:
            #find path
            path, flow = self.get_residual_network().find_residual('S', [0], np.Inf)
            print(path, flow)

            # if it's not actually a path, return the total flow leaving the source (this is the answer: the max flow)
            if flow == 0: return sum(self.flow[self.nodes['S']])

            # Otherwise, for each edge in the path, increase its flow by the flow of the path.
            for i in range(len(path)-1):
                self.flow[path[i], path[i+1]]+=flow

if __name__=='__main__':
    # G = Network()      
    # G.add_node('A')
    # G.add_node('B')
    # G.add_node('C')
    # G.add_node('D')
    # G.add_edge('S', 'A', 16)
    # G.add_edge('S', 'C', 13)
    # G.add_edge('C', 'A', 4)
    # G.add_edge('A', 'B', 12)
    # G.add_edge('C', 'D', 14)
    # G.add_edge('B', 'C', 9)
    # G.add_edge('D', 'B', 7)
    # G.add_edge('B', 'T', 20)
    # G.add_edge('D', 'T', 4)

    # G.solve_network()

    snacks = Network()
    snacks.add_node('Alice')
    snacks.add_node('Bob')
    snacks.add_node('Chris')
    snacks.add_node('Dawn')
    snacks.add_node('Edward')
    snacks.add_node('Thin Mints')
    snacks.add_node('Reeses Pieces')
    snacks.add_node('Snickers')
    snacks.add_node('KitKat')
    snacks.add_node('Chex Mix')
    snacks.add_node('Pocky')
    snacks.add_edge('S', 'Thin Mints', 1)
    snacks.add_edge('S', 'Reeses Pieces', 1)
    snacks.add_edge('S', 'Snickers', 1)
    snacks.add_edge('S', 'KitKat', 1)
    snacks.add_edge('S', 'Chex Mix', 1)
    snacks.add_edge('S', 'Pocky', 1)
    snacks.add_edge('Thin Mints', 'Alice', 1)
    snacks.add_edge('Reeses Pieces', 'Alice', 1)
    snacks.add_edge('Snickers', 'Bob', 1)
    snacks.add_edge('Reeses Pieces', 'Bob', 1)
    snacks.add_edge('KitKat', 'Bob', 1)
    snacks.add_edge('Chex Mix', 'Chris', 1)
    snacks.add_edge('Pocky', 'Chris', 1)
    snacks.add_edge('Snickers', 'Chris', 1)
    snacks.add_edge('Chex Mix', 'Dawn', 1)
    snacks.add_edge('Thin Mints', 'Edward', 1)
    snacks.add_edge('Reeses Pieces', 'Edward', 1)
    snacks.add_edge('Snickers', 'Edward', 1)
    snacks.add_edge('KitKat', 'Edward', 1)
    snacks.add_edge('Chex Mix', 'Edward', 1)
    snacks.add_edge('Pocky', 'Edward', 1)
    snacks.add_edge('Alice', 'T', 1)
    snacks.add_edge('Bob', 'T', 1)
    snacks.add_edge('Chris', 'T', 1)
    snacks.add_edge('Dawn', 'T', 1)
    snacks.add_edge('Edward', 'T', 1)
#%%    
    names = dict(zip(snacks.nodes.values(), snacks.nodes.keys()))

    print(snacks.solve_network())
    print(snacks)
    for name, idx in snacks.nodes.items():
        print(name, snacks.flow.T[idx, 10])
    print(snacks.nodes)
# %%

