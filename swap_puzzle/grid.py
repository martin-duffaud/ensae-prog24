"""
This is the grid module. It contains the Grid class and its associated methods.
"""
import numpy as np
import random
import heapq as hq

import sys 
sys.path.append("swap_puzzle/")
from graph import Graph

import matplotlib.pyplot as plt

class Grid():
    """
    A class representing the grid from the swap puzzle. It supports rectangular grids. 

    Attributes: 
    -----------
    m: int
        Number of lines in the grid
    n: int
        Number of columns in the grid
    state: list[list[int]]
        The state of the grid, a list of list such that state[i][j] is the number in the cell (i, j), i.e., in the i-th line and j-th column. 
        Note: lines are numbered 0..m and columns are numbered 0..n.
    """
    
    def __init__(self, m, n, initial_state = []):
        """
        Initializes the grid.

        Parameters: 
        -----------
        m: int
            Number of lines in the grid
        n: int
            Number of columns in the grid
        initial_state: list[list[int]]
            The intiail state of the grid. Default is empty (then the grid is created sorted).
        """
        self.m = m
        self.n = n
        if not initial_state:
            initial_state = [list(range(i*n+1, (i+1)*n+1)) for i in range(m)]            
        self.state = initial_state

    def __str__(self): 
        """
        Prints the state of the grid as text.
        """
        output = f"The grid is in the following state:\n"
        for i in range(self.m): 
            output += f"{self.state[i]}\n"
        return output

    def __repr__(self):   # Question 3
        """
        Returns a representation of the grid with number of rows and columns.
        """
        return f"<grid.Grid: m={self.m}, n={self.n}>"

    def is_sorted(self):  # Question 2
        """
        Checks is the current state of the grid is sorted and returns the answer as a boolean.
        """
        n = self.n
        m = self.m
        return self.state == [list(range(i*n+1, (i+1)*n+1)) for i in range(m)]

    def swap(self, cell1, cell2):  # Question 2
        """
        Implements the swap operation between two cells. Raises an exception if the swap is not allowed.

        Parameters: 
        -----------
        cell1, cell2: tuple[int]
            The two cells to swap. They must be in the format (i, j) where i is the line and j the column number of the cell. 
        """
        i1, j1 = cell1
        i2, j2 = cell2
        if i1 == i2 and abs(j1-j2) == 1 or j1 == j2 and abs(i1-i2):
            self.state[i1][j1], self.state[i2][j2] = self.state[i2][j2], self.state[i1][j1]
        else:
            raise Exception("Sorry, this swap is not allowed")

    def swap_seq(self, cell_pair_list):  # Question 2
        """
        Executes a sequence of swaps. 

        Parameters: 
        -----------
        cell_pair_list: list[tuple[tuple[int]]]
            List of swaps, each swap being a tuple of two cells (each cell being a tuple of integers). 
            So the format should be [((i1, j1), (i2, j2)), ((i1', j1'), (i2', j2')), ...].
        """
        for (cell1, cell2) in cell_pair_list:
            self.swap(cell1, cell2)

    @classmethod
    def grid_from_file(cls, file_name): 
        """
        Creates a grid object from class Grid, initialized with the information from the file file_name.
    
        Parameters: 
        -----------
        file_name: str
            Name of the file to load. The file must be of the format: 
            - first line contains "m n" 
            - next m lines contain n integers that represent the state of the corresponding cell

        Output: 
        -------
        grid: Grid
            The grid
        """
        with open(file_name, "r") as file:
            m, n = map(int, file.readline().split())
            initial_state = [[] for i_line in range(m)]
            for i_line in range(m):
                line_state = list(map(int, file.readline().split()))
                if len(line_state) != n: 
                    raise Exception("Format incorrect")
                initial_state[i_line] = line_state
            grid = Grid(m, n, initial_state)
        return grid

    def display(self):
        n=self.n
        m=self.m
        colonnes=[i for i in range (n)]
        lignes=[i for i in range (m)]
        cases=[[self.state[j][i] for i in range(n)] for j in range(m)]
        table=plt.table(cellText=cases, rowLabels=lignes, colLabels=colonnes, rowColours=["blue"]*m, colColours=["blue"]*n)
        plt.show()

    def permutation(self, lst):  # Question 6
        if len(lst) == 0:
            return []
        if len(lst) == 1:
            return [lst]
        l = []
        """
        c'est une fonction récursive : pour toutes les permutations d'un ensemble à n éléments, on considère 
        toutes les permutations de tous les sous-ensembles à n-1 éléments en ajoutant au début de toutes ces 
        permutations l'élément qu'on n'a pas considéré
        """
        for i in range(len(lst)):
            m = lst[i]
            sous_lst = lst[:i] + lst[i+1:]
        for p in self.permutation(sous_lst):
            l.append([m] + p)
        return l

    def gridlist_from_permlist(self):  # Question 6    
        """
        cette fonction permet de construire la liste des grilles à partir de la liste des permutations
        """
        n, m = self.n, self.m
        permlist = self.permutation([i for i in range(1,n*m +1)])
        liste_grilles = []

        def grid_from_perm(s):
            grille = []    
            for i in range(m):
                ligne_i = []
                for j in range(n):
                    ligne_i.append(s[n*i + j])
                grille.append(ligne_i)
            return grille

        for s in permlist:
            liste_grilles.append(grid_from_perm(s))
   
        return liste_grilles

    def all_swaps_possible(self):  # Question 6
        list_swaps = []
        m, n = self.m, self.n
        for i in range(m):
            for j in range(n):
                if i != 0:
                    list_swaps.append(((i, j), (i-1, j)))
                if i != (m-1):
                    list_swaps.append(((i, j), (i+1, j)))  
                if j != 0:
                    list_swaps.append(((i, j), (i, j-1)))
                if j != (n-1):
                    list_swaps.append(((i, j), (i, j+1)))
        return list_swaps

    def grilles_voisines(self):  # Question 6
        """
        cette fonction renvoie la liste de toutes les grilles voisines d'une grille, au sens où elles sont accessibles en un seul swap
        """
        L = []
        S = self.all_swaps_possible()
        for k in range(len(S)):
            g_temp=Grid(self.m,self.n,copy.deepcopy(self.state))
            g_temp.swap(S[k][0], S[k][1])
            L.append(g_temp.state)
        return L

    def construct_graph(self):  # Question 7
        """ 
        on considère la liste de toutes les grilles de taille n*m à partir de la fonction qui génère toutes les
        permutations de l'ensemble {1,2,...,n*m} sans considérer la grille objectif car on initialisera le graphe 
        avec celle-ci
        """
        n, m = self.n, self.m
        gl = self.gridlist_from_permlist()[1:]
        """
        Création du graphe gr, initialisé avec le noeud objectif, qui est la grille triée
        """
        gr = Graph([Grid(m, n)])

        """ 
        on cherche à vider la liste de toutes les grilles possibles: on la parcourt tant qu'elle est non vide
        """
        while gl != []:
            traitees = []
            for i in range(len(gl)):
                """
                pour chaque grille à ajouter dans le graphe, on parcourt tous les noeuds (grilles) du graphe 
                en cours de construction ; quand un noeud du graphe est voisin de la grille que l'on parcourt 
                (ce que l'on teste avec la fonction grilles_voisines), on associe les deux grilles en ajoutant 
                l'arête voulue
                """
                for j in range(len(gr.nodes)):
                    if gl[i] in (gr.nodes[j]).grilles_voisines():
                        traitees.append(i)
                        gr.nodes.append(gl[i])
                        gr.add_edge(gl[i], gr.nodes[j])
                        break
            """ 
            on supprime toutes les grilles qu'on a pu rajouter au graphe
            """            
            for v in range(len(traitees)):
                del (gl[v])
        return gr

    def bfs_swap(self):  # Question 7
        """
        cette fonction a pour but de reproduire la séquence de swaps qui permet de passer d'une grille quelconque à la grille triée
        """
        def find_perm(g1, g2):
            """
            cette fonction permet de trouver le swap qui a permis de passer d'une grille à une autre étant données ces deux grilles
            """
            e1, e2 = None, None
            for i in range(self.m):
                for j in range(self.n):
                    if g1[i][j] != g2[i][j]:
                        e1 = g1[i][j]
                        e2 = g2[i][j]
                        break
                if e1 is not None and e2 is not None:
                    break
            return e1, e2

        """
        on construit le graphe des grilles et on applique le bfs
        """
        gr = self.construct_graph()
        source = self.state
        but = [[i*j for j in range(1, self.n + 1)] for i in range(1, self.m + 1)]
        longueur_chemin, chemin = gr.bfs(source, but)
        """
        on effectue la séquence de swaps du chemin trouvé par bfs
        """
        for k in range(len(chemin)-1):
            g1, g2 = chemin[k], chemin[k+1]
            self.swap(find_perm(g1, g2))

    def final_bfs(self, dst):  # Question 8
        """
        il faut associer une clé unique à chaque grille
        """
        src = self
        liste_grilles = Grid(self.m, self.n).gridlist_from_permlist()
        cle_src = liste_grilles.index(src.state)
        g = Graph([cle_src])
        liste_chemins = [[src]]
        aparcourir = [src]
        parcourus = [src]
        while aparcourir != []:
            s = aparcourir[0]
            aparcourir.remove(0)
            cle_s = liste_grilles.index(s.state)
            print(cle_s)
            """
            on complète les chemins en récupérant le chemin finissant par s
            """
            for chemin in liste_chemins:
                if chemin[len(chemin)-1] == s:
                    chemin_a_completer = chemin
                    liste_chemins.remove(chemin)
            """
            on crée la liste de toutes les grilles voisines de s
            """
            V_tmp = s.grilles_voisines()
            V = []
            for i in range(len(V_tmp)):
                v = Grid(self.m, self.n)
                v.state = V_tmp[i]
                V.append(v)
            """
            on rajoute au graphe les voisins de s qui ne sont pas déjà parcourus ni à parcourir
            """
            for voisin_possible in V:
                if (voisin_possible not in aparcourir) and (voisin_possible not in parcourus):
                    try:
                        g.graph[cle_s].append(voisin_possible)
                    except KeyError:
                        g.graph[cle_s] = [voisin_possible]
                    liste_chemins.append(chemin_a_completer+[voisin_possible])
                    aparcourir.append(voisin_possible)
                    parcourus.append(voisin_possible)
                if voisin_possible == dst:
                    return (len(chemin_a_completer), chemin_a_completer+[voisin_possible])
        return None
    
    def astar(self, dst):  # Question 1 ; Séances 3 et 4

        '''
        Comme heuristique est utilisé comme un key function pour ordonner la file,
        sa présence dans la fonction astar, bien que peu élégante, est nécessaire
        '''

        def heuristique(grille):  # Question 1 ; Séances 3 et 4
            s = 0
            for i in range(grille.m):
                for j in range(grille.n):
                    k = grille.state[i][j]
                    itarget = k % grille.n
                    jtarget = k - itarget*grille.n
                    s += abs(i - itarget) + abs(j - jtarget)
                    return s

        traites = []
        liste_chemins = [[self]]
        openList = hq.merge(key=heuristique)
        openList.push(self)
        while openList != [] :
            u = openList.pop()
            for chemin in liste_chemins:
                if chemin[len(chemin)-1] == u:
                    chemin_a_completer = chemin
                    liste_chemins.remove(chemin)
                    if u.state == dst.state:  
                        return chemin_a_completer
            
            """
            on introduit la liste de toutes les grilles voisines de s
            """
            liste_voisins = u.grilles_voisines()
            for v in liste_voisins:
                if not (v in traites or (v in openList and v.heuristique < u.heuristique + 1)):
                    openList.push(v)
                    liste_chemins.append(chemin_a_completer + [v])
            traites.ajouter(u)
        raise Exception("Error")

