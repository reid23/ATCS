'''
Author: Reid Dye

This module contains my CircDoubLinkedList class.

This was likely not the intended implementation, but it felt like the easiest option.
Here's how it works:
There are two main parts: the adj matrix and the vals list.

Vals is just a list of the items in the linked list, with pointers to the items referring to their index in the list. 
When something is inserted into the linked list, it is just prepended onto this vals list. When something is deleted, it is just deleted from this list.

Then there's the adj matrix. This is like an adjacency matrix for representing graphs. Each vector represents an index of the vals list and is all zeros except for one one.
That one's location is the index of the next element in the linked list. So if Adj_3 was E_5, then vals[3]'s successor is vals[5].
This way, the back links can be obtained by simply transposing the adj matrix, removing the need to keep track of them.

The other cool thing about this implementation is that it allows us to use all of the matrix things!
When we take the vector [0 1 2 3 4].T and dot it with a vector from adj, we get the next index, because the elements of [0 1 2 3 4] are the indices:

[0 1 2 3 4] * E_3 = 2 (E_3 is the 3rd vector of the identity matrix)

So when we multiply adj*[0 1 2 3 4].T, we get the "next" pointers in every spot:
0. [0 1 2 3 4]  #let's say we start with this
1. [1 2 3 4 0]  #after first multiplication by a simple A where each element points to the next
2. [2 3 4 0 1]  #after another multiplication by the same A
After the multiplication, we see the next element of the linked list's index in vals as the first element, then the next one after that, then the next one after that.
multiplying by A will go forward, and A.T will go backward.

Normally, to access an element of a linked list, you'd have to traverse the whole list until you get to the element you want. 
But since we can use the adj matrix to move through the list, we can factor it:

adj = P * D * P^-1, where D is diagonal.

Then powers of the matrix should be computed in O(1) time if exponentiation is O(1) (right? i don't think there'd be any extra time, but I'm not sure)

In conclusion i've been learning linear algebra and noticed after implementing the list that you could do this and got super excited and wrote this.
Initially i was using .index() to find the index of the 1s in the vectors of adj, but then i was like, hey i could dot it with [0 1 2 ... n]! And then
that opened the door to thinking about it from more of a linalg point of view.

Do people actually use this in the real world? it seems like computing the eigenvalues for such a huge matrix would take forever, but the matrix has
a ton of zeroes so maybe a sparse matrix would make that managable. Do you know?

The method I wrote based on this, CirDoubLinkedList.get(), works correctly, but that doesn't mean anything I said here was correct ;). It's a nice proof
of concept, but could still use some fixing. The symbolic version is accurate but slow, and the numeric version (uncommented) is inaccurate due to float errors.
'''
import numpy as np
from numpy.linalg import multi_dot
import sympy as sp
from scipy.linalg import eig, inv

