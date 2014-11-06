__author__ = 'Yunfei'
'''
  File: mystack.py
  Author: Steve Hubbard
  Date: August 30, 2012
  Description: This is a very simple implementation of a Stack ADT
   Based on Python lists.
'''

class MyStack:
    '''  This is a very simple implementation of a stack ADT
      based on Python lists.
    '''
    def __init__(self):
        self.data = []

    def __str__(self):
        st = 'The contents of the stack, from the top: \n'
        for x in range(len(self.data) - 1, -1, -1):
            st += str(self.data[x]) + '\n'
        return st

    def push(self, item):
        '''
          Push item onto the top of the reciever.
        '''
        self.data.append(item)

    def isEmpty(self):
        ''' Answer True if the reciever is empty.  If not,
          answer False.
        '''
        return len(self.data)== 0

    def pop(self):
        ''' If the receiver is not empty, remove and answer the
          top element of the stack.  If the stack was empty, answer
          None.
        '''
        if not self.isEmpty():
            item = self.data.pop()
            return item
        else:
            return None

    def top(self):
        ''' If the receiver is not empty, answer the top element
          of the stack.  If the stack was empty, answer
          None.  The stack is not modified.
        '''
        if not self.isEmpty(): # could be a one-liner!
            item = self.data.pop()
            self.data.append(item)
            return item
        else:
            return None

    def clear(self):
        '''
          Empty the stack.
        '''
        self.data = []

def main():
    s = MyStack()
    s.push(3)
    s.push(4)
    s.push(5)

    print( s )
    print( s.top() )
    print( s.pop() )
    print( s.pop() )
    print( s.pop() )
    print( s.pop() )

if __name__ == '__main__': main()

