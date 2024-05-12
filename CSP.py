class CSPSolver:
    def __init__(self, grid_env, start_pos):
        self.grid_env = grid_env
        self.start = start_pos
        self.domain = [(0, 1), (1, 0), (-1, 0), (0, -1)]
    
    def solve_csp(self, start):
        return self.backtrack({start}, [])

    def backtrack(self, assignments, paths):
        if self.goal_reached(paths):
            return paths

        new_action = self.select_unassigned_variable(assignments)
        for action in self.domain:
            if self.valid_action(new_action, action):
                new_assignment = assignments.copy()
                new_assignment.add(new_action)
                paths = paths + [new_action]
                result_assignments = self.backtrack(new_assignment, paths)
                if result_assignments:
                    return result_assignments
        return None


    def goal_reached(self, paths):
        return any(self.grid_env.grid[pos[0]][pos[1]].startswith('G') for pos in paths)
    
    def select_unassigned_variable(self, assignments):
        for row in range(self.grid_env.rows):
            for col in range(self.grid_env.cols):
                if (row, col) not in assignments and self.grid_env.grid[row][col]!='X':
                    return (row, col)
    
    def valid_action(self, action, pos):
        row, col = pos
        return (0<=row+action[0]<self.grid_env.rows-1) and (0<=col+action[1]<self.grid_env.cols-1) and (self.grid_env.grid[row + action[0]][col+action[1]] != 'X')
                
