def soln(A):
	# init our grid as [(G_{i-2}, memo), 
	#   				(G_{i-1}, memo)]
	grid = [(0, 0b0), (0, 0b0)] # memos notated 0b0 for clarity, not neccessary
	
	for idx, val in enumerate(A):
		grid = (
			grid[1], # first element of grid is second element (shift our "moving window")
			max(
				grid[1], # second is either previous second (G_{i-1})...
				(grid[0][0]+val, # or the one before that plus A_i.
				 grid[0][1]|(1<<idx)), # add the memo, (just previous memo w/ a 1 for this slot)
			    key=lambda x: x[0] # key says: compare the first element of these tuples
			) 
		)
			      
	return grid[1][0], list(map(lambda x: bool(int(x)), # convert to boolean array
								bin( # turn number into binary string representation
									grid[1][1] # the memo, as a binary number
								)[-1:1:-1] # flip around and remove '0b'
								.ljust(len(A), '0'))) # replace any missing leading zeros
print(soln([1,4,3,2,5,2,5,3,0,2,3,5]))