import sys 
sys.path.append("swap_puzzle/")

import unittest 
from graph import Graph

class Test_BFSLoading(unittest.TestCase):
    def test_bfs(self):
        g = Graph.graph_from_file("input/graph1.in")
        """
        On utilise les éléments de graph1.path.out pour 
        vérifier la fonction bfs. Voici un exemple avec
        2 et 17
        """
        self.assertEqual(g.bfs(2,17), (2, [2, 14, 17]))

if __name__ == '__main__':
    unittest.main()
