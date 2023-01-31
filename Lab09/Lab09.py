#%%
import numpy as np
import numpy.linalg
import matplotlib.pyplot as plt

#%%
def randGeoGraph(A, B, N, D):
    # generate random coordinates matrix with shape (N, 2)
    nodes = np.append(
        np.random.randint(0, A, (N, 1)), # random x
        np.random.randint(0, B, (N, 1)), # random y
        axis=1 # append them so each element is [x, y]
    )
    edges = {} # init edges dict
    # find and write down all edges
    for i_idx, i in enumerate(nodes):
      # connections  = where (distance to all other vertices is less than D) is not zero (aka not false)
        edges[i_idx] = (np.linalg.norm(nodes-i, axis=1)<=D).nonzero()[0]

    return nodes, edges
# %%
def drawGraph(V, E, ax, *highlights):
    ax.scatter(*V.T, color='black', zorder=2) # scatter plot to draw all nodes
    # draw all edges
    for start, neighbors in E.items(): # for each node,
        for end in neighbors: # for each of it's neighbors, 
            # plot a line from the node to that connection
            ax.plot([V[start][0], V[end][0]], [V[start][1], V[end][1]], color='tab:blue', zorder=1)
    
    # highlight certain nodes in a different color
    if highlights:
        ax.scatter(*np.array(highlights).T, color='orange', zorder=3)

#* for debugging, not neccessary for functionality
def drawGraphDebug(V, E, D, source, ax, Q, *highlights):
    ax.scatter(*V.T, color='black', zorder=2) # scatter plot to draw all nodes
    # draw all edges
    for start, neighbors in E.items(): # for each node,
        for end in neighbors: # for each of it's neighbors, 
            # plot a line from the node to that connection
            ax.plot([V[start][0], V[end][0]], [V[start][1], V[end][1]], color='tab:blue', zorder=1)
    if highlights:
        ax.scatter(*np.array(highlights).T, color='orange', zorder=3)

    ax.add_patch(plt.Circle(V[source], radius=D, color='orange', fill=False, zorder=4, linestyle='dashed'))
    for idx, node in enumerate(V):
        ax.text(*node, np.format_float_positional(Q.get_cost(idx), trim='-'))
    ax.text(*V[source], 'source', zorder=5)
    
fig, ax = plt.subplots()
drawGraph(*randGeoGraph(50, 50, 50, 13), ax)
# %%
#priority queue implementation
class priority_queue:
    def __init__(self, elements = {}):
        self.elements = elements #starting elements
        self.seen = {} #vertices we've popped go here
    def update(self, element, cost):
        # updates element's cost if the cost passed here is better
        # first try updating self.elements
        try: 
            if cost <= self.elements[element]:
                self.elements[element] = cost
                return True
            return False
        # if that doesn't work, update from self.seen instead
        except KeyError:
            if cost <= self.seen[element]:
                self.seen[element] = cost
                return True
            return False
    def pop(self):
        # removes minimum-cost element from self.elements, moves it to self.seen, and returns it
        if len(self.elements) == 0: raise KeyError #if there are no more elements
        val = min(self.elements, key=lambda x: self.elements[x]) #get the minimum by cost
        cost = self.elements[val]
        self.elements.pop(val)
        self.seen[val] = cost
        return val, cost
    def get_cost(self, key):
        # gets the cost of a key without popping it
        try:
            return self.elements[key]
        except KeyError:
            return self.seen[key]
#%%
# utility function
def dist(x1, x2):
    return np.linalg.norm(x1-x2)

#%%
def roadtrip(V, E, D, source, target):
    #init two queues to hold the costs
    days_costs = priority_queue(dict(zip(
        range(len(V)), # indices
        [np.Inf] * len(V) # distances
    )))
    distance_costs = priority_queue(dict(zip(
        range(len(V)),
        [np.Inf] * len(V)
    )))
    # set source costs
    days_costs.update(source, 0)
    distance_costs.update(source, 0)

    # actual loop to do dijkstra's
    while True:
        #get next minimum node based on days
        try:
            cur = days_costs.pop()
        except KeyError:
            break #if there are no more nodes

        for i in E[cur[0]]: # for each neighbor of cur,
            # update the days cost based on the additional distance
            days_costs.update(i, cur[1] + (dist(V[cur[0]], V[i]) + distance_costs.get_cost(cur[0]))//D)
            # and update the distance cost with the remainder distance
            distance_costs.update(i, (dist(V[cur[0]], V[i]) + distance_costs.get_cost(cur[0]))%D)
            # importantly, update() only changes the value if it is an improvement
    # return the cost and the queue (for debugging and displaying)
    return days_costs.get_cost(target), days_costs


D = 9

V, E = randGeoGraph(30, 30, 20, D)
soln, Q = roadtrip(V, E, D, 5, 8)

fig, ax = plt.subplots()
# drawGraph(V, E, ax, V[5], V[9])
drawGraphDebug(V, E, D, 5, ax, Q, V[5], V[8])


# %%
def checkPath(V,E,S,T,L):
    # if we found the target, return yes!
    if S==T: return True
    # if we reached the end of the path length, return no!
    if L<=0: return False

    # recurse for each neighbor
    for idx in E[S]:
        if checkPath(V, E, idx, T, L-1): 
            return True #if we found it, return and collapse the stack
    return False #if we didn't find it in any neighbors, return false

def iterativeDeepening(V,E,S,T,LB,UB):
    #init bounds
    lower, upper = LB, UB
    # do binary search
    while True:
        # check if we're done
        if lower+1==upper: return lower
        # do checkpath and update bounds based on it
        if checkPath(V,E,S,T,(lower+upper)//2-1):
            upper = (lower+upper)//2
        else:
            lower = (lower+upper)//2



S, T = 5, 9
V, E = randGeoGraph(50, 50, 50, 13)
# print(V.shape)
fig, ax = plt.subplots()
drawGraph(V, E, ax, V[S], V[T])
for i in range(15):
    print(i, checkPath(V,E,S,T,i))
iterativeDeepening(V,E,S,T,0,50)


# %%


