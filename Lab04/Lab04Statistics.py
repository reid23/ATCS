'''
Author: Reid Dye

This is my statistic program for Lab04
'''
#%%
# for reference
def quicksort(A, p, r):
    if p < r:
        q=partition(A, p, r)
        quicksort(A, p, q-1)
        quicksort(A, q, r)

def partition(A, p, r):
    x = A[r]
    i = p-1
    for j in range(p, r):
        if A[j]<=x:
            i+=1
            A[i], A[j] = A[j], A[i]
    A[i+1], A[r] = A[r], A[i+1]
    return i+1
# %%
def statistic(A, j, p, r):
    if j<=0 or j-1>r: #make sure its in bounds
        return None #return none if it's not in bounds

    q=partition(A, p, r) #partition around pivot

    if q==j-1: #-1 because first order statistic is 0th index
        return A[q] #if it's been found, return it
    
    # now recurse on the correct half, depending on where the pivot ended up
    if q>j-1:
        return statistic(A, j, p, q-1)
    else:
        return statistic(A, j, q-1, r)
 

l=[6,3,8,5,4,1,9]
print(l, statistic(l, 6, 0, len(l)-1))

