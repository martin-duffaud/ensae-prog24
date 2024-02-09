from grid import Grid

g = Grid(2, 3)
print(g)

data_path = "../input/"
file_name = data_path + "grid0.in"

print(file_name)

g = Grid.grid_from_file(file_name)
print(g)























def bfs_swap(self):

    def find_perm(g1,g2):
    e1, e2 = None, None
    for i in range(self.m):
        for j in range (self.n):
            if g1[i][j] != g2[i][j] :
                e1 = g1[i][j]
                e2 = g2[i][j]
                break
        if e1 is not None and e2 is not None :
            break
    return e1, e2

    gr = construct_graph(self.n,self.m)
    longueur_chemin, chemin = gr.bfs(self.state, [[i*j for j in range(1, self.n)] for i in range(1,self.m + 1)])
    
    for k in range (len(chemin)-1):
        g1, g2 = chemin[k], chemin[k+1]
        self.swap(find_perm(g1,g2))