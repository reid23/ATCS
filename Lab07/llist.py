'''
Author: Reid Dye

Here is my Linked List class. I don't know what this is. It's cursed. I'm never touching this again.
The problem is that I only wanted to have one class, not a node and a graph, but that means to insert at the front of the list I have to reassign self from within the function.
Little did I know, that is impossible. If only there was a language where it was easy to get low-level control and understanding without sacrificing all the high-level language features we love...

I tried to do self.__dict__ = other.__dict__; self.__class__ = other.__class__; but that didn't work, and I got stuck in a recursive loop where eval('self is self.next is self.next.next is self.next.next.next')==True.
There's a lot of problems with this code but it works enough and I don't have time to fix them :/
'''

class llist:
    def __init__(self, *vals):
        if len(vals)==0:
            self.val = None
            self.next = None
        else:
            self.val = vals[-1]
            self.next = llist(*vals[:-1])
    def insert(self, val, index = 0):
        if index<0:
            depth = 0
            cur = self
            while cur!=None:
                cur = cur.next
                depth += 1
            return self._setItem(val, depth-index)
        if not isinstance(val, llist):
            val = llist(val)
        self = self._setItem(val, index)
        return self
    def delete(self, val):
        if self == val:
            self = self.next
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
            raise ValueError(f'Value {val} not found in list.')
    def _setItem(self, node, depth):
        try:
            cur = self
            pred = None
            for _ in range(depth):
                pred = cur
                cur = cur.next
            node.next = cur
            if pred is None:
                self = node
            else:
                pred.next = node
            return self
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
    def __str__(self):
        return f'''```mermaid
graph LR;
    {'-->'.join(list(self)[::-1])};
```'''
    def __repr__(self):
        return 'llist()' + ''.join([f'.insert({repr(i)})' for i in self][::-1])
    def __eq__(self, other):
        if isinstance(other, llist):
            return self.val==other.val
        return self.val==other

if __name__ == '__main__':
    linked_list = (llist('A', 'B').insert('b')
                        .insert('c')
                        .insert('d')
                        .insert('e')
                        .delete('c')
                        .insert('c'))
    linked_list = linked_list.insert('H')
    print(linked_list)
    print(repr(linked_list))
    print(list(linked_list))