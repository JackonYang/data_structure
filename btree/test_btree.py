# -*- coding: utf-8-*-
import unittest

class test_btree(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_is_root(self):
        self.assertEquals(1, 1)

if __name__=='__main__':
    suite=unittest.TestSuite()

    runner=unittest.TextTestRunner()
    runner.run(suite)
    suite.addTest(test_btree('test_is_root'))
    runner=unittest.TextTestRunner()
    runner.run(suite)
