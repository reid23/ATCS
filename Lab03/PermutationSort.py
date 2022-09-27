'''
Author: Reid Dye

Here is my implementation of Permutation Sort and
a function to benchmark it. For benchmarking, I'm
using timeit, since that does things like turning
off garbge collection and executing all the setup
before starting the timer to improve accuracy.
'''
from random import randint, random
import numpy as np
from timeit import timeit
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def permutationSort(arr):
    while True:
        # shuffle
        for i in range(len(arr)):
            randidx = randint(0, i)
            arr[i], arr[randidx] = arr[randidx], arr[i]

        # check if its sorted
        for i in range(len(arr)-1):
            if arr[i]>arr[i+1]: break
        else: #yes i know "bad practice" whatever
            return True

def benchmarkSort(n, t):
    return (timeit(
        stmt = "permutationSort(arr)",
        setup = f"arr = [random() for _ in range({n})]", 
        globals = globals(),
        number = t
    )/t)*1000 # take the average and convert to ms

def graphBenchmarks(max_len, iters = 10):
    # init
    x = list(np.arange(1, max_len+1, 1)) # vals to test at
    x_fine = list(np.arange(1, max_len+0.05, 0.05)) # smooth range of vals for plotting curve
    
    # gather all the data
    data = np.array([benchmarkSort(i, iters) for i in x])
    
    # make the model
    eval_exp = lambda t, a, b, c: a * np.exp(b * t) + c # define the exponential function
    popt, _ = curve_fit(eval_exp, x, data) # fit the model
    fitted = list(map(lambda x: eval_exp(x, *popt), x_fine)) # evaluate the model at a bunch of points for plotting
    
    #plot the things
    plt.scatter(x, data, label = 'True Average Runtime (ms)', color = 'orange') # plot actual results
    plt.plot(x_fine, fitted, label = r'$%fe^{%fx}+%f$' % (popt[0], popt[1], popt[2])) # plot model
    
    #legend, labels, then show
    plt.legend()
    plt.title('List Length vs. Average Runtime (ms)')
    plt.xlabel('List Length')
    plt.ylabel('Average Runtime (ms)')
    plt.show()
#%%

if __name__=='__main__':
    graphBenchmarks(8, 100)
# %%
