import numpy as  np
from math import floor
class MinPriorityQueue:
    def __init__(self, n):
        self.A = np.full(n+1, np.Inf)
        self.len = 0
        
    def insert(self, val):
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
        if self.len < 0: raise IndexError("Underflow Error: Heap already empty; cannot extract more elements.")

        out = self.A[0]
        self.A[0] = np.Inf

        self.maxHeapifyFromRoot()

        self.len -= 1
        return out
    
    def getMin(self): return self.A[0]
        
    def maxHeapifyFromRoot(self):
        cur = 0
        while cur < self.len:
            # print(self.A, cur)
            best = None
            if (l:=self.left(cur)) < len(self.A)-1:
                if self.A[l]<self.A[cur]:
                    best = l
            if (r:=self.right(cur)) < len(self.A)-1:
                if self.A[r]<self.A[l] and self.A[r]<self.A[cur]: #have to cascade ifs so we can use r
                    best = r
            if best is None: break
            self.A[best], self.A[cur] = self.A[cur], self.A[best]
            cur = best
        

    def __iter__(self): return self
    def __next__(self):
        if self.len==0: raise StopIteration
        return self.extractMin()
    
    def __len__(self): return self.len
    def size(self): return self.len
    def left(self, idx): return 2*(idx + 1) -1
    def right(self, idx): return 2*(idx + 1)
    def parent(self, idx): return floor((idx + 1)/2 - 1)

class kLargestValues(MinPriorityQueue):
    def __init__(self, k, vals=[]):
        super().__init__(k)
    def insert(self, val):
        if self.len<len(self.A)-1:
            super().insert(val)
        else:
            if val <= self.A[0]: return self
            self.A[0] = val
            self.maxHeapifyFromRoot()
        return self


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

if __name__ == '__main__':
    testMPQ()
    testKLV()
