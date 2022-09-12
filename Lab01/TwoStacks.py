'''
Author: Reid Dye

This is my TwoStacks class.

How it works:
There is one array with constant length N, representing memory. Stack 1 is from 0 to p, with its
top at P, and stack 2 is from q to N, with its top at q.

There are two pointers (in self.ptrs) that point to the first and last free spots on the array.
When pushing an item to the stack, the item gets inserted at the location of the pointer, 
and then the pointer is incremented by one.  Stack 1's pointer is incremented up while stack 2's
pointer is incremented down.

When popping things off the stack, they are not actually deleted. The item gets returned and the 
pointer moves down by one, but the data is still there. It just gets overwritten next time 
something is pushed to the stack.

I wrote a rust version of this first, so I didn't have to think about the logic when implementing
this. As a result, it's dense. I think it's still reasonably readable, but let me know if it's not.
'''

class StackOverflowError(Exception): pass

class TwoStacks:
    def __init__(self, n):
        self.arr, self.ptrs = [None]*n, [0, n-1] #arr is storage, ptrs stores [stack_1_head_ptr, stack_2_head_ptr]
    def height(self, stack_num):
        assert stack_num in [0, 1], "Invalid argument: stack_num must be 0 or 1!" #input validation
        return self.ptrs[stack_num] if stack_num == 0 else len(self.arr)-self.ptrs[stack_num]-1 # just return the pointer (for stack from front of list) or length minus pointer (for stack from back of list)
    def push(self, stack_num, item):
        assert stack_num in [0, 1], "Invalid argument: stack_num must be 0 or 1!" #input validation
        if self.ptrs[0]>self.ptrs[1]: raise StackOverflowError("not enough space in stack to push") #check for overflow
        self.arr[self.ptrs[stack_num]] = item #add the item to the top of the stack, given by the ptr
        self.ptrs[stack_num] += [1, -1][stack_num] #move the ptr by one since we just filled its spot
    def pop(self, stack_num):
        assert stack_num in [0, 1], "Invalid argument: stack_num must be 0 or 1!" #input validation
        if self.ptrs[stack_num] == (len(self.arr)-1)*stack_num: return #return None if there's nothing to pop
        self.ptrs[stack_num] -= [1, -1][stack_num] #move the pointer down the stack by one so we can free the memory
        return self.arr[self.ptrs[stack_num]] #return the popped value
    def __str__(self): return f'Stack 1: {self.arr[:self.ptrs[0]]}\nStack 2: {self.arr[self.ptrs[1]+1:]}' #take from 0 to pointer1 for stack 1, and from pointer2 to the end for stack 2

if __name__ == '__main__':
    s = TwoStacks(3)

    print(s)

    s.push(0, 5)
    s.push(0, 6)
    s.push(0, 7)

    print(s)

    print(s.height(0))
    print(s.height(1))

    print(s.pop(0))
    print(s.pop(1))

    s.push(1, 8)
    try:
        s.push(1, 9)
    except StackOverflowError:
        pass

    print(s)
    print(s.pop(0))
    print(s.pop(1))

    for i in range(10):
        try: s.push(1, 1)
        except: break
    else:
        print('yikes')