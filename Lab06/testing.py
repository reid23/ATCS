price = [1,2,3,2]

def solve(n, cuts, score):
    if n==0:
        return score, cuts, score
    maxval = 0
    cutlen = 0
    for i in range(1, n+1):
        c, _, _ = solve(n-i, cuts+(i+1,), score)
        c = price[c]
        if c>maxval:
            maxval = c
            cutlen = i+1
    return maxval, cuts + (cutlen,), score+maxval

# print(solve(4, (), 0))

def solve2(rod, pos):
    rod[pos] = True
    c1 = solve2(rod, pos+1)
    rod[pos] = False
    c2 = solve2(rod, pos+1)

from functools import cache, lru_cache

@cache
def exactChangeFT(n, coins):
    if n==0: return True
    if n<0: return False
    for counter, c in enumerate(coins):
        if exactChangeFT(n-c, coins[:counter] + coins[counter+1:]):
            return True
    return False
    

def exactChangeBad(n, coins):
    if n==0: return True
    if n<0: return False
    for counter, c in enumerate(coins):
        if exactChangeFT(n-c, coins[:counter] + coins[counter+1:]):
            return True
    return False

def exactChange(n, coins, cache = {}):
    exists = True
    try: return cache[(n, coins)]
    except: pass
    if n == 0: return True
    if n <  0: return False
    if len(coins)==0: return False
    for idx, coin in enumerate(coins):
        params = (n-coin, coins[:idx] + coins[idx+1:])
        cache[params] = exactChange(*params, cache)
        if cache[params]: 
            return True
    return False

from time import perf_counter_ns
def benchmark_exact_change():
    times = {'FT':[], 'custom':[]}
    for i in range(50):
        start = perf_counter_ns()
        exactChange(700+i, (1,5,5,5,5,5,5,5,5,5,5,5,5,5,5,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25))
        end = perf_counter_ns()
        times['custom'].append((end-start)/1000000)

    for i in range(50):
        start = perf_counter_ns()
        exactChangeFT(700+i, (1,5,5,5,5,5,5,5,5,5,5,5,5,5,5,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25))
        end = perf_counter_ns()
        times['FT'].append((end-start)/1000000)

    print(times)
    print(sum(times['custom'])/50)
    print(sum(times['FT'])/50)


import numpy as np
import numpy.linalg

vals, vecs = np.linalg.eig(np.array([[0,1],[1,1]]))
vals = np.diag(vals)
vecs_inv = np.linalg.inv(vecs)

def fib2(n):
    return round((vecs@(vals**n)@vecs_inv@np.array([1,0]))[0])

from sympy import Matrix, pprint
from sympy.abc import x

M = Matrix(2, 2, [0, 1, 1, 1])
f = Matrix(2, 1, [1,0])
# pprint(M)
# pprint(f)
P, D = M.diagonalize()
P_inv_f = P.inv()*f
# pprint(P_inv_f)
# pprint(D)
# pprint(D**5)
diag_expr = Matrix(1, 2, [0, 1])*P*((D**x)*P_inv_f)

def fibSympy(n):
    return diag_expr.evalf(subs={x: n})[0]

# for i in range(1_000,1_010):
#     print(fib(i))

@lru_cache(2)
def fib(n):
    if n<=1: return n
    return fib(n-2) + fib(n-1)

def fibDP(n):
    vals = (0, 1)
    for i in range(n):
        vals = vals[1], sum(vals)
    return vals[0]

times = [[], []]

for i in range(5,100_000,10_000):
    avg = 0
    for _ in range(10):
        start = perf_counter_ns()
        fibDP(i)
        end = perf_counter_ns()
        avg += (end-start)/5
    times[0].append(avg)

    avg = 0
    for _ in range(10):
        start = perf_counter_ns()
        fibSympy(i)
        end = perf_counter_ns()
        avg += (end-start)/5
    times[1].append(avg)
    print(i)



times = np.array(times)
# print(times)


import matplotlib.pyplot as plt

plt.plot(list(range(5,100_000,10_000)), times[0], label = 'fibDP')
plt.plot(list(range(5,100_000,10_000)), times[1], label = 'fibSympy')
plt.legend()
plt.title('Runtime (ns) vs. n for $fibDP(n)$ and $fibSympy(n)$')
plt.xlabel('$n$')
plt.ylabel('Runtime (ns)')
plt.show()