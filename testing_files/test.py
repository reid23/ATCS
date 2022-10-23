#%%
import numpy as np
def counting_sort(l, get_key: lambda x: x):
    vals = dict()
    for i in l:
        try:
            vals[get_key(i)].append(i)
        except:
            vals[get_key(i)] = [i]
    print(vals)
    return sum([vals[char] for char in 'abcdefghijklmnopqrstuvwxyz'], [])

def radix_sort(l): #for three-letter words
    for i in range(2, -1, -1):
        print(i)
        l=counting_sort(l, lambda x: x[i])


# l=['cow', 'dog', 'sea', 'rug', 'row', 'mob', 'box', 'tab']
# print(l)
# radix_sort(l)
# print(l)

#%%

from math import log2
from random import randint
from time import perf_counter_ns as time
from matplotlib import pyplot as plt

def binary_counting_sort(l):
    start, end = [], []
    for i in range(int(log2(max(l)))+1):
        for j in l:
            if bin(j>>i)[-1] == '0':
                start.append(j)
            else:
                end.append(j)
        l = start + end
        start, end = [], [] 
    return l

#%%
def benchmark():
    iters = 10
    list_lengths = (30, 1000)
    times = [0 for i in range(list_lengths[1]-list_lengths[0])]
    for j in range(*list_lengths):
        print(j)
        for _ in range(iters):
            l = [randint(0, 127) for _ in range(10*j)]
            start = time()
            # binary_counting_sort(l)
            l.sort()
            end = time()
            times[j-30] += ((end-start)/1000000)/iters

    plt.plot(list(range(*list_lengths)), times)
benchmark()



    

    


# %%
