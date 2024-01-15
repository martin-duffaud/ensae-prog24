from grid import Grid

class Solver(Grid): 
    """
    A solver class, to be implemented.
    """
    
    def get_solution(self):
        """
        Solves the grid and returns the sequence of swaps at the format 
        [((i1, j1), (i2, j2)), ((i1', j1'), (i2', j2')), ...]. 
        """
        n = self.n
        m = self.m
        while not self.is_sorted :
            for i in range (m):
                for j in range (n):
                    if j < n-1 :
                        cell1 = (i, j)
                        cell2 = (i, j+1)
                        if self.state[i][j] > self.state[i][j+1]:
                            self.swap(cell1,cell2)
                    if i < m-1 :
                        cell1 = (i, j)
                        cell2 = (i+1, j)
                        if self.state[i][j] > self.state[i+1][j]:
                            self.swap(cell1, cell2)
        



