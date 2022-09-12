'''
Author: Reid Dye

This is my MaxSubArray file.

It contains several functions to find a slice
of a given array with a maximized sum. It also
contains benchmarking and data vis tools.
'''



#%%
import random, time
import numpy as np

# Input a list (L) and the low (inclusive) and high (not inclusive) indices for the 
# array that you want to find the maximum subarray
# Output will be the left and right indices of the max subarray and the sum
def maxSubarray(L,low,high):
    # if there's only one item in the subarray then the max is it
    if low+1 == high: return low,high,L[low]

    # otherwise, divide the list in half and look for the max subarray in each side
    mid = (low + high) // 2
    leftLow,leftHigh,leftSum = maxSubarray(L,low,mid)
    rightLow,rightHigh,rightSum = maxSubarray(L,mid,high)

    # check for a max subarray that crosses the midpoint
    crossLow,crossHigh,crossSum = maxCrossingSubarray(L,low,mid,high)

    # compare the 3 sums and return the data for the max
    if leftSum >= rightSum:
        if leftSum >= crossSum: return leftLow,leftHigh,leftSum
    elif rightSum >= crossSum: return rightLow,rightHigh,rightSum
    return crossLow,crossHigh,crossSum

#%%
# i wrote this first but
# turns out its slower :(
# easier to read though
# @profile
def maxCrossingSubarray2(l, low, mid, high):
    lsum = np.cumsum(l[low:mid][::-1])[::-1]
    hsum = np.cumsum(l[mid:high])
    lo = np.argmax(lsum)
    hi = np.argmax(hsum)
    return lo+low, mid+hi, lsum[lo] + hsum[hi]


def maxCrossingSubarray(l, low, mid, high):
    #keep track of maximums and their indices, and the current total
    maxsuml, maxidxl, acc = l[mid-1], mid-1, 0
    
    # loop through mid to low, accumulating the whole time.
    # keep track of the max value of the accumulated sum
    # and the index where it occurred
    for i in range(mid-1, low-1, -1):
        acc += l[i]
        if acc > maxsuml: maxsuml, maxidxl = acc, i

    
    # now do the exact same thing, except for the upper half
    maxsumh, maxidxh, acc = l[mid], mid, 0
    for i in range(mid, high):
        acc += l[i]
        if acc > maxsumh: maxsumh, maxidxh = acc, i

    # the ends of the max crossing subarray are the 
    # places where the accumulated sum was greatest!
    # so just return those, and the sum of the max sums
    return maxidxl, maxidxh, maxsuml+maxsumh





#%%
#again here's the first one i wrote
# it's slower *and* harder to read
# rip me
def maxSubarrayBF2(L):
    sums = [np.convolve(L, v=[1]*n, mode='valid') for n in range(len(L), 0, -1)]
    maxs = list(map(max, sums)) # max val of each list (len of them)
    idx_of_slice_len = np.argmax(maxs)
    low = np.argmax(sums[idx_of_slice_len])
    high = len(L)-idx_of_slice_len
    maxsum = max(sums[idx_of_slice_len])
    return low, high, maxsum


def maxSubarrayBF(L):
    # keep track of idxs and current max
    bestidxs, maxsum = (), L[0]

    # loop through the positions of the 
    # front and back pointers, taking the 
    # sum as we go. If we hit a new max, 
    # record it, and the indices of the limits.
    for i in range(len(L)):
        acc = 0
        for j in range(i, 0, -1):
            acc += L[j]
            if acc>maxsum: bestidxs = j, i

    # finally, return the indexes and
    # sum we found while looping
    return *bestidxs, maxsum


#%%

### (c) COMMENT THIS FUNCTION THEN RUN A COUPLE TIMES TO FIND THE CROSSOVER POINT ###
def findDCCrossover():
    n = 5 #set length of list to test with
    testcases = 5000    #set number of times to test each method
    while True:  #loop, we'll break out when the efficiencies cross over
        dtBF, dtDC = 0,0 #init time sums
        for i in range(testcases): #test each one 5k times
            L = makeList(n) #make the list
            dtBF += timeBF(L)   #time the algorithms and add the
            dtDC += timeDC(L)   #times to their respective totals
        avgBF, avgDC = dtBF/testcases, dtDC/testcases #convert totals to averages

        #pretty printing
        print(f'Timing results for len(L) = {n}:')
        print(f'BF: {np.format_float_positional(avgBF)}')
        print(f'DC: {np.format_float_positional(avgDC)}')
        print()

        if avgDC < avgBF: #now compare average times
            print("DC is faster than BF when n =", n)
            break #if we crossed over, break!
        n += 1



