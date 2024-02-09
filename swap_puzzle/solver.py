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
        grille = self.state
        def research(x,grille):
            for k in range (m):
                for l in range (n):
                    if grille[k][l] == x+1 :
                        return (k,l)

        def relocate(x):
            (k,l) = research(x,grille)
            i = x//n
            j = x - n*i
            if k<i :
                for a in range(i-k):
                    self.swap((k+a+1,l),(k+a,l))
            elif k>i :
                for a in range(k-i, -1):
                    self.swap((k+a+1,l),(k+a,l))
            if l<j : 
                for b in range(j-l):
                    self.swap((i,l+b+1),(i,l+b))
            if l>j : 
                for b in range(l-j, -1):
                    self.swap((i,l+b+1),(i,l+b))

        for x in range (n*m):
            relocate(x)

    """
    The Function below is another proposal of answer to the question 3, 
    that is effective and was considered as naive by the binomial.
    While the grid is not sorted, it runs through the grid comparing
    every square to its right neighbor and then its bottom neighbor.
    """

    def get_solution2(self):
        """
        Solves the grid and returns the sequence of swaps at the format 
        [((i1, j1), (i2, j2)), ((i1', j1'), (i2', j2')), ...]. 
        """
        n = self.n
        m = self.m
        while not self.is_sorted() :
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




        



