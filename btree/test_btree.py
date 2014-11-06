# -*- coding: utf-8-*-
import unittest
from btree import BTree

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

if __name__=='__main__':
    suite=unittest.TestSuite()

    runner=unittest.TextTestRunner()
    runner.run(suite)
    suite.addTest(test_btree('test_is_root'))
    runner=unittest.TextTestRunner()
    runner.run(suite)
