from collections import deque
import math
from queue import PriorityQueue
from GridEnvironment import *
from CSP import *

#Self-Driving Car Simulation
class Simulation:
    def __init__(self, env: GridEnvironment, csp: CSPSolver) -> None:
        self.env = env
        self.positions = {}
        self.csp_solver = csp

    def solve_with_csp(self, start):
        path = self.csp_solver.solve_csp(start)
        return path

    def getNeighbours(self, pos, curr_timer, agent_id):
        neighbors = []
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            r, c = pos[0] + dr, pos[1] + dc
            if 0 <= r < self.env.rows and 0 <= c < self.env.cols and self.env.grid[r][c] != 'X':
                if self.positions:
                    #If any other agent is in the same position at the same time than the position is not valid
                    for id, val in self.positions.items():
                        if curr_timer in val.keys() and id!=agent_id:
                            if val[curr_timer] != (r,c):
                                neighbors.append((r, c))
                            else:
                                print(f"Oops. Encountered Another Agent {id+1} at Position {r, c}\n")
                        elif id == agent_id:
                            neighbors.append((r, c))
                else:
                    neighbors.append((r, c))
        return neighbors

    def BFS(self, agent_id):
        t = 0
        start = self.env.s_pos[agent_id]
        curr = {}

        visited = set()
        queue = deque([(start, [])])
        
        while queue:
            curr_pos, path = queue.popleft()
            if curr_pos in visited:
                continue
            visited.add(curr_pos)
            curr[t] = curr_pos

            if self.env.grid[curr_pos[0]][curr_pos[1]].startswith('G'):
                self.positions[agent_id] = curr
                return path + [curr_pos]
            t+=1
            for neighbors in self.getNeighbours(curr_pos, t, agent_id):
                queue.append((neighbors, path+[curr_pos]))
        return None


    def DFS(self, agent_id):
        start = self.env.s_pos[agent_id]
        visited = set()
        t = 0
        curr = {}

        stack = [(start, [])]

        while stack:
            curr_pos, path = stack.pop()
            if curr_pos in visited:
                continue
            visited.add(curr_pos)
            curr[t] = curr_pos
            t+=1
            if self.env.grid[curr_pos[0]][curr_pos[1]].startswith("G"):
                self.positions[agent_id] = curr
                return path + [curr_pos]
            
            for neighbor in self.getNeighbours(curr_pos, t, agent_id):
                stack.append((neighbor, path + [curr_pos]))
        return None
    
    def manhattan_distance(self, curr_pos, goal_pos):
        return abs(curr_pos[0] - goal_pos[0]) + abs(curr_pos[1] - goal_pos[1])
    
    def euclidean_distance(self, curr_pos, goal_pos):
        return math.sqrt(math.pow((curr_pos[0] - goal_pos[0]), 2) + math.pow((curr_pos[1] - goal_pos[1]), 2))
    
    def chebyshev_distance(self, curr_pos, goal_pos):
        return max(abs(curr_pos[0] - goal_pos[0]), abs(curr_pos[1] - goal_pos[1]))
    
    def calculate_heuristic(self, start, goal, heuristic):
        if heuristic == "euc":
            return self.euclidean_distance(start, goal)
        elif heuristic == "man":
           return self.manhattan_distance(start, goal)
        elif heuristic == "cheb":
            return self.chebyshev_distance(start, goal)

    def a_star(self, agent_id, heuristic):
        t = 0
        start = self.env.s_pos[agent_id]
        goal = self.env.goal_pos[random.randint(1, self.env.goals)-1]  #Choosing Random Goal

        open_set = PriorityQueue()
        open_set.put((0, start))

        came_from = {}
        curr_t = {}
        g_score = {start: 0}
        f_score = {start: self.calculate_heuristic(start, goal, heuristic)}

        while not open_set.empty():
            _, current = open_set.get()
            curr_t[t] = current
            if current == goal:
                self.positions[agent_id] = curr_t  # Store positions for the agent
                return self.reconstruct_path(came_from, current)

            for neighbor in self.getNeighbours(current, t, agent_id):
                tentative_g_score = g_score[current] + 1  # Assuming uniform cost of movement

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.calculate_heuristic(neighbor, goal, heuristic)
                    open_set.put((f_score[neighbor], neighbor))

            t += 1 

        return None
    
    def reconstruct_path(self, came_from, current):
        path = []
        while current in came_from:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path
    

    def evaluate_path(self, path):
        reward = 0
        for i in path:
            # print(i)
            if self.env.grid[i[0]][i[1]].startswith('C'):
                reward += int(self.env.grid[i[0]][i[1]].split('(')[1].split(')')[0])
            elif self.env.grid[i[0]][i[1]].startswith('O'):
                reward -= int(self.env.grid[i[0]][i[1]].split('(')[1].split(')')[0])

        return reward

