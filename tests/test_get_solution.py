# This will work if ran from the root folder ensae-prog24
import sys 
sys.path.append("../swap_puzzle/")

import unittest 
from swap_puzzle import Grid
from swap_puzzle import Solver

class Test_get_solution(unittest.TestCase):
    def test_grid1(self):
        g = Grid.grid_from_file("../input/grid1.in")
        s = Solver()
        s.get_solution(g)
        self.assertEqual(g.is_sorted(), True)

if __name__ == '__main__':
    unittest.main()