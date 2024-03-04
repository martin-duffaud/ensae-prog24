import sys 
sys.path.append("swap_puzzle/")

from grid import Grid
grid = Grid.grid_from_file("input/grid1.in")

print(grid.level_starter(1))