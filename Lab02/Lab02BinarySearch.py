'''
Author: Reid Dye

This is my Binary Search implementation!

It's really simple. As simple as possible.
'''
def binarySearch(L,low,high,target):
    # base case: if we search the whole thing and find nothing
    if low>high: return -1

    # other base case: if we only have 1 item left
    if low==high: return low if L[low]==target else -1

    # get middle value in sorted list
    mid = (high + low) // 2
    n = L[mid]

    # refine the search to the upper or lower
    # half based on comparing the target with 
    # the middle value
    if target > n: return binarySearch(L, mid+1, high, target)
    if target < n: return binarySearch(L, low, mid, target)

    # if we found the target, just return the index
    if target == n: return mid