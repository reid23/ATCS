'''
Author: Reid Dye

Here are my code responses for Lab06.
'''
# here's FibDP
def fibDP(n):
    vals = (0, 1) #init, this is FibDP(0)
    for i in range(n):
        vals = vals[1], sum(vals)
    return vals[0]

#and here's the constant time version
from sympy import Matrix, pprint, MatMul
from sympy.abc import x

A = Matrix(2, 2, [0, 1, 1, 1]) # transition matrix
f = Matrix(2, 1, [1,0]) # initial value (Fib(0))
P, D = A.diagonalize()
P_inv_f = P.inv()*f
diag_expr = Matrix(1, 2, [0, 1])*P*((D**x)*P_inv_f)
#           ^^^^^^^^^^^^^^^^^^^^
#           this mat just gets the second element,
#           allowing more simplification

#here's the expression printed out:
pprint(MatMul(Matrix(1, 2, [0, 1]), P, D**x, P.inv(), f))

def fibSympy(n): return diag_expr.evalf(subs={x: n})[0]
# though very slow for small n, this function does seem 
# to be constant time, and shows very large benefits 
# over the DP solution for large n.



# Here's ExactChange. The whole thing is based around using
# integers as arrays of bits.
def exactChange(target, coins):
    # set the first row to 1 0 0 0 0 ... 0 because
    # you can always make change for 0.
    # also do <<target to set the right grid size
    # and get the 1 to the correct location
    row = 1<<target

    # loop through each row
    for coin in coins:
        # set the new row to the bitwise or (union) of the previous 
        # row (aka if you don't use this new coin, what change can 
        # you make) and the previous row bitshifted right by the 
        # coin's value (aka if you do use this new coin, what change 
        # can you make).
        # Because the "decimal place" is at the right side of our DP
        # grid, all unnecessary data for change values higher than
        # n are truncated by the bitshift.
        # the decimal place's location is set by the first line.
        row |= row >> coin

        # uncomment this to see the grid printed out
        # print('  '.join(list(bin(grid)[2:])))
    
    # now just return the farthest-right digit of the row.
    # in the first line we set the number of digits to 
    # the correct value so the ones place here dictates
    # whether we can make change for our target amount.

    # this is one of the rare times when &1 is more
    # readable than %2==0 lol
    return row&1

# here's a faster version; I guess bit shifting the other way 
# is a lot faster since you just append a zero?
# the only difference here is that the numbers are the other 
# way. The low-value digit places represent the low change values.
# this was actually the first way I implemented it, but it isn't 
# as simple and doesn't fit perfectly with the grid process I 
# explained in the responses. It also uses a lot more memory since 
# it doesn't truncate responses after target digits, but it's
# somehow still faster.
def exactChange2(n, coins):
    row = 1
    for coin in [0] + coins:
        row |= row<<coin
    return not row&1<<(n-1)
