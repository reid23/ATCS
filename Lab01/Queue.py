'''
Author: Reid Dye

This is my Queue class. It's so tiny! how adorable

How it works:
There's a TwoStacks object with capacity N+1, where n is the queue's capacity. To enqueue, everything is popped from the first stack and pushed to the second stack. Then the item is pushed to the first stack, followed by everything else from the second stack. This results in the new element being at the bottom of the stack, just like it would be in a queue!
To dequeue, you just pop the top item off the first stack.

I wrote a rust version of this first, which is why it's so dense - was only thinking about the syntax and typing while I wrote it, not the acutal logic
'''
from TwoStacks import *
class Queue:
    def __init__(self, n): self.stack, self.capacity = TwoStacks(n+1), n
    def length(self): return self.stack.height(0) #length is just height on its side ;) all the stuff is in stack 0 so it's just the height of stack 0
    def enqueue(self, item):
        if self.length()>=self.capacity: raise StackOverflowError("Not enough capacity in Queue") #input validation
        for _ in range(self.length()): self.stack.push(1, self.stack.pop(0)) #move from stack 0 to stack 1 by popping and pushing
        for i in range(self.stack.height(1)+1): self.stack.push(0, item if i==0 else self.stack.pop(1)) #pop and push everything back, but push item first so it goes to the bottom of the stack
    def dequeue(self): return self.stack.pop(0) #just take the top element from the stack to dequeue
    def __str__(self): return str(self.stack)[9:].split(sep = '\n')[0] # __str__ is just the same as the stack, but removing the "Stack 1: " label, and removing the stuff from stack 2

#END OF CODE


#testing
if __name__ == '__main__':
    q = Queue(2)            #test initialization
    print(q)                #test printing an empty queue
    q.enqueue(1)            #test adding first thing to queue
    q.enqueue(2)            #test adding subsequent things
    print(q)                #test printing a non-empty queue
    try: q.enqueue(1)       #test overflow error
    except StackOverflowError: pass
    print(q)                #test printing after error, and make sure it didn't add the 1
    assert q.dequeue()==1   #test dequeueing
    print(q)                #check that dequeuing did something
    q.dequeue()
    assert q.dequeue()==None#test underflow
    print(q)                #test printing after that


# in the interest of obfuscation and joy, here's the entire class in one line
class Queue2: 
    def __init__(self, n): self.stack, self.capacity, self.length, self.enqueue, self.dequeue, self.__str__ = TwoStacks(n+1), n, lambda: self.stack.height(0), lambda item: (lambda x, err: None if not err else ().throw(StackOverflowError("Not enough capacity in Queue")))([self.stack.push(int(i<self.stack.height(0)+self.stack.height(1)), item if self.stack.height(0)==0 else self.stack.pop(int(i>=self.stack.height(0)+self.stack.height(1)))) for i in range(self.length()*2 + 1)], not self.length()>=self.capacity), lambda: self.stack.pop(0), lambda: str(self.stack[9:].split('\n')[0])
