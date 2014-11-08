# -*- coding: utf-8-*-
import unittest
from btree import BTree
from btree import BTreeNode

class test_btree_node(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_copyWithRight(self):
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

        # print n.copyWithRight(m,p) 

    def test_isLeaf(self):
        n = BTreeNode(4)
        n.items[0:8] = [15,20,30,35,None,None,None,None]
        n.child[0:9] = [1,2,3,4,5,None,None,None,None]
        n.numberOfKeys = 4
        self.assertFalse(n.isLeaf())

        p = BTreeNode(1)
        p.items[0:8] = [40,50]
        p.child[0:9] = [6,7,8]
        p.setNumberOfKeys(2)
        p.setIndex(17)
        self.assertFalse(p.isLeaf())

        m = BTreeNode(4)
        self.assertTrue(m.isLeaf())

 
class test_btree(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_is_root(self):
        bt = BTree(1)
        self.assertTrue(bt.isRoot(1))
        self.assertFalse(bt.isRoot(0))
        self.assertFalse(bt.isRoot(3))

    def test_add_in_root(self):
        bt = BTree(1)
        bt.addInRoot(50)
        self.assertEqual(bt.rootNode.items, [50, None])
        bt.addInRoot(27)
        self.assertEqual(bt.rootNode.items, [27, 50])
        bt.addInRoot(35)

if __name__=='__main__':
    suite=unittest.TestSuite()

    runner=unittest.TextTestRunner()
    runner.run(suite)

    suite.addTest(test_btree_node('test_copyWithRight'))
    suite.addTest(test_btree_node('test_isLeaf'))

    suite.addTest(test_btree('test_is_root'))
    suite.addTest(test_btree('test_add_in_root'))
    runner=unittest.TextTestRunner()
    runner.run(suite)
