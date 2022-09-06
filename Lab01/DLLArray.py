'''
Author: Reid Dye

A Doubly Linked List

Words:
idx, ptr        index of a thing in "memory"
memory          the fake memory we've made with a list
prev            predecessor
next            successor
cur             current node
full head       the head of the linked list filled with data
empty head      the head of the linked list of free memory

Data is stored in 3-element blocks in memory, like this:
[prev val next | prev val next | ... ]

The last two entries are pointers to the empty and full list heads:
[... val next | free_list_head_ptr | full_list_head_ptr ]

An important note is that `freeNode` and `search` use pointers, *not list indices*. 
next() will give elements in the order they appear in the list.
'''

class DLLArray:
    def __init__(self, n):
        #        | function to flatten the list        |    init each sub-unit of the 'empty' linked list        | repeat that n times| add end bits for tracking head
        self.arr = (lambda l: [i for j in l for i in j])([[i-1 if i!=0 else None, None, i+1 if i!=(n-1) else None] for i in range(n)]) + [0, None]
        # Format: [prev, val, next, ... , emptyLLhead, fullLLhead]

        # a pointer referres to the index of the *block of 3*
        # so given int *ptr, val is arr[(ptr*3) + 1]


    # doesn't actually do anything since this dll is statically allocated
    def allocate(self): return print('Stack Overflow Error: list is full') if self.arr[-2] == None else self.arr[-2] 

    def insert(self, val):
        """Prepends `val` to the linked list. If there is no space, a failure message will be printed but no exceptions will be raised.

        Args:
            val (any): the item to add.
        """
        if self.arr[-2] == None: return print("Stack Overflow Error: list full!") # check to make sure list isn't full by making sure the empty LL has a head
        oldfullhead, self.arr[-2], self.arr[-1] = self.arr[-1], self.arr[(self.arr[-2]*3) + 2], self.arr[-2] #set empty head ptr to empty head's successor, and set full head ptr to the old empty head (where we will put val)
        self.arr[(self.arr[-1]*3):(self.arr[-1]*3)+3] = [None, val, oldfullhead] #set new val item, with ptr to previous head
        if oldfullhead!=None: self.arr[oldfullhead*3] = self.arr[-1] #connect 2nd element's backlink to head, passing if tmp is none (when previous head doesnt exist)
    
    def freeNode(self, idx: int):
        """Frees the node referred to by the pointer idx. If idx is not a valid pointer, a failure message will be printed but no exceptions will be raised.

        Args:
            idx (int): a pointer to the node to be freed
        """
        if not idx in list(map(lambda x: x[1], iter(self))): return #make sure idx is a valid pointer
        #     prev's next's idx              next's prev's idx             =  cur's next's idx   cur's prev's idx  
        self.arr[(self.arr[idx*3]*3)+2], self.arr[self.arr[(idx*3) + 2]*3] = self.arr[(idx*3)+2], self.arr[idx*3]
        #empty's head's prev's idx (or cur's prev's idx if no head)   cur's prev's idx    cur's next's idx       empty's head's idx  =    idx of cur or None if there's no empty head  None (now head)  old empty head's idx     cur's idx
        self.arr[self.arr[-2]*3 if self.arr[-2]!=None else idx*3],    self.arr[idx*3],    self.arr[(idx*3)+2],    self.arr[-2]       =       idx*3 if self.arr[-2]!=None else None,       None,         self.arr[-2],            idx

    def search(self, item):
        """seach through the list for `item`. Returns nothing if not found, but will print a message.

        Args:
            item (any): the item to search for

        Returns:
            int|NoneType: a pointer to the item in the list, or None if it is not found.
        """
        for val, idx in self:
            if val==item: return idx
        return print(f'{item} not found in list.')
    
    def delete(self, item): self.freeNode((lambda x: 0.5 if x==None else x)(self.search(item))) #sketchy error propagation: 0.5 will never be found in freeNode so it'll just return, and search already printed

    #enable looping
    def __iter__(self):
        self.i = self.arr[-1]
        return self

    def __next__(self):
        if self.i==None: raise StopIteration 
        out    = (self.arr[(self.i*3) + 1], self.i)
        self.i =  self.arr[(self.i*3) + 2]
        return out

    def __str__(self): return f"[{' '.join(map(lambda x: str(x[0]), iter(self)))}]"



a = DLLArray(5)
a.insert('first')
a.insert('second')
print(a)
print(a.allocate())
a.insert('third')
a.insert('fourth')
a.insert('fifth')
a.insert('sixth')
print(a.search('third'))
print(a)
a.delete('fourth')
print(a)