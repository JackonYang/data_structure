'''
  File: btree.shell   -- save as btree.py
  Author(s): 
  Date: 
  Description: 
'''

from mystack import MyStack
from myqueue import MyQueue
#from person import Person
from copy import deepcopy
import sys

class BTreeNode:
    '''
      This module provides the BTreeNode class.  This class will
      be used by the BTree class.  Much of the functionality of
      BTrees is provided by this class.
    '''
    def __init__(self, degree = 1):
        ''' Create an empty node with the indicated degree.'''
        self.numberOfKeys = 0
        self.items = [None]*2*degree
        self.child = [None]*(2*degree+1)
        self.index = None

    def __str__(self):
        st = 'The contents of the node with index '+ \
             str(self.index) + ':\n'
        for i in range(0, self.numberOfKeys):
            st += '   Index   ' + str(i) + '  >  child: '
            st += str(self.child[i])
            st += '   item: '
            st += str(self.items[i]) + '\n'
        st += '                 child: '
        st += str(self.child[self.numberOfKeys]) + '\n'
        return st

    def addItemAndSplit(self, anItem, left, right):
        ''' 
          If the receiver is not full, generate an error.
          If full, split the receiver into two nodes, the
          smallest degree + 1 keys staying in the original node.
          The largest degree keys go into a new node which is
          returned. Note that the last child of the receiver
          and the first child of the new node will be the same.
        '''
        if not self.isFull():
            print( 'Error in addItemAndSplit' )
            return None

        degree = len(self.items) / 2

        n = BTreeNode(degree)
        n.copyItemsAndChildren(self, degree+1, self.numberOfKeys, None)
        n.insertItem(anItem, left, right)
        self.setNumberOfKeys(degree+1)
        return n

    def childIndexOf(self, anIndex):
        '''  Answer the index of the child, in the receiver,
          which contains anIndex.  Print an error message if
          there is no such child in the receiver.
        '''
        index = -1
        found = False
        k = 0
        while not found and k <= self.numberOfKeys:
            if self.child[k] == anIndex:
                found = True
                index = k
            else:
                k += 1
        if index < 0:
            print( 'Error in childIndexOf' )
        return index

    def clear(self):
        self.numberOfKeys = 0
        self.items = [None]*len(self.items)
        self.child = [None]*len(self.child)
    
    def copyItemsAndChildren(self, fromNode, start, finish, index):
        ''' The receiver, self, gets the contents of the fromNode, from
          index start to finish, along with the next child.  The
          copying within the receiver begins at position index.
        '''
        for i in range(start, finish):
            self.items[i-start] = fromNode.items[i]
            self.child[i-start] = fromNode.child[i]

        self.child[finish-start] = fromNode.child[finish]
        self.numberOfKeys = finish - start
        self.index = index

    def extendItemsAndChildren(self, fromNode, start, delta, copyChild=True):
        for i in range(delta):
            self.items[self.getNumberOfKeys()+i] = fromNode.items[start+i]
        if copyChild:
            for i in range(delta+1):
                self.child[self.getNumberOfKeys()+i] = fromNode.child[start+i]

        self.numberOfKeys += delta
    
    def copyWithRight(self, aNode, parentNode):  
        '''Answer a node which contains all the items and children
          of the receiver, followed by the parent item followed by
          all the items and children of aNode.  The receiver and
          aNode are left and right siblings with respect to an
          item within the parentNode.
        '''
        degree = (self.getNumberOfKeys() + aNode.getNumberOfKeys() + 2) / 2

        n = BTreeNode(degree)
        n.copyItemsAndChildren(self, 0, self.getNumberOfKeys(), None)
        n.extendItemsAndChildren(parentNode, 0, 1, False)
        n.extendItemsAndChildren(aNode, 0, aNode.getNumberOfKeys(), True)
        return n

    def insertItem(self, anItem, left = None, right = None):  
        ''' We assume that the receiver is not full. anItem is
          inserted into the receiver with child indices left and
          right.  This is done while retaining the <= ordering on
          the key of the item.  If the insertion is successful,
          answer True.  If not, answer False.
        '''
        if self.isFull():
            return False

        self.items[self.numberOfKeys] = anItem
        self.numberOfKeys += 1
        self.items = sorted(self.items[:self.numberOfKeys]) + self.items[self.numberOfKeys:]
        return True

    def isFull(self):
        ''' Answer True if the receiver is full.  If not, return
          False.
        '''
        return (self.numberOfKeys == len(self.items))

    def removeChild(self, index):
        ''' If index is valid, remove and answer the child at
          location index.  If not, answer None.  In any event,
          do NOT update the key count.  We copy all the rest of
          the child entries towards the start one position.
          The method removeItem will decrement numberOfKeys.
        '''
        pass

    def removeItem(self, index):
        ''' If index is valid, remove and answer the item at
          location index.  Move the rest of the items to fill the
          gap.  Update the key count.  If the index is not valid,
          answer None.
        '''
        pass

    def searchNode(self, anItem):
        '''Answer a dictionary satisfying: at 'found'
          either True or False depending upon whether the receiver
          has a matching item;  at 'nodeIndex', either the index of
          the matching item, or in the case of an unsuccessful
          search, the index of the smallest (first) item such that
          anItem < item, or self.numberOfKeys if all items
          are < anItem.  In other words, nodeIndex is the place in the node
          where the object is, or should go if there is room in the node.
        '''
        import bisect
        poistion = bisect.bisect_left(self.items, anItem)
        found = poistion < len(self.items) and anItem == self.items[poistion]
        return {'nodeIndex': poistion, 'found': found}

    def setIndex(self, anInteger):
        self.index = anInteger

    def setNumberOfKeys(self, anInt ):
        self.numberOfKeys = anInt
    
    def getNumberOfKeys(self):
        return self.numberOfKeys

