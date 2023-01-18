#%%
import numpy as np
import numpy.linalg
import matplotlib.pyplot as plt

#%%
def randGeoGraph(A, B, N, D):
    nodes = np.append(
        np.random.randint(0, A, (N, 1)), # random x
        np.random.randint(0, B, (N, 1)), # random y
        axis=1 # append them so each element is [x, y]
    )
    edges = {} # init edges dict
    for i_idx, i in enumerate(nodes):
      # connections  = where (distance to all other vertices is less than D) is not zero (aka not false)
        edges[i_idx] = (np.linalg.norm(nodes-i, axis=1)<=D).nonzero()[0]

    return nodes, edges
# %%
def drawGraph(V, E, ax, *highlights):
    ax.scatter(*V.T) # scatter plot to draw all nodes
    # draw all edges
    for start, neighbors in E.items(): # for each node,
        for end in neighbors: # for each of it's neighbors, 
            # plot a line from the node to that connection
            ax.plot([V[start][0], V[end][0]], [V[start][1], V[end][1]])
    if highlights:
        ax.scatter(*np.array(highlights).T, color='orange', zorder=10)

def drawGraphDebug(V, E, D, source, ax, Q, *highlights):
    ax.scatter(*V.T) # scatter plot to draw all nodes
    # draw all edges
    for start, neighbors in E.items(): # for each node,
        for end in neighbors: # for each of it's neighbors, 
            # plot a line from the node to that connection
            ax.plot([V[start][0], V[end][0]], [V[start][1], V[end][1]])
    if highlights:
        ax.scatter(*np.array(highlights).T, color='orange', zorder=10)

    ax.add_patch(plt.Circle(V[source], radius=D, color='orange', fill=False, zorder=9, linestyle='dashed'))
    for idx, node in enumerate(V):
        ax.text(*node, Q.get_cost(idx))
    ax.text(*V[source], 'source', zorder=11)

# drawGraph(*randGeoGraph(50, 50, 50, 13), ax)
# %%
class priority_queue:
    def __init__(self, elements = {}):
        self.elements = elements
        self.seen = {}
    def update(self, element, cost):
        try: 
            if cost <= self.elements[element]:
                self.elements[element] = cost
                return True
            return False
        except KeyError:
            if cost <= self.seen[element]:
                self.seen[element] = cost
                return True
            return False
    def force_update(self, element, cost):
        try:
            self.elements[element] = cost
        except KeyError:
            self.seen[element] = cost
    def pop(self):
        if len(self.elements) == 0: raise KeyError
        val = min(self.elements, key=lambda x: self.elements[x])
        cost = self.elements[val]
        self.elements.pop(val)
        self.seen[val] = cost
        return val, cost
    def get_cost(self, key):
        try:
            return self.elements[key]
        except KeyError:
            return self.seen[key]
#%%
def dist(x1, x2):
    return np.linalg.norm(x1-x2)

#%%
def roadtrip(V, E, D, source, target):
    days_costs = priority_queue(dict(zip(
        range(len(V)), # indices
        [np.Inf] * len(V) # distances
    )))
    distance_costs = priority_queue(dict(zip(
        range(len(V)),
        [np.Inf] * len(V)
    )))
    days_costs.update(source, 0)
    distance_costs.update(source, 0)

    while True:
        try:
            cur = days_costs.pop()
        except KeyError:
            break

        for i in E[cur[0]]: # for each neighbor of cur,
            # update distance cost to the increased value
            # update costs if needed
            days_costs.update(i, cur[1] + (dist(V[cur[0]], V[i]) + distance_costs.get_cost(cur[0]))//D)
            distance_costs.update(i, (dist(V[cur[0]], V[i]) + distance_costs.get_cost(cur[0])))

    # return days_costs
    return days_costs.get_cost(target), days_costs

D = 9


V, E = randGeoGraph(30, 30, 20, D)
soln, Q = roadtrip(V, E, D, 5, 9)

fig, ax = plt.subplots()
# drawGraph(V, E, ax, V[5], V[9])
drawGraphDebug(V, E, D, 5, ax, Q, V[5], V[8])


# %%
def checkPath(V,E,S,T,L):
    if S==T: return True
    if L<=0: return False
    for idx in E[S]:
        if checkPath(V, E, idx, T, L-1): return True
    return False

def iterativeDeepening(V,E,S,T,LB,UB):
    lower, upper = LB, UB
    while True:
        if lower==upper: return upper
        if lower >= UB or upper <= LB: return False
        if checkPath(V,E,S,T,(lower+upper)//2):
            upper = (lower+upper)//2
        else:
            lower = (lower+upper)//2 + 1


S, T = 5, 9
V, E = randGeoGraph(50, 50, 20, 13)
fig, ax = plt.subplots()
drawGraph(V, E, ax, V[S], V[T])
iterativeDeepening(V,E,S,T,0,50)


# %%
