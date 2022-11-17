class llist:
    def __init__(self, *vals):
        if len(vals)==0:
            self.val = None
            self.next = None
        else:
            self.val = vals[-1]
            self.next = llist(*vals[:-1])
    def insert(self, val, index = 0):
        if not isinstance(val, llist):
            val = llist(val)
        if index<0:
            depth = 0
            cur = self
            while cur!=None:
                cur = cur.next
                depth += 1
            self._setItem(val, depth-index)
        self._setItem(val, index)
        return self
    def delete(self, val):
        if self == val:
            self.__dict__ = self.next.__dict__
            self.__class__ = self.next.__class__
            return self
        self._deleteItem(val)
        return self
    def _deleteItem(self, val):
        try:
            if self.next == val:
                self.next = self.next.next
            else:
                self.next._deleteItem(val)
        except AttributeError:
            raise KeyError(f'Value {val} not found in list.')
    def _setItem(self, node, depth):
        try:
            cur = self
            pred = None
            for _ in range(depth):
                pred = cur
                cur = cur.next
            node.next = cur
            if pred is None:
                self.__dict__ = node.__dict__
                self.__class__ = node.__class__
            else:
                pred.next = node
        except AttributeError:
            raise IndexError(f'Index {depth} out of range.')
    def __getitem__(self, index):
        if index<0:
            depth = 0
            cur = self
            while cur!=None:
                cur = cur.next
                depth += 1
            return self[depth+index]
        try:
            cur = self
            for _ in range(index):
                cur = cur.next
            return cur.val
        except AttributeError:
            raise IndexError(f'Index {index} out of range')
    def __iter__(self):
        self.cur = self
        return self
    def __next__(self):
        if self.cur == None: raise StopIteration
        out = self.cur.val
        self.cur = self.cur.next
        return out
    def __call__(self):
        return self.val
#     def __str__(self):
#         return f'''```mermaid
# graph LR;
#     {'-->'.join(list(self)[::-1])};
# ```'''
#     def __repr__(self):
#         return 'llist()' + ''.join([f'.insert({repr(i)})' for i in self][::-1])
    def __eq__(self, other):
        if isinstance(other, llist):
            return self.val==other.val
        return self.val==other

if __name__ == '__main__':
    linked_list = (llist('A', 'B').insert('b')
                        .insert('c')
                        .insert('d')
                        .insert('e')
                        .insert('c'))
    linked_list.insert('H')
    # print(linked_list)
    print(linked_list is linked_list.next is linked_list.next.next)