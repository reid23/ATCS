'''
Author: Reid Dye


'''
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
        grid |= grid >> coin

        # uncomment this to see the grid printed out
        # print('  '.join(list(bin(grid)[2:])))
    
    # now just return the farthest-right digit of grid.
    # in the first line we set the number of digits to 
    # the correct value so the ones place here dictates
    # whether we can make change for our target amount.

    # this is one of the rare times when &1 is more
    # readable than %2==0 lol
    return grid&1


def exactChange(target, coins):
	row = 1<<target
	for coin in coins: row |= row >> coin
	return row&1
    
print(exactChange(13, [1,1,5,10,25]))