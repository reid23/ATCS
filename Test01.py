'''
Author: Reid Dye

This is my recursive O(lg n) 2**n fuction.

The way it works is by dividing and conquering. The way to get a
stack height of max lg n + 1 is to break it down into lg n levels,
so each recursion has two sequential calls to exp.

Each time, it does exp(n/2)*exp(n/2), and when n is 1, it returns 2.
This way we still end up multiplying 2 n times, but we keep
the stack height low.

There's also some logic to help it when it encounters odd numbers.
'''

from math import log2

def exp(n):
    # print('here') #uncomment to check stack height
    if n==0: return 1 # in case the user wants to do this???
    if n==1: return 2
    # print('end of run') #uncomment to check stack height
    if n%2==0:
        return exp(n/2)*exp(n/2)
    return exp(n//2)*exp((n//2)+1)
'''
demo for n=6:
         6
      3     3
     1 2   1 2
      1 1   1 1
there are 6 ones
'''