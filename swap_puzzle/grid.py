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
        Comme la fonction heuristique est utilisée comme une key function pour ordonner 
        la file, sa présence dans la fonction astar, bien que peu élégante, est nécessaire.
        L'heuristique choisie donne la somme des distances de Manhattan (norme 1) 
        pour chaque élément de la grille, notées (i,j) (correspondant à la ligne i et colonne j 
        où se trouve l'élément), et l'emplacement (itarget, jtarget) où il serait si la grille était
        triée. C'est en quelque sorte sa distance à la grille objectif.
        '''

        m=self.m
        n=self.n
        def heuristique(grille,m,n): 
            s = 0
            for i in range(m):
                for j in range(n):
                    k = grille[i][j]
                    itarget = k // n - 1
                    jtarget = k%n
                    s += abs(i - itarget) + abs(j - jtarget)
                    return s

        traites = []
        liste_chemins = [[self]]
        openList = self.gridlist_from_permlist()
        hq.merge(openList,key=heuristique)
        hq.heappush(openList,self.state)
        while openList != [] :
            u = hq.heappop(openList)
            for chemin in liste_chemins:
                if chemin[len(chemin)-1].state == u:
                    chemin_a_completer = chemin
                    liste_chemins.remove(chemin)
                    if u == dst.state:  
                        return chemin_a_completer
            
            """
            on introduit la liste de toutes les grilles voisines de s
            """
            grid_u=Grid(m,n,u)
            liste_voisins = grid_u.grilles_voisines()
            for v in liste_voisins:
                grid_v=Grid(m,n,v)
                if not (v in traites or (v in openList and heuristique(v,m,n) < heuristique(u,m,n) + 1)):
                    hq.heappush(openList,v)
                    liste_chemins.append(chemin_a_completer + [grid_v])
            traites.append(u)
        raise Exception("Error")

    '''
    Question 2 : voici un autre exemple d'heuristique possible dans notre
    cadre d'étude
    '''

    '''
    Voici une première alternative à l'heuristique utilisée dans astar.
    Comme les grilles sont des permutations sur {1, ..., mn}, la distance de 
    Kendall-Tau, dKT, qui donne  le nombre de paires d’éléments qui sont en désaccord 
    par rapport à leur ordre. En particulier, dans notre cas, on compare une grille 
    avec l'identité, donc on va simplement calculer le nombre d'inversion d'une permutation.
    si g est une grille et Id est l'identité, le nombre d'inversion de g est dKT(g, Id).
    
    En pratique, la distance de Kendall Tau est équivalente au nombre de swaps effectués 
    par le Tri à Bulle. Elle prend ainsi ses valeurs entre 0 et mn

    L'intérêt de cette heuristique est qu'elle est par nature fondée sur le problème 
    de recherche d'un nombre de swaps optimal entre deux grilles, puisqu'elle mesure justement
    cette valeur.

    L'implémentation naive est en O((mn)^2). Cependant, comme on compare toujours une grille avec 
    l'identité, l'utilisation du tri fusion permet, en comptant le nombre de "sauts" des éléments 
    de la 2e liste lors de la fusion, d'obtenir un temps de calcul en O((mnlog(mn))).
    '''

    def kendall_tau_naif(self):  # Question 2 ; Séances 3 et 4
        s = 0
        n, m = self.m, self.n
        for a in range(m*n):
            for b in range(m*n):
                if a < b and self.state[a//n - 1][a%n] > self.state[b//n - 1][b%n]:
                    s += 1
        return s
    
    '''
    Pour la question 4 et la création de niveaux de difficulté, le fait
    d'utiliser la distance de Kendall-Tau comme heuristique simplifie 
    grandement le choix de grille à effectuer : on aura qu'à, à partir
    de l'identité, réaliser un certain nombre d'inversions pour choisir
    la difficulté. On remplace donc l'heuristique du code de astar 
    (distance de Manhattan) par celle de Kendall-Tau. On suppose donc
    que ce changement a été effectué (ce qui revient à remplacer les
    lignes 336 à 343 par les lignes 395 à 401).

    On choisit 4 niveaux de difficultés. Soit g une grille.
    En notant dmax = mn (qui est la valeur maximale pour dKT(g, Id) 
    comme on l'a vu précédemment), on a :
    - La difficulté du jeu est EASY:= 1 ssi         1 <= dKT(g, ID) <= dmax//4
    - La difficulté du jeu est INTERMEDIATE:= 2 ssi dmax//4 < dKT(g, ID) <= dmax//2
    - La difficulté du jeu est DIFFICULT := 3 ssi   dmax//2 < dKT(g, ID) <= 3dmax//4
    - La difficulté du jeu est HARDCORE := 4 ssi    3dmax//4 < dKT(g, ID) <= dmax
    '''

    def level_starter(self, difficulty):  # Question 4 ; Séances 3 et 4
        n, m = self.m, self.n
        dmax = m*n
        if difficulty == 1:
            k = random.randint(1, dmax//4)
        elif difficulty == 2:
            k = random.randint(dmax//4 + 1, dmax//2)
        elif difficulty == 3:
            k = random.randint(dmax//2 + 1, 3*dmax//4)
        elif difficulty == 4:
            k = random.randint(3*dmax//4 + 1, dmax)

        inversions = random.sample([a for a in range(m*n)], k)
        starter = Grid(m, n)

        for a in range(k-1):
            i1, i2 = inversions[a]//n, inversions[a+1]//n
            j1, j2 = a%n, (a+1)%n
            starter.state[i1][j1], starter.state[i2][j2] = starter.state[i2][j2], starter.state[i1][j1]

        return starter




    


    