class BTree:
    '''  Comment about the class BTree!!
    '''
    def __init__(self, degree):
        # This method is complete.
        self.degree = degree
        self.rootNode = BTreeNode(degree)
        
        # If time, file creation code, etc.
        self.nodes = {}  # A dictionary
        self.stackOfNodes = MyStack()
        self.rootNode.setIndex(1)
        self.writeAt(1, self.rootNode)
        self.rootIndex = 1
        self.freeIndex = 2

    def __str__(self):
        # This method is complete.
        st = '  The degree of the BTree is ' + str(self.degree)+\
             '.\n'
        st += '  The index of the root node is ' + \
              str(self.rootIndex) + '.\n'
        for x in range(1, self.freeIndex):
            node = self.readFrom(x)
            if node.getNumberOfKeys() > 0:
                st += str(node) 
        return st

    def delete(self, anItem):
        ''' Answer None if a matching item is not found.  If found,
          answer the entire item.  
        '''
        pass  

    def inorderOn(self, aFile):
        '''
          Print the items of the BTree in inorder on the file 
          aFile.  aFile is open for writing.
          This method is complete at this time.
        '''
        aFile.write("An inorder traversal of the BTree:\n")
        self.inorderOnFrom( aFile, self.rootIndex)

    def inorderOnFrom(self, aFile, index):
        ''' Print the items of the subtree of the BTree, which is
          rooted at index, in inorder on aFile.
        '''
        pass

    def isRoot(self, idx):
        return self.rootIndex == idx

    def addInRoot(self, anItem):
        if not self.rootNode.isFull():
            self.rootNode.insertItem(anItem)
        else:
            print 'root full'

    def insert(self, anItem):
        ''' Answer None if the BTree already contains a matching
          item. If not, insert a deep copy of anItem and answer
          anItem.
        '''
        position = self.searchTree(anItem)
        if position['found']:
            return None
        if self.isRoot(position['nodeIndex']):
            return self.rootNode
        
    def levelByLevel(self, aFile):
        ''' Print the nodes of the BTree level-by-level on aFile.
        '''
        pass

    def readFrom(self, index):
        ''' Answer the node at entry index of the btree structure.
          Later adapt to files.  This method is complete at this time.
        '''
        if self.nodes.__contains__(index):
            return self.nodes[index]
        else:
            return None

    def recycle(self, aNode):
        # For now, do nothing
        # This method is complete at this time.
        aNode.clear()

    def retrieve(self, anItem):
        ''' If found, answer a deep copy of the matching item.
          If not found, answer None
        '''
        pass

    def searchTree(self, anItem):
        ''' Answer a dictionary.  If there is a matching item, at
          'found' is True, at 'fileIndex' is the index of the node
          in the BTree with the matching item, and at 'nodeIndex'
          is the index into the node of the matching item.  If not,
          at 'found' is False, but the entry for 'fileIndex' is the
          leaf node where the search terminated.  An important
          function of this method is that it pushes all of the
          nodes of the search path from the rootnode, down to,
          but not including the corresponding leaf node of a search
          (or the node containing a match).  Again, the rootnode
          is pushed if it is not a leaf node and has no match.
        '''
        cur_node = self.readFrom(self.rootIndex)
        status = cur_node.searchNode(anItem)
        if status['found']:
            status['fileIndex'] = cur_node.index
            return status
        while cur_node.index is not None:
            cur_node = self.readFrom(cur_node.child[status['nodeIndex']])
            if cur_node is None:
                return status
            status = cur_node.searchNode(anItem)
            if status['found']:
                break
        status['fileIndex'] = cur_node.index
        return status


    def update(self, anItem):
        ''' If found, update the item with a matching key to be a
          deep copy of anItem and answer anItem.  If not, answer None.
        '''
        pass
    

    def writeAt(self, index, aNode):
        ''' Set the element in the btree with the given index
          to aNode.  This method must be invoked to make any
          permanent changes to the btree.  We may later change
          this method to work with files.
          This method is complete at this time.
        '''
        self.nodes[index] = aNode

