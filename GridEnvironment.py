import random

#Grid Environment for N-Agents
class GridEnvironment:
    def __init__(self, n, m, num_agents, num_goals, start_pos) -> None:
        self.rows = n
        self.cols = m
        self.agents = num_agents
        self.goals = num_goals
        self.s_pos = start_pos
        self.goal_pos = []
        self.grid = self.gen_grid()
        self.gen_env()

    def gen_grid(self):
        return [['[.]' for _ in range(self.cols)] for _ in range(self.rows)]
    
    def getEmptyPos(self):
        while True:
            i, j = random.randint(0, self.rows-1), random.randint(0, self.cols-1)
            if self.grid[i][j] == '[.]':
                return (i,j)

    
    def gen_env(self):
        #Placing Agents
        for i in range(self.agents):
            start = self.s_pos[i]
            self.grid[start[0]][start[1]] = f'A({i+1})'
        
        #Placing Goals
        for i in range(self.goals):
            pos = self.getEmptyPos()
            self.goal_pos.append(pos)
            self.grid[pos[0]][pos[1]] = f'G({i+1})'
        
        #Placing PotHoles, Coins and Barriers.
        for i in range((self.rows * self.cols) // 5):
            pos = self.getEmptyPos()
            if random.uniform(0, 1) < 0.1:
                self.grid[pos[0]][pos[1]] = f'0({random.randint(-50, -10)})'
            elif random.uniform(0, 1) < 0.3:
                self.grid[pos[0]][pos[1]] = 'X'
            else:
                self.grid[pos[0]][pos[1]] = f'C({random.randint(10, 50)})'

        
    def print_grid(self):
        for i in range(self.rows):
            for j in range(self.cols):
                print(self.grid[i][j], end="  ") 
            print("\n")   
    