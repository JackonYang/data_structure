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

    def test_isUnderflow(self):
        n = BTreeNode(4)
        n.items[0:8] = [15,20,30,None,None,None,None,None]
        n.child[0:9] = [1,2,3,4,None,None,None,None,None]
        n.numberOfKeys = 3
        self.assertTrue(n.isUnderFlow())

        p = BTreeNode(1)
        p.items[0:8] = [40,50]
        p.child[0:9] = [6,7,8]
        p.setNumberOfKeys(2)
        p.setIndex(17)
        self.assertFalse(p.isUnderFlow())

        m = BTreeNode(4)
        self.assertTrue(m.isUnderFlow())

    def test_findNext(self):
        n = BTreeNode(4)
        n.items[0:8] = [15,20,30,40,None,None,None,None]
        n.child[0:9] = [101, 102, 103, 104, 105, None, None, None, None]
        n.numberOfKeys = 4

        self.assertEquals(n.findNext(103), (104, False))
        self.assertEquals(n.findNext(103, inverse=True), (102, True))

        # boundary check
        self.assertEquals(n.findNext(104), (105, False))
        self.assertEquals(n.findNext(102, inverse=True), (101, True))
        self.assertEquals(n.findNext(105), (None, False))
        self.assertEquals(n.findNext(101, inverse=True), (None, True))
        # comment below to avoid printing info msg
        #self.assertEquals(n.findNext(100, inverse=True), None)
        #self.assertEquals(n.findNext(100, inverse=False), None)

    def test_addItemAndSplit(self):
        import copy
        n = BTreeNode(2)
        n.items[0:4] = [15,20,30,35]
        n.child[0:5] = [1,2,3,4,5]
        n.numberOfKeys = 4
        n.index = 10

        # add 32
        temp = copy.deepcopy(n)
        new_node = temp.addItemAndSplit(32, 4, 13)
        self.assertEqual(temp.items[:3], [15, 20, 30])
        self.assertEqual(temp.numberOfKeys, 3)
        self.assertEqual(new_node.items, [32, 35, None, None])

        # add 10
        temp = copy.deepcopy(n)
        new_node = temp.addItemAndSplit(10, 4, 13)
        self.assertEqual(temp.items[:3], [10, 15, 20])
        self.assertEqual(temp.numberOfKeys, 3)
        self.assertEqual(new_node.items, [30, 35, None, None]) 

        # add 36
        temp = copy.deepcopy(n)
        new_node = temp.addItemAndSplit(36, 4, 13)
        self.assertEqual(temp.items[:3], [15, 20, 30])
        self.assertEqual(temp.numberOfKeys, 3)
        self.assertEqual(new_node.items, [35, 36, None, None])

        n = BTreeNode(1)
        n.items = [64, 89]
        n.child= [2, 8, 4]
        n.numberOfKeys = 2
        n.index = 6
        rhs = n.addItemAndSplit(83, 7, 9)
        self.assertEqual(n.items, [64, 83])
        self.assertEqual(n.child, [2, 7, 9])
        self.assertEqual(n.numberOfKeys, 2)
        self.assertEqual(rhs.items, [89, None])
        self.assertEqual(rhs.child, [9, 4, None])

        lhs = BTreeNode(1)
        lhs.items = [64, 89]
        lhs.child= [2, 8, 4]
        lhs.numberOfKeys = 2
        lhs.index = 6
        rhs = lhs.addItemAndSplit(93, 7, 9)
        self.assertEqual(lhs.items, [64, 89])
        self.assertEqual(lhs.child, [2, 8, 7])
        self.assertEqual(lhs.numberOfKeys, 2)
        self.assertEqual(rhs.items, [93, None])
        self.assertEqual(rhs.child, [7, 9, None])
        self.assertEqual(rhs.numberOfKeys, 1)

    def test_insertItem(self):
        b = BTreeNode(3)
        b.index = 133
        b.insertItem(500, 19, 21)
        b.insertItem(150, 31, 43)
        b.insertItem(200, 50, 62)
        b.insertItem(700, 70, 18)
        b.insertItem(100, 19, 10)
        b.insertItem(300, 11, 12)
        self.assertEqual(b.items, [100, 150, 200, 300, 500, 700])
        self.assertEqual(b.child, [19, 10, 50, 11, 12, 70, 18])

    def test_splitLast(self):
        n = BTreeNode(2)
        n.items[0:8] = [15,35,None,None]
        n.child[0:9] = [1,4,5,None,None]
        n.numberOfKeys = 2
        m = n.splitLast()
        self.assertEqual(m.items, [35, None, None, None])
        self.assertEqual(m.child, [4, 5, None, None, None])
 

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

    def test_add_insert_not_full(self):
        bt = BTree(2)
        bt.insert(50)
        self.assertEqual(bt.rootNode.items, [50, None, None, None])
        bt.insert(27)
        self.assertEqual(bt.rootNode.items, [27, 50, None, None])
        res = bt.insert(30)
        self.assertEqual(bt.rootNode.items, [27, 30, 50, None])
        res = bt.insert(10)
        self.assertEqual(bt.rootNode.items, [10, 27, 30, 50])

    def test_add_insert_full(self):
        bt = BTree(1)
        bt.insert(50)
        self.assertEqual(bt.rootNode.items, [50, None])
        bt.insert(27)
        self.assertEqual(bt.rootNode.items, [27, 50])

        res = bt.insert(35)
        self.assertEqual(res, 35)

    def test_add_insert_deep(self):
        bt = BTree(1)
        bt.insert(50)
        bt.insert(27)
        res = bt.insert(35)
        self.assertEqual(res, 35)  # full, root
        bt.insert(98)
        bt.insert(201)

    def test_add_insert_split_parent(self):
        bt = BTree(1)
        bt.insert(50)
        bt.insert(27)
        bt.insert(35)
        bt.insert(98)
        bt.insert(201)

        bt.insert(73)
        bt.insert(29)
        bt.insert(150)
        bt.insert(15)
        # print( bt )

    def test_add_insert_full_d2(self):
        bt = BTree(2)
        bt.insert(50)
        self.assertEqual(bt.rootNode.items, [50, None, None, None])
        bt.insert(27)
        self.assertEqual(bt.rootNode.items, [27, 50, None, None])
        bt.insert(11)
        self.assertEqual(bt.rootNode.items, [11, 27, 50, None])
        bt.insert(72)
        self.assertEqual(bt.rootNode.items, [11, 27, 50, 72])

        res = bt.insert(10)
        self.assertEqual(res, 10)

    def test_del_leaf_not_underflow(self):
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
        print( bt )

if __name__=='__main__':
    suite=unittest.TestSuite()

    runner=unittest.TextTestRunner()

    suite.addTest(test_btree_node('test_copyWithRight'))
    suite.addTest(test_btree_node('test_addItemAndSplit'))
    suite.addTest(test_btree_node('test_insertItem'))
    suite.addTest(test_btree_node('test_isLeaf'))
    suite.addTest(test_btree_node('test_isUnderflow'))
    suite.addTest(test_btree_node('test_splitLast'))

    suite.addTest(test_btree_node('test_findNext'))

    suite.addTest(test_btree('test_is_root'))
    suite.addTest(test_btree('test_add_insert_not_full'))
    suite.addTest(test_btree('test_add_insert_full'))
    suite.addTest(test_btree('test_add_insert_full_d2'))

    suite.addTest(test_btree('test_add_insert_deep'))
    suite.addTest(test_btree('test_add_insert_split_parent'))
    suite.addTest(test_btree('test_del_leaf_not_underflow'))
    runner=unittest.TextTestRunner()
    runner.run(suite)
