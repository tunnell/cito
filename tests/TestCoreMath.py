from cito.core.math import find_subranges

__author__ = 'tunnell'

import unittest


class CoreMathTestCase(unittest.TestCase):
    def test_subrange(self):
        self.assertEqual(find_subranges([2, 3, 4, 5, 12, 13, 14, 15, 16, 17, 20]),
                         [[0, 3], [4, 9], [10, 10]])


if __name__ == '__main__':
    unittest.main()
