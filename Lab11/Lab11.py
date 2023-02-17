#%%
import numpy as np
#%%
def PrimMSTBad(G):
    assert (G.T == G).all(), "G must be undirected and represented as a numpy array"
    con = [0]
    non = list(range(1, len(G)))
    weights = []
    T = []
    while len(non)>0:
        print(G[con][:, non].shape)
        min_weight = np.min(G[con][:,non], where=G[con][:,non]!=0.0, initial=np.inf)
        if min_weight is np.Inf: break
        conidx, nonidx = np.where(G[con][:,non]==min_weight)
        con.append(non[nonidx[0]])
        weights.append(min_weight)
        T.append((con[conidx[0]], non.pop(nonidx[0])))
    output = list(zip(T, weights))
    print('Edge\tWeights')
    for i in output:
        print(*i, sep = '\t')
    print(f'MST weight: {sum(weights)}')
    return output

def PrimMST(G):
    # init a dict describing the distances of each node to the tree
    # dist from tree   node indices : (dist,   predecessor)
    dists = dict(zip(range(len(G)), [(np.Inf, None)]*(len(G))))

    # set start node's distance to 0 and predecessor to nothing (no pred)
    dists[0] = (0, None)
    
    # init edges, where we'll track all the edges in the set
    edges = []
    # init visited, where we'll track all the nodes we've visited so far
    visited = set() # set for O(1) membership check


    while len(visited)<len(G):
        # extract min
        u = min(dists, key = lambda x: dists[x][0]+(np.Inf if x in visited else 0))

        # add it to the tree
        visited.add(u)
        edges.append(((dists[u][1], u), G[dists[u][1], u]))

        # for each node connected to it, reduce the distance if possible.
        # if the distance was reduced, update predecessor to u as well 
        for idx, i in enumerate(G[u]):
            if idx in visited or i==0: continue
            # print(dists[idx], idx, i)
            dists[idx] = min(dists[idx], (i, u))
    
    # get rid of first edge which is bad
    edges = edges[1:]

    # pretty print everything
    print('Edge\tWeights')
    for i in edges: print(*i, sep='\t')
    print(f'MST weight: {sum([i[-1] for i in edges])}')



# %%
if __name__=='__main__':
    # declare a test graph G to represent Figure 21.1 from CLRS
    G = np.zeros((9,9))
    # a b c d e f g h i
    # 0 1 2 3 4 5 6 7 8

    # connect a
    G[0,1] = 4
    G[0,7] = 8

    # connect b
    G[1,2] = 8
    G[1,7] = 11

    # connect c
    G[2,3] = 7
    G[2,5] = 4
    G[2,8] = 2

    # connect d
    G[3,4] = 9
    G[3,5] = 14

    # connect e
    G[4,5] = 10

    # connect f
    G[5,6] = 2

    # connect g
    G[6,8] = 8
    G[6,7] = 1

    # connect h
    G[7,8] = 7

    # i has already been connected

    # make it undirected (I <3 symmetric matrices)
    G = G+G.T

    PrimMST(G)

# %%