def main():
    print('Our names are ')
    
    print("Test the BTreeNode class:")
    
    # Poor style using instance variables directly!
    # Makes for easier testing, though!!
    n = BTreeNode(2)
    n.items[0:4] = [15,20,30,35]
    n.child[0:5] = [1,2,3,4,5]
    n.numberOfKeys = 4
    n.index = 11
    print( "Run 1" )
    print( n.searchNode(30))
    print( n.searchNode(10) )
    print( n.searchNode(31) )
    print( n.searchNode(40) )
    print( '' )

    
    b = BTreeNode(3)
    b.index = 133
    b.insertItem(500,19,21) # Child indices do NOT make sense!
    b.insertItem(150,31,43)
    b.insertItem(200,50,62)
    b.insertItem(700,70,18)
    b.insertItem(100,19,10)
    b.insertItem(300,11,12)    
    print( "Run 2" )
    print( b )


    n = BTreeNode(1)
    n.index = 12
    n.insertItem(50,3,34)
    n.insertItem(100, 34, 37)
    print( "Run 3" )
    print( n.searchNode(100) )
    print( n.searchNode(31) )
    print( n.searchNode(90) )
    print( n.searchNode(150) )
    print( '' )
    
    n = BTreeNode(2)
    n.items[0:4] = [15,20,30,35]
    n.child[0:5] = [1,2,3,4,5]
    n.numberOfKeys = 4
    n.index = 10
    print( "Run 4" )
    print( n )
    print( n.addItemAndSplit(32,4,13) )# Try adding 10, 36, ... 
    print( n )

    
    # This next part is useful for deletion
    n = BTreeNode(4)
    n.items[0:8] = [15,20,30,35,None,None,None,None]
    n.child[0:9] = [1,2,3,4,5,None,None,None,None]
    n.numberOfKeys = 4
    n.index = 6

    p = BTreeNode(4)
    p.items[0:8] = [40,50,60,70,None,None,None,None]
    p.child[0:9] = [6,7,8,9,10,None,None,None,None]
    p.setNumberOfKeys(4)
    p.setIndex(17)

    m = BTreeNode(4)
    m.items[0:8] = [41,42,43,44,None,None,None,None]
    m.child[0:9] = [11,12,13,14,15,None,None,None,None]
    m.setNumberOfKeys(4)
    m.setIndex(7)
    print( "Run 5" )
    print( m )


    new = n.copyWithRight(m,p) 
    print( "Run 6" )
    print( new )

    
    print('Test the BTree class:')
    
    print( ' # run #1 -------------------------------' )
    bt = BTree(1)
    bt.insert(50)
    bt.insert(27)
    bt.insert(35)
    print( bt )

    return

    bt.insert(98)
    bt.insert(201)
    print( bt )

    bt.insert(73)
    bt.insert(29)
    bt.insert(150)
    bt.insert(15)
    print( bt )

    bt.insert(64)
    print( bt )

    bt.insert(83)
    bt.insert(90)
    print( bt )

    bt.insert(87)
    bt.insert(253)
    print( bt )

    bt.insert(84)
    print( bt )
    
    
    print( ' # run #2 -------------------------------' )
    t = BTree(1)
    # t.insert(Person('Joe', 38))
    # t.insert(Person('Susie',48))
    # t.insert(Person('Billy',39))
    # t.insert(Person('Tomas',12))
    # t.insert(Person('Don',35))
    # t.update(Person('Willy', 12))
    # print( t.retrieve(Person('', 48)) )
    # print( t )

    # t.levelByLevel(sys.stdout)
    # t.inorderOn(sys.stdout)
    # t.delete(Person('',35))
    # t.inorderOn(sys.stdout)
    

    print( ' # run#3 -------------------------------' )
    bt = BTree(2)
    bt.insert(20)
    bt.insert(40)
    bt.insert(10)
    bt.insert(30)
    bt.insert(15)
    bt.insert(35)
    bt.insert(7)
    bt.insert(26)
    bt.insert(18)
    bt.insert(22)
    bt.insert(5)
    bt.insert(42)
    bt.insert(13)
    bt.insert(46)
    bt.insert(27)
    bt.insert(8)
    bt.insert(32)
    bt.insert(38)
    bt.insert(24)
    bt.insert(45)
    bt.insert(25)
    print( bt )
    
    
    print( ' # run#4 -------------------------------' )
    bt = BTree(2)
    bt.insert(20)
    bt.insert(40)
    bt.insert(10)
    bt.insert(30)
    bt.insert(15)
    bt.insert(35)
    bt.insert(7)
    bt.insert(26)
    bt.insert(18)
    bt.insert(22)
    bt.insert(5)
    bt.insert(42)
    bt.insert(13)
    bt.insert(46)
    bt.insert(27)
    bt.insert(8)
    bt.insert(32)
    bt.insert(38)
    bt.insert(24)
    bt.insert(45)
    bt.insert(25)
    bt.delete(35)
    bt.delete(38)
    bt.delete(25)
    bt.delete(38)
    print( bt )

    print( ' #run #5 -------------------------------' )
    bt = BTree(1)
    bt.insert(27)
    bt.insert(50)
    bt.insert(35)
    bt.insert(29)
    bt.insert(150)
    bt.insert(98)
    bt.insert(73)
    bt.insert(201)
    print( bt )
    bt.delete(35)
    bt.delete(98)
    bt.delete(29)
    bt.delete(73)
    bt.delete(50)
    bt.delete(150)
    bt.delete(12)
    bt.delete(98)
    print( bt )
    


