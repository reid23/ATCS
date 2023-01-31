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
        return self
    def add_edge(self, a, b, c):
        # check if we're given a and b as labels or indices
        if isinstance(a, str): a = self.nodes[a]
        if isinstance(b, str): b = self.nodes[b]
        # make that edge's capacity nonzero
        self.caps[a, b] = c
        return self
    def get_residual_network(self):
        # print(self.flow)
        # get the residual network for the current graph
        # flow mat of new network has 2 parts: 
        # (caps-flow) and (flow.T)
        # caps-flow is how much flow we can still push through
        # flow.T is current flow in opposite direction
        return Network(self.caps-self.flow, 
                       self.flow.T,
                       self.nodes) # stays the same
    def find_residual(self, current = 'S', visited = [(0, 1)], min_capacity = np.Inf):
        # finds a residual path
        # call this function only on a network
        # obtained by Network.get_residual_network()

        # make sure current is an index
        if isinstance(current, str): current = self.nodes[current]
        # if we've reached the target (our base case), return the path and capacity
        if current == self.nodes['T']: return visited, min_capacity
        # for each neighbor
        for idx, i in enumerate(self.flow[current]):
            # if this is a fake neighbor (if it's not connected), skip to the next neighbor
            if i==0: continue
            # if we've already visited this node, skip to the next neighbor
            if (idx, 1) in visited or (idx, -1) in visited: continue
            # otherwise recurse                 add node to visited  update min capacity if needed
            path, flow = self.find_residual(idx, visited+[(idx, 1)], min(min_capacity, i))
            # and if flow is nonzero from the recursion, return it.
            # if it was zero, we don't return to make sure we explore all 
            # neighbors before returning 0
            # print(path, flow)
            if flow>0: return path, flow
        for idx, i in enumerate(self.caps[current]):
            if i==0: continue
            if (idx, 1) in visited or (idx, -1) in visited: continue
            path, flow = self.find_residual(idx, visited+[(idx, -1)], min(min_capacity, i))
            # print(path, flow)
            if flow>0: return path, flow
        # now that we're definitely sure there's no path, we can safely return zero
        return ([],0)


    def solve_network(self):
        # actually solve the path for the maximum flow
        # modifies the network in-place

        # main loop: keep finding residual paths until there aren't any anymore
        while True:
            #find path
            path, flow = self.get_residual_network().find_residual('S', [(0, 1)], np.Inf)
            print(path, flow)

            # if it's not actually a path, return the total flow leaving the source (this is the answer: the max flow)
            if flow == 0: return sum(self.flow[self.nodes['S']])

            # Otherwise, for each edge in the path, increase its flow by the flow of the path.
            for i in range(len(path)-1):
                if path[i+1][1]>0:
                    self.flow[path[i][0], path[i+1][0]] += flow*path[i+1][1]
                else:
                    self.flow[path[i+1][0], path[i][0]] += flow*path[i+1][1]
#%%
def test_graph_from_class():
    G = (Network()      
        .add_node('A')
        .add_node('B')
        .add_node('C')
        .add_node('D')
        .add_edge('S', 'A', 16)
        .add_edge('S', 'C', 13)
        .add_edge('C', 'A', 4)
        .add_edge('A', 'B', 12)
        .add_edge('C', 'D', 14)
        .add_edge('B', 'C', 9)
        .add_edge('D', 'B', 7)
        .add_edge('B', 'T', 20)
        .add_edge('D', 'T', 4))

    print(G.solve_network())
def snacks():
    snacks = (Network()
        .add_node('Alice')
        .add_node('Bob')
        .add_node('Chris')
        .add_node('Dawn')
        .add_node('Edward')
        .add_node('Thin Mints')
        .add_node('Reeses Pieces')
        .add_node('Snickers')
        .add_node('KitKat')
        .add_node('Chex Mix')
        .add_node('Pocky')
        .add_edge('S', 'Thin Mints', 1)
        .add_edge('S', 'Reeses Pieces', 1)
        .add_edge('S', 'Snickers', 1)
        .add_edge('S', 'KitKat', 1)
        .add_edge('S', 'Chex Mix', 1)
        .add_edge('S', 'Pocky', 1)
        .add_edge('Thin Mints', 'Alice', 1)
        .add_edge('Reeses Pieces', 'Alice', 1)
        .add_edge('Snickers', 'Bob', 1)
        .add_edge('Reeses Pieces', 'Bob', 1)
        .add_edge('KitKat', 'Bob', 1)
        .add_edge('Chex Mix', 'Chris', 1)
        .add_edge('Pocky', 'Chris', 1)
        .add_edge('Snickers', 'Chris', 1)
        .add_edge('Chex Mix', 'Dawn', 1)
        .add_edge('Thin Mints', 'Edward', 1)
        .add_edge('Reeses Pieces', 'Edward', 1)
        .add_edge('Snickers', 'Edward', 1)
        .add_edge('KitKat', 'Edward', 1)
        .add_edge('Chex Mix', 'Edward', 1)
        .add_edge('Pocky', 'Edward', 1)
        .add_edge('Alice', 'T', 1)
        .add_edge('Bob', 'T', 1)
        .add_edge('Chris', 'T', 1)
        .add_edge('Dawn', 'T', 1)
        .add_edge('Edward', 'T', 1))

    print('max snack flow:', snacks.solve_network()) 
    # display a grid of people/snacks
    # flow is [from, to] and the edges are from snacks to people
    # so we do flow[snacks_range, people_range]
    print('  A  B  C  D  E')
    print(snacks.flow[7:13, 2:7]) # 7-12 are snacks, 2-7 are people
    print('rows key:')
    print('thin mints\nreeses pieces\nsnickers\nkitkat\nchex mix\npocky')
def trading():
    money = np.array([
        ['A', 5, 1],
        ['B', 2, 1],
        ['C', 1, 5],
        ['D', 3, 5],
        ['E', 4, 3]
    ], dtype=object)
    total_money = sum(money[:, 1])
    trades = Network()

    for i in money:
        (trades.add_node(f'{i[0]}_i')
               .add_edge('S', f'{i[0]}_i', i[1]))
    for i in money:
        (trades.add_node(f'{i[0]}_f')
               .add_edge('T', f'{i[0]}_f', i[2]))
    for i in money[:, 0]:
        for j in money[:, 0]:
            trades.add_edge(f'{i}_i', f'{j}_f', total_money)
    print(trades.caps)
    print(trades.flow)
    print(trades.solve_network())
    print(trades.flow)
    print(trades.nodes)
    print(trades.get_residual_network().flow)
    print(trades.get_residual_network().caps)
# %%


if __name__=='__main__':
    # snacks works
    snacks()