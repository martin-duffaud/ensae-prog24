


class Grid:
    
    def __init__(self, m, n, initial_state = []):
        
        self.m = m
        self.n = n
        if not initial_state:
            initial_state = [list(range(i*n+1, (i+1)*n+1)) for i in range(m)]            
        self.state = initial_state

    def __str__(self): 
        output = f"The grid is in the following state:\n"
        for i in range(self.m): 
            output += f"{self.state[i]}\n"
        return output



    def swap(self, cell1, cell2):
        # TODO: Implement swap operation between two cells if they are neighbors.
        pass

    def is_sorted(self):
        # TODO: Check if the current state is sorted
        pass


    @classmethod
    def grid_from_file(cls, file_name): 
        # TODO : add checks that the number of lines is correct
        with open(file_name, "r") as file:
            m, n = map(int, file.readline().split())
            initial_state = [[] for i_line in range(m)]
            for i_line in range(m):
                line_state = list(map(int, file.readline().split()))
                if len(line_state) != n: 
                    raise Exception("Format incorrect")
                initial_state[i_line] = line_state
            g = Grid(m, n, initial_state)
        return g