if __name__ == '__main__': main()

''' The output:
[evaluate btree.py]
My/Our name(s) is/are :
Test the BTreeNode class:
Run 1
{'nodeIndex': 2, 'found': True}
{'nodeIndex': 0, 'found': False}
{'nodeIndex': 3, 'found': False}
{'nodeIndex': 4, 'found': False}

Run 2
The contents of the node with index 133:
   Index   0  >  child: 19   item: 100
   Index   1  >  child: 10   item: 150
   Index   2  >  child: 50   item: 200
   Index   3  >  child: 11   item: 300
   Index   4  >  child: 12   item: 500
   Index   5  >  child: 70   item: 700
                 child: 18

Run 3
{'nodeIndex': 1, 'found': True}
{'nodeIndex': 0, 'found': False}
{'nodeIndex': 1, 'found': False}
{'nodeIndex': 2, 'found': False}

Run 4
The contents of the node with index 10:
   Index   0  >  child: 1   item: 15
   Index   1  >  child: 2   item: 20
   Index   2  >  child: 3   item: 30
   Index   3  >  child: 4   item: 35
                 child: 5

The contents of the node with index None:
   Index   0  >  child: 4   item: 32
   Index   1  >  child: 13   item: 35
                 child: 5

The contents of the node with index 10:
   Index   0  >  child: 1   item: 15
   Index   1  >  child: 2   item: 20
   Index   2  >  child: 3   item: 30
                 child: 4

Run 5
The contents of the node with index 7:
   Index   0  >  child: 11   item: 41
   Index   1  >  child: 12   item: 42
   Index   2  >  child: 13   item: 43
   Index   3  >  child: 14   item: 44
                 child: 15

Run 6
The contents of the node with index None:
   Index   0  >  child: 1   item: 15
   Index   1  >  child: 2   item: 20
   Index   2  >  child: 3   item: 30
   Index   3  >  child: 4   item: 35
   Index   4  >  child: 5   item: 40
   Index   5  >  child: 11   item: 41
   Index   6  >  child: 12   item: 42
   Index   7  >  child: 13   item: 43
   Index   8  >  child: 14   item: 44
                 child: 15

Test the BTree class:
 # run #1 -------------------------------
  The degree of the BTree is 1.
  The index of the root node is 3.
The contents of the node with index 1:
   Index   0  >  child: None   item: 27
                 child: None
The contents of the node with index 2:
   Index   0  >  child: None   item: 50
                 child: None
The contents of the node with index 3:
   Index   0  >  child: 1   item: 35
                 child: 2

  The degree of the BTree is 1.
  The index of the root node is 3.
The contents of the node with index 1:
   Index   0  >  child: None   item: 27
                 child: None
The contents of the node with index 2:
   Index   0  >  child: None   item: 50
                 child: None
The contents of the node with index 3:
   Index   0  >  child: 1   item: 35
   Index   1  >  child: 2   item: 98
                 child: 4
The contents of the node with index 4:
   Index   0  >  child: None   item: 201
                 child: None

 # run #1 A -------------------------------
  The degree of the BTree is 1.
  The index of the root node is 7.
The contents of the node with index 1:
   Index   0  >  child: None   item: 15
                 child: None
The contents of the node with index 2:
   Index   0  >  child: None   item: 50
   Index   1  >  child: None   item: 73
                 child: None
The contents of the node with index 3:
   Index   0  >  child: 1   item: 27
                 child: 5
The contents of the node with index 4:
   Index   0  >  child: None   item: 150
   Index   1  >  child: None   item: 201
                 child: None
The contents of the node with index 5:
   Index   0  >  child: None   item: 29
                 child: None
The contents of the node with index 6:
   Index   0  >  child: 2   item: 98
                 child: 4
The contents of the node with index 7:
   Index   0  >  child: 3   item: 35
                 child: 6

  The degree of the BTree is 1.
  The index of the root node is 7.
The contents of the node with index 1:
   Index   0  >  child: None   item: 15
                 child: None
The contents of the node with index 2:
   Index   0  >  child: None   item: 50
                 child: None
The contents of the node with index 3:
   Index   0  >  child: 1   item: 27
                 child: 5
The contents of the node with index 4:
   Index   0  >  child: None   item: 150
   Index   1  >  child: None   item: 201
                 child: None
The contents of the node with index 5:
   Index   0  >  child: None   item: 29
                 child: None
The contents of the node with index 6:
   Index   0  >  child: 2   item: 64
   Index   1  >  child: 8   item: 98
                 child: 4
The contents of the node with index 7:
   Index   0  >  child: 3   item: 35
                 child: 6
The contents of the node with index 8:
   Index   0  >  child: None   item: 73
                 child: None

 # run #1 B -------------------------------
  The degree of the BTree is 1.
  The index of the root node is 7.
The contents of the node with index 1:
   Index   0  >  child: None   item: 15
                 child: None
The contents of the node with index 2:
   Index   0  >  child: None   item: 50
                 child: None
The contents of the node with index 3:
   Index   0  >  child: 1   item: 27
                 child: 5
The contents of the node with index 4:
   Index   0  >  child: None   item: 150
   Index   1  >  child: None   item: 201
                 child: None
The contents of the node with index 5:
   Index   0  >  child: None   item: 29
                 child: None
The contents of the node with index 6:
   Index   0  >  child: 2   item: 64
                 child: 8
The contents of the node with index 7:
   Index   0  >  child: 3   item: 35
   Index   1  >  child: 6   item: 83
                 child: 10
The contents of the node with index 8:
   Index   0  >  child: None   item: 73
                 child: None
The contents of the node with index 9:
   Index   0  >  child: None   item: 90
                 child: None
The contents of the node with index 10:
   Index   0  >  child: 9   item: 98
                 child: 4

  The degree of the BTree is 1.
  The index of the root node is 7.
The contents of the node with index 1:
   Index   0  >  child: None   item: 15
                 child: None
The contents of the node with index 2:
   Index   0  >  child: None   item: 50
                 child: None
The contents of the node with index 3:
   Index   0  >  child: 1   item: 27
                 child: 5
The contents of the node with index 4:
   Index   0  >  child: None   item: 150
                 child: None
The contents of the node with index 5:
   Index   0  >  child: None   item: 29
                 child: None
The contents of the node with index 6:
   Index   0  >  child: 2   item: 64
                 child: 8
The contents of the node with index 7:
   Index   0  >  child: 3   item: 35
   Index   1  >  child: 6   item: 83
                 child: 10
The contents of the node with index 8:
   Index   0  >  child: None   item: 73
                 child: None
The contents of the node with index 9:
   Index   0  >  child: None   item: 87
   Index   1  >  child: None   item: 90
                 child: None
The contents of the node with index 10:
   Index   0  >  child: 9   item: 98
   Index   1  >  child: 4   item: 201
                 child: 11
The contents of the node with index 11:
   Index   0  >  child: None   item: 253
                 child: None

  The degree of the BTree is 1.
  The index of the root node is 15.
The contents of the node with index 1:
   Index   0  >  child: None   item: 15
                 child: None
The contents of the node with index 2:
   Index   0  >  child: None   item: 50
                 child: None
The contents of the node with index 3:
   Index   0  >  child: 1   item: 27
                 child: 5
The contents of the node with index 4:
   Index   0  >  child: None   item: 150
                 child: None
The contents of the node with index 5:
   Index   0  >  child: None   item: 29
                 child: None
The contents of the node with index 6:
   Index   0  >  child: 2   item: 64
                 child: 8
The contents of the node with index 7:
   Index   0  >  child: 3   item: 35
                 child: 6
The contents of the node with index 8:
   Index   0  >  child: None   item: 73
                 child: None
The contents of the node with index 9:
   Index   0  >  child: None   item: 84
                 child: None
The contents of the node with index 10:
   Index   0  >  child: 9   item: 87
                 child: 12
The contents of the node with index 11:
   Index   0  >  child: None   item: 253
                 child: None
The contents of the node with index 12:
   Index   0  >  child: None   item: 90
                 child: None
The contents of the node with index 13:
   Index   0  >  child: 4   item: 201
                 child: 11
The contents of the node with index 14:
   Index   0  >  child: 10   item: 98
                 child: 13
The contents of the node with index 15:
   Index   0  >  child: 7   item: 83
                 child: 14

 # run #2 -------------------------------
Name: Susie Id: 48 
  The degree of the BTree is 1.
  The index of the root node is 3.
The contents of the node with index 1:
   Index   0  >  child: None   item: Name: Willy Id: 12 
                 child: None
The contents of the node with index 2:
   Index   0  >  child: None   item: Name: Susie Id: 48 
                 child: None
The contents of the node with index 3:
   Index   0  >  child: 1   item: Name: Don Id: 35 
   Index   1  >  child: 4   item: Name: Billy Id: 39 
                 child: 2
The contents of the node with index 4:
   Index   0  >  child: None   item: Name: Joe Id: 38 
                 child: None

A level-by-level listing of the nodes: 
The contents of the node with index 3:
   Index   0  >  child: 1   item: Name: Don Id: 35 
   Index   1  >  child: 4   item: Name: Billy Id: 39 
                 child: 2
The contents of the node with index 1:
   Index   0  >  child: None   item: Name: Willy Id: 12 
                 child: None
The contents of the node with index 4:
   Index   0  >  child: None   item: Name: Joe Id: 38 
                 child: None
The contents of the node with index 2:
   Index   0  >  child: None   item: Name: Susie Id: 48 
                 child: None
An inorder traversal of the BTree:
Name: Willy Id: 12 
Name: Don Id: 35 
Name: Joe Id: 38 
Name: Billy Id: 39 
Name: Susie Id: 48 
An inorder traversal of the BTree:
Name: Willy Id: 12 
Name: Joe Id: 38 
Name: Billy Id: 39 
Name: Susie Id: 48 
 # run#3 -------------------------------
  The degree of the BTree is 2.
  The index of the root node is 9.
The contents of the node with index 1:
   Index   0  >  child: None   item: 5
   Index   1  >  child: None   item: 7
   Index   2  >  child: None   item: 8
                 child: None
The contents of the node with index 2:
   Index   0  >  child: None   item: 22
   Index   1  >  child: None   item: 24
                 child: None
The contents of the node with index 3:
   Index   0  >  child: 1   item: 10
   Index   1  >  child: 5   item: 20
                 child: 2
The contents of the node with index 4:
   Index   0  >  child: None   item: 32
   Index   1  >  child: None   item: 35
   Index   2  >  child: None   item: 38
                 child: None
The contents of the node with index 5:
   Index   0  >  child: None   item: 13
   Index   1  >  child: None   item: 15
   Index   2  >  child: None   item: 18
                 child: None
The contents of the node with index 6:
   Index   0  >  child: None   item: 42
   Index   1  >  child: None   item: 45
   Index   2  >  child: None   item: 46
                 child: None
The contents of the node with index 7:
   Index   0  >  child: None   item: 26
   Index   1  >  child: None   item: 27
                 child: None
The contents of the node with index 8:
   Index   0  >  child: 7   item: 30
   Index   1  >  child: 4   item: 40
                 child: 6
The contents of the node with index 9:
   Index   0  >  child: 3   item: 25
                 child: 8

 # run#4 -------------------------------
  The degree of the BTree is 2.
  The index of the root node is 3.
The contents of the node with index 1:
   Index   0  >  child: None   item: 5
   Index   1  >  child: None   item: 7
   Index   2  >  child: None   item: 8
                 child: None
The contents of the node with index 2:
   Index   0  >  child: None   item: 22
   Index   1  >  child: None   item: 24
                 child: None
The contents of the node with index 3:
   Index   0  >  child: 1   item: 10
   Index   1  >  child: 5   item: 20
   Index   2  >  child: 2   item: 26
   Index   3  >  child: 7   item: 42
                 child: 6
The contents of the node with index 5:
   Index   0  >  child: None   item: 13
   Index   1  >  child: None   item: 15
   Index   2  >  child: None   item: 18
                 child: None
The contents of the node with index 6:
   Index   0  >  child: None   item: 45
   Index   1  >  child: None   item: 46
                 child: None
The contents of the node with index 7:
   Index   0  >  child: None   item: 27
   Index   1  >  child: None   item: 30
   Index   2  >  child: None   item: 32
   Index   3  >  child: None   item: 40
                 child: None

 #run #5 -------------------------------
  The degree of the BTree is 1.
  The index of the root node is 3.
The contents of the node with index 1:
   Index   0  >  child: None   item: 27
   Index   1  >  child: None   item: 29
                 child: None
The contents of the node with index 2:
   Index   0  >  child: None   item: 50
   Index   1  >  child: None   item: 73
                 child: None
The contents of the node with index 3:
   Index   0  >  child: 1   item: 35
   Index   1  >  child: 2   item: 98
                 child: 4
The contents of the node with index 4:
   Index   0  >  child: None   item: 150
   Index   1  >  child: None   item: 201
                 child: None

  The degree of the BTree is 1.
  The index of the root node is 1.
The contents of the node with index 1:
   Index   0  >  child: None   item: 27
   Index   1  >  child: None   item: 201
                 child: None
'''
