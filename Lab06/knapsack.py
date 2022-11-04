import numpy as np

things = np.array([
    [3, 10],
    [1, 3],
    [2, 9],
    [2, 5],
    [1, 6]
])

def knapsackBad(things, bagSize):
    l = things.shape[0]

    # result = np.array([[j=='1' for j in bin(i)[2:].rjust(l, '0')] for i in range(2<<(l-1))])@things
    result = np.array([[(i>>j)&1 for j in range(l)] for i in range(2<<(l-1))])@things
    return max(result[:, 1][result[:, 0]<=bagSize])
    # curmax = 0
    # for i in range(2**l):
    #     result = things.T@np.array(list(bin(i)[2:].rjust(l, '0')), dtype=int, ndmin=2).T
    #     if result[1,0] > curmax and result[0,0]<=bagSize:
    #         curmax = result[1,0]
    # return curmax

def knapsack(things, bagSize):
    grid = np.zeros((things.shape[0], bagSize+1), dtype=int)
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            x = grid[i-1, j]

            if j-things[i, 0] >= 0:
                y = grid[i-1, j-things[i, 0]] + things[i, 1]
            else:
                y = 0

            grid[i, j] = max(x, y)
    return grid[-1, -1]
'''
1   2   3   4   5   6
0   0   10  10  10  10
3   3   10  13  13  13
3   9   12  12  19  22
3   9   12  14  19  22
6   9   15  18  20  25
'''
from timeit import timeit
print(knapsack(things, 6))
print(knapsackBad(things, 6))
print(timeit('knapsack(things, 6)', globals=globals(), number=10000)/10000)
print(timeit('knapsackBad(things, 6)', globals=globals(), number=10000)/10000)