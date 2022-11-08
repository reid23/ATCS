'''
Author: Reid Dye


'''
def exactChange(n, coins):
    # start grid as 1 0 0 0 0 ... 0 because you can always make change for 0
    grid = 1<<n

    # loop through each row
    for coin in coins:
        # set grid to the union ("|" is bitwise or) of the current 
        # grid (everything that worked without this row's coin) and 
        # the current grid bitshifted right by the coin's value 
        # (everything that would work if you took the previous 
        # row's things and added this new coin)
        # Because the "decimal place" is at the right side of our DP
        # grid, all unnecessary data for change values higher than
        # n are truncated by the bitshift.
        grid |= grid >> coin
        print('  '.join(list(bin(grid)[2:])))
    
    # now just return the farthest-right digit of grid.
    # this is one of the rare times when &1 is more
    # readable than %2==0 lol
    return grid&1

print(exactChange(13, [1,1,5,10,25]))