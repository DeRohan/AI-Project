from GridEnvironment import *
from CSP import *
from Simulation import *


def choose_heuristic():
    print("Please Choose a Heuristic for A Star algorithm")
    print("1. Euclidean Distance")
    print("2. Manhattan Distance")
    print("3. Chebyshev Distance")
    choice = int(input("Enter Your Choice: "))
    if choice == 1:
        return "euc"
    elif choice == 2:
        return "man"
    elif choice == 3:
        return "cheb"
    else:
        print("Invalid Input. Choosing Euclidean Distance by Default.")
        return "euc"


if __name__ == "__main__":
    n, m = map(int, input("Enter Number of Rows and Columns (rows columns): ").split())
    num_agents = int(input("Enter the Number of Agents: "))
    num_goals = int(input("Enter the Number of Goals: "))
    start_pos = []
    for i in range(num_agents):
        i, j = map(int, input(f"Enter the Starting Position (i j) for Agent {i+1}: ").split())
        start_pos.append((i, j))
    env = GridEnvironment(n, m, num_agents, num_goals, start_pos)
    
    print("Initial Starting Grid")
    env.print_grid()
    print("\n\n")
    
    csp = CSPSolver(env, (0,0))
    game = Simulation(env, csp)
    
    good_algo = ()

    for i in range(num_agents):

        
        print(f"\nChoose the Type of Algorithm you would like to run\n")
        print(f"1. BFS")
        print(f"2. DFS")
        print(f"3. A*")
        rewards = []
        max_util = -math.inf
        choice = int(input(f"\nFor Agent {i+1}: "))
        if choice == 1:
            path = game.BFS(i)
            if path:
                re = game.evaluate_path(path)
                print(f"Agent {i+1}: Found Path using BFS\n{path}\nTotal Reward Acquired: {re}\n")

                if re > max_util:
                    good_algo = ("BFS", re)
                    max_util = re
                
            else:
                print(f"Agent {i+1} Couldn't Find the Path using BFS\n")
        elif choice == 2:
            path = game.DFS(i)
            if path:
                re = (game.evaluate_path(path))
                print(f"Agent {i+1}: Found Path using DFS\n{path}\nTotal Reward Acquired: {re}\n")

                if re > max_util:
                    good_algo = ("DFS", re)
                    max_util = re
            else:
                print(f"Agent {i+1} Couldn't Find the Path using DFS\n")
        elif choice == 3:
            heuristic = choose_heuristic()
            path = game.a_star(i, heuristic)
            if path:
                re = (game.evaluate_path(path))
                print(f"Agent {i+1}: Found Path using A*\n{path}\nTotal Reward Acquired: {re}\n")
                if re > max_util:
                    good_algo = ("A*", re)
                    max_util = re
            else:
                print(f"Agent {i+1} Couldn't Find the Path using A*\n") 
        else:
            print(f"Invalid Choice. Choosing BFS For agent {i+1}")
            path = game.BFS(i)
            if path:
                re = (game.evaluate_path(path))
                if re > max_util:
                    good_algo = ("BFS", re)
                    max_util = re
                print(f"Agent {i+1}: Found Path using BFS\n{path}\nTotal Reward Acquired: {re}\n")  
            else:
                print(f"Agent {i+1} Couldn't Find the Path using BFS\n")
    
    csp_c = input(f"\n\nWould you like to get Solutions by CSP? (y/n): ").lower()
    if csp_c.startswith('y'):
        for i in range(num_agents):
            csp = CSPSolver(env, env.s_pos[i])
            csp_game = Simulation(env, csp)
            path = csp_game.solve_with_csp(env.s_pos[i])
            if path: 
                print(f"\nAgent {i+1} Path Found using CSP\n{path}")
            else:
                print(f"\nAgent {i+1} Couldn't find the path.\n")
    else:
        print(f"\nHave a Great Day!")

    print(f"Best Algorithm for Agents using {good_algo[0]} achieved utility-reward {good_algo[1]}")