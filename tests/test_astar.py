import sys 
sys.path.append("swap_puzzle/")

from grid import Grid
grid = Grid.grid_from_file("input/grid2.in")

n=grid.n
m=grid.m

result=grid.astar(Grid(m,n))
for i in range(len(result)):
    print(result[i])
