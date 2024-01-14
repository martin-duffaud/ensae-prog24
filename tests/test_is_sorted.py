# This will work if ran from the root folder ensae-prog24
import sys 
sys.path.append("swap_puzzle/")

import unittest 
from grid import Grid

class Test_IsSorted(unittest.TestCase):
    def test_grid1(self):
        grid = Grid.grid_from_file("input/grid1.in")
        self.assertEqual(grid.is_sorted(), False)
        grid.swap((3,0), (3,1))
        self.assertEqual(grid.is_sorted(), True)

if __name__ == '__main__':
    unittest.main()