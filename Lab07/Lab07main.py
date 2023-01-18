'''
Author: Reid Dye

This is my random walk file. 
'''


from random import choice
from GraphAdjList import GraphAdjList
from GraphAdjMatrix import GraphAdjMatrix

def randomWalk(graphClass, file):
    g = graphClass() #init graph

    #open the file and read all the connections
    with open(file, 'r') as f:
        for line in f.readlines():
            g.addEdge(*line[:3].split(','))
    print('Graph loaded. Paste this into a text editor which supports mermaid diagrams, or https://mermaid.live, to view the graph:')
    print(g)

    #main loop
    while True:
        # get input
        while True:
            try:
                n = input('Please enter an integer number of steps to take, or q to quit: ')
                if n=='q': 
                    print('exiting.')
                    return
                n = int(n)
            except ValueError:
                pass
            else:
                break
        # choose random starting node
        node = choice(list(g.nodes()))
        walk = str(node) #init walk log
        for _ in range(n-1): #loop through and continue walking
            node = choice(list(g.getNeighbors(node)))
            walk += f'-->{node}'
        print('random walk results:') #print results
        print(walk)

if __name__=='__main__':
    randomWalk(GraphAdjMatrix, 'Lab07Sample.graph')
    randomWalk(GraphAdjList, 'Lab07Sample.graph')
