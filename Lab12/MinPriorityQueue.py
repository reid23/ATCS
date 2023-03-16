import numpy as  np
from math import floor
class MinPriorityQueue:
    def __init__(self, n):
        """construct a new MinPriorityQueue

        Args:
            n (int): amount of memory to allocate for this MPQ
        """
        self.A = np.full(n+1, np.Inf)
        self.len = 0 # len is our heap-size - it's the thing that changes.
        
    def insert(self, val):
        """insert val into the MinPriorityQueue

        Args:
            val (T: comparable): the value to insert

        Raises:
            IndexError: represents overflow of statically allocated memory

        Returns:
            MinPriorityQueue: self, to chain .insert() calls
        """
        # make sure we can do this
        if self.len >= len(self.A)-1: raise IndexError("Overflow Error: preallocated memory already full; cannot insert more elements.")
        
        # insert into the end
        self.A[self.len] = val
        cur = self.len
        self.len += 1

        # simplified max_heapify
        while self.A[cur]<self.A[parent := self.parent(cur)] and cur>0:
            self.A[cur], self.A[parent] = self.A[parent], self.A[cur]
            cur = parent
        
        # return self so we can do something like the 
        # builder pattern but without the builder object
        return self
    def extractMin(self):
        """pop the minimum value off this queue

        Raises:
            IndexError: represents underflow: no more elements left to extract

        Returns:
            T: comparable: type passed in
        """
        if self.len < 0: raise IndexError("Underflow Error: Heap already empty; cannot extract more elements.")

        # get value
        out = self.A[0]

        # delete from queue by setting to infinity
        # which will then get moved to back
        self.A[0] = np.Inf
        self.maxHeapifyFromRoot()

        # change len so it doesn't include that last infinity
        self.len -= 1
        return out
    
    def getMin(self): return self.A[0]
    
    
    def maxHeapifyFromRoot(self):
        """corrects errors at the root of the heap
        """
        # start at root
        cur = 0

        # while we still have space left...
        while cur < self.len:
            # current best place to move cur
            # starts at none bc we don't know if
            # we should move cur at all
            best = None

            # if cur's left child is in range...
            if (l:=self.left(cur)) < len(self.A)-1:
                # and it is better than cur...
                if self.A[l]<self.A[cur]:
                    # update best!
                    best = l
            # if cur's right child is in range...
            if (r:=self.right(cur)) < len(self.A)-1:
                # and it is better than l and cur...
                if self.A[r]<self.A[l] and self.A[r]<self.A[cur]: #have to cascade ifs so we can use r
                    # update best!
                    best = r
            # if best still hasn't changed, we're done. There's nowhere else to move cur.
            if best is None: break
            #otherwise swap best and cur
            self.A[best], self.A[cur] = self.A[cur], self.A[best]
            # then update cur bc we just moved cur
            cur = best
        
    # allow iteration with for loops
    def __iter__(self): return self
    def __next__(self):
        if self.len==0: raise StopIteration
        return self.extractMin()
    
    # allow length with len(MPQ)
    def __len__(self): return self.len

    # util methods
    def size(self): return self.len
    def left(self, idx): return 2*(idx + 1) -1
    def right(self, idx): return 2*(idx + 1)
    def parent(self, idx): return floor((idx + 1)/2 - 1)

class kLargestValues(MinPriorityQueue):
    def __init__(self, k):
        # nothing special here
        super().__init__(k)
    def insert(self, val):
        # if it's in range, just use MPQ insert
        # it's the same thing
        if self.len<len(self.A)-1:
            super().insert(val)
        else:
            # if it's not in range, we have to do
            # some funnier buisness
            # if val is not a new largest value,
            # we just return bc we shouldn't add it
            if val <= self.A[0]: return self
            # otherwise we replace A[0] with val bc
            # A[0] is the smallest one
            self.A[0] = val
            # then we move val to the correct location
            self.maxHeapifyFromRoot()

        # allows chaining .insert() calls
        return self
    
    # all other methods are the same

# testing functions
def testMPQ():
    mpq = MinPriorityQueue(10)
    (mpq.insert(10)
        .insert(9)
        .insert(8)
        .insert(12)
        .insert(15)
        .insert(13)
        .insert(7)
        .insert(11)
        .insert(2))
    for i in mpq:
        print(i)
    
def testKLV():
    klv = kLargestValues(5)
    (klv.insert(10)
        .insert(9)
        .insert(8)
        .insert(12)
        .insert(15)
        .insert(13)
        .insert(7)
        .insert(11)
        .insert(2))
    for i in klv:
        print(i)
# test!
if __name__ == '__main__':
    print("MPQ test:")
    testMPQ()
    print("KLV test:")
    testKLV()
