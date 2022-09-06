class DLLArray:
    def __init__(self, n): self.arr = (lambda l: [i for j in l for i in j])([[i-1 if i!=0 else None, None, i+1 if i!=(n-1) else None] for i in range(n)]) + [0, None]
    def allocate(self): return print('Stack Overflow Error: list is full') if self.arr[-2] == None else self.arr[-2] 
    def insert(self, val):
        if self.arr[-2] == None: return print("Stack Overflow Error: list full!")
        oldfullhead, self.arr[-2], self.arr[-1] = self.arr[-1], self.arr[(self.arr[-2]*3) + 2], self.arr[-2]
        self.arr[(self.arr[-1]*3):(self.arr[-1]*3)+3] = [None, val, oldfullhead]
        if oldfullhead!=None: self.arr[oldfullhead*3] = self.arr[-1]
    def freeNode(self, idx: int):
        if not idx in list(map(lambda x: x[1], iter(self))): return
        self.arr[(self.arr[idx*3]*3)+2], self.arr[self.arr[(idx*3) + 2]*3] = self.arr[(idx*3)+2], self.arr[idx*3]
        self.arr[self.arr[-2]*3 if self.arr[-2]!=None else idx*3], self.arr[idx*3], self.arr[(idx*3)+2], self.arr[-2] = idx*3 if self.arr[-2]!=None else None, None, self.arr[-2], idx
    def search(self, item):
        for val, idx in self: 
            if val==item: return idx
        return print(f'{item} not found in list.')
    def delete(self, item): self.freeNode((lambda x: 0.5 if x==None else x)(self.search(item)))
    def __iter__(self):
        self.i = self.arr[-1]
        return self
    def __next__(self):
        if self.i==None: raise StopIteration 
        out    = (self.arr[(self.i*3) + 1], self.i)
        self.i =  self.arr[(self.i*3) + 2]
        return out
    def __str__(self): return f"[{' '.join(map(lambda x: str(x[0]), iter(self)))}]"


if __name__ == '__main__':
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