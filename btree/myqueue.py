__author__ = 'Yunfei'
class MyQueue:
    def __init__(self):
        self.data = []

    def __str__(self):
        st = 'The contents of the queue, from the front: \n'
        for x in range(len(self.data)):
            st += str(self.data[x]) + '\n'
        return st

    def enqueue(self, item):
        self.data.append(item)

    def isEmpty(self):
        return len(self.data)== 0

    def dequeue(self):
        if not self.isEmpty():
            item = self.data[0]
            self.data = self.data[1:]
            return item
        else:
            print( 'Error.  Empty queue in dequeue().' )
            return None

    def clear(self):
        self.data = []


def main():
    s = MyQueue()
    s.enqueue(3)
    s.enqueue(4)
    s.enqueue(5)

    print( s )
    print( s.dequeue() )
    print( s.dequeue() )
    print( s.dequeue() )
    print( s.dequeue() )
if __name__ == '__main__': main()