# Divide and conquer method for solving max subarray that is same as above except
# the base case uses the brute-force strategy when the array is small enough
def maxSubarrayMod(L,low,high):
    ### (d) CHANGE YOUR BASE CASE HERE
    if high-low<28:
        return maxSubarrayBF(L[low:high])

    # otherwise, divide the list in half and look for the max subarray in each side
    mid = (low + high) // 2
    leftLow,leftHigh,leftSum = maxSubarray(L,low,mid)
    rightLow,rightHigh,rightSum = maxSubarray(L,mid,high)

    # check for a max subarray that crosses the midpoint
    crossLow,crossHigh,crossSum = maxCrossingSubarray(L,low,mid,high)

    # compare the 3 sums and return the data for the max
    if leftSum >= rightSum:
        if leftSum >= crossSum: return leftLow,leftHigh,leftSum
    elif rightSum >= crossSum: return rightLow,rightHigh,rightSum
    return crossLow,crossHigh,crossSum


### (d) ENTER THE n WHERE YOUR ORIGINAL DC BECAME FASTER THAN BF
### YOU DO NOT NEED TO COMMENT THIS FUNCTION
def findDCMCrossover():
    testcases = 10000
    count = 0
    data = []
    print("n          \tBF          \tDC          \tDCM")
    for n in range(3, 2*29):
        dtBF, dtDC, dtDCM = 0,0,0
        for i in range(testcases):
            L = makeList(n)
            dtBF += timeBF(L)
            dtDC += timeDC(L)
            dtDCM += timeDCM(L)
        avgBF, avgDC, avgDCM = dtBF/testcases, dtDC/testcases, dtDCM/testcases
        data.append([n, avgBF*1000000, avgDC*1000000, avgDCM*1000000]) # just for matplotlib
        print(f"{n}\t{np.format_float_positional(avgBF, 10)}\t{np.format_float_positional(avgDC, 10)}\t{np.format_float_positional(avgDCM, 10)}\t{np.argmin([avgBF, avgDC, avgDCM])}")
    return data


### YOU DO NOT NEED TO MODIFY ANY FUNCTION BEYOND HERE BUT IT'S A GOOD IDEA
### TO MAKE SURE YOU UNDERSTAND THEM

# returns a list of length n that contains integers in the range -20 to 20
def makeList(n):
    L = []
    for i in range(n):
        L.append(random.randint(-20,20))
    return L

# returns the time it takes the brute-force method to find the max subarray of L 
def timeBF(L):
    start = time.time()
    maxSubarrayBF(L)
    end = time.time()
    return end-start

# returns the time it takes the divide and conquer method to find the max subarray of L
def timeDC(L):
    start = time.time()
    maxSubarray(L,0,len(L))
    end = time.time()
    return end-start

# returns the time it takes the modified divide and conquer method to find the
# max subarray of L
def timeDCM(L):
    start = time.time()
    maxSubarrayMod(L,0,len(L))
    end = time.time()
    return end-start

#%%
from matplotlib import pyplot as plt
data = np.array(findDCMCrossover())
data = data.T #get columns instead of rows

#%%
if __name__ == '__main__':
    plt.plot(data[0], data[1], label='Brute Force')
    plt.plot(data[0], data[2], label='Divide and Conquer')
    plt.plot(data[0], data[3], label='Adaptive BF/DC')
    # plt.annotate('Crossover: n=28', xy=(27.5, sum(data.T[24][1:])/3 + 3),  xycoords='data',
    #         xytext=(25, 70), textcoords='data',
    #         arrowprops=dict(facecolor='black', shrink=0.05, width=2, headlength=7, headwidth=5),
    #         horizontalalignment='right', verticalalignment='top',) #turns out this is ugly
    plt.xlabel('List Length')
    plt.ylabel('Average Runtime (µs)')
    plt.title('Algorithm Runtime vs. List Length')
    plt.legend()
    plt.show()
# %%