class CircDoubLinkedList:
    def __init__(self):
        self.adj = np.array([], dtype = np.int8)
        self.vals = np.array([])
        self.n = 0
        self.fwd = True
        self.get = lambda x: None
        self._update_get()

    def _get_adj(self, ptr, dir): # gets the pointer to the successor or predecessor to ptr, based on dir
        if dir:
            return self.adj[ptr].dot([i for i in range(len(self))])
        else:
            return self.adj.T[ptr].dot([i for i in range(len(self))])


    def _update_get(self):
        if len(self) == 0:
            self.get = lambda idx: None
            return
        self.egvals, self.egvecs = eig(self.adj)
        Pinv = inv(self.egvecs)
        self.PinvV = np.dot(Pinv, np.array([i for i in range(len(self))]))
        self.get = lambda idx: self.vals[round(float(multi_dot([self.egvecs, np.diag(self.egvals**idx), self.PinvV])[0]))]


        # M = sp.Matrix(self.adj)
        # self.P, self.D = M.diagonalize() #ah hah! it exists lfg
        # self.PinvV = (self.P**-1) * sp.Matrix([i for i in range(len(self))]) #up front calculations go brrrrr!
        # self.D = np.array([self.D.row(i).col(i)[0][0] for i in self.D]).astype(np.float64)
        # self.get = lambda idx: self.vals[int(np.array((self.P*(self.D**idx)*self.PinvV).as_real_imag()[0][0]).astype(np.float64))]

    def __len__(self): return self.adj.shape[0]

    def insert(self, item):
        #process to insert:

        #start: 
        # note columns are displayed horizontally in my ascii stuff because ascii-drawing column vectors is hard

        #    0 1 2 3
        # 0 [0 1 0 0]
        # 1 [0 0 1 0]
        # 2 [0 0 0 1]
        # 3 [1 0 0 0]

        # 1. insert row of 0's between row 0 and 1. So end pointer still always points back to start (it doesn't get moved by inserting a column)
        
        #    0 1 2 3 4
        # 0 [0 0 1 0 0]
        # 1 [0 0 0 1 0]
        # 2 [0 0 0 0 1]
        # 3 [1 0 0 0 0]

        # 2. insert column E_2 before col 0, because we want the predecessor of the old first element

        #    0 1 2 3 4
        # 0 [0 1 0 0 0]
        # 1 [0 0 1 0 0]
        # 2 [0 0 0 1 0]
        # 3 [0 0 0 0 1]
        # 4 [1 0 0 0 0]

        match len(self):
            case 0: #case if there's nothing, algorithm breaks down but we can just manually do it
                self.vals = np.array([item])
                self.adj = np.array([[1]], dtype = np.int8)
            case 1: #same thing here
                self.vals = np.insert(self.vals, 0, item)
                self.adj = np.array([[0, 1], [1,0]], dtype=np.int8)
            case n: #here's the generic case
                self.vals = np.insert(self.vals, 0, item)
                idx = self._get_adj(0, True)
                self.adj = np.insert(self.adj, 1, np.zeros(n), axis = 1)
                self.adj = np.insert(self.adj, 0, np.identity(n+1)[idx], axis = 0)
        
        self._update_get() #update the getter function because we changed the contents

    def search(self, item): #just searches by looping
        for i in self: 
            if i==item: return self._get_adj(self.n, False)
        return print(f'Warning: {item} not found in list')

    def delete(self, item):
        # a = predecessor of idx
        # b = successor of idx
        # change column a to point to b
        # delete row idx
        # delete column idx

        self.change_iter_dir(True)

        idx = self.search(item)
        if idx == None: return
        predecessor = self._get_adj(idx, False)
        successor = self._get_adj(idx, True)

        self.vals = np.delete(self.vals, idx)

        self.adj[predecessor] = np.identity(len(self))[successor]

        self.adj = np.delete(self.adj, idx, axis=0)
        self.adj = np.delete(self.adj, idx, axis=1)
        self._update_get()

    def change_iter_dir(self, fwd = None): 
        self.fwd = (bool(fwd) and (not fwd==None)) ^ ((not self.fwd) and fwd==None) #set self.fwd to fwd if it is given, else toggle self.fwd

    # enable looping
    def __iter__(self):
        self.stop = 0 #stop iteration flag
        self.n = 0 if self.fwd else self._get_adj(self.n, False) #set start idx to be either head or tail
        return self
    def __next__(self):
        if len(self)==0: raise StopIteration #if there's nothing, don't even start iterating
        if self.stop == -1: raise StopIteration #this is the flag condition
        if self.stop == -2: self.stop = -1 #by setting stop to -2 initially, we can get an extra loop when going backwards (which is neccessary because :sparkles: off by one errors! :sparkles: Yay!)
        out = self.vals[self.n] #set the return value for this loop
        self.n = self._get_adj(self.n, self.fwd) #update n so we can check before next time
        if self.n == 0: self.stop = -1 if self.fwd else -2 # set the stop flag if needed
        return out

    def __str__(self): return f'[{" ".join([str(i) for i in self])}]' #use iteration to get all the values in order

if __name__ == '__main__':
    # testing!
    c = CircDoubLinkedList() #test init
    print(c) # test __str__ with nothing in it
    c.insert(1) # these four test adding stuff to the list
    c.insert(2)
    c.insert(3)
    c.insert(4)
    print(c) # now test __str__ with actual things in the list
    c.delete(3) #test delete
    print(c) #see whether delete did anything
    c.delete(3) #test delete when the thing doesn't exist
    print(c) #see whether delete did anything
    
    #this next part tries to delete everything in the list and see what happens
    c.delete(1) #also this tests deleting the last element which might be tricky
    print(c)
    c.delete(2)
    print(c)
    c.delete(4) #and deleting the final one
    print(c)

    c.delete(10) #try deleting when the entire list is empty
    print(c)

    c.delete(1) #same thing again
    print(c)

    c.insert(10) #test inserting again after deleting everything
    c.insert(15)
    c.insert(20)

    print(c)

    for i in range(10): print(c.get(i)) #test the get() method (slow)



#    1 2 3 4
# 1 [0 1 0 0]
# 2 [0 0 1 0]
# 3 [0 0 0 1]
# 4 [1 0 0 0]


# to insert

# 1. insert column between 1 and 2

#    1 2 3 4 5
# 1 [0 0 1 0 0]
# 2 [0 0 0 1 0]
# 3 [0 0 0 0 1]
# 4 [1 0 0 0 0]

# 2. insert row before 1, [0 1 0 ... 0], 1 is in idx of previous head

#    1 2 3 4 5
# 1 [0 1 0 0 0]
# 2 [0 0 1 0 0]
# 3 [0 0 0 1 0]
# 4 [0 0 0 0 1]
# 5 [1 0 0 0 0]