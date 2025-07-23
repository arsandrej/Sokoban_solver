from sokoban_state import SokobanState
from solvers.astar_solver import astar_solver
from solvers.bfs_solver import bfs_solver
from solvers.dfs_solver import dfs_solver
from level_loader import load_level


level = load_level("levels/level4.txt")

initial_state = SokobanState(level)

solution = astar_solver(initial_state)
if solution:
    print("A* Solution:", solution)
else:
    print("No A* solution found.")

solutionbfs = bfs_solver(initial_state)
if solutionbfs:
    print("BFS Solution:", solutionbfs)
else:
    print("No BFS solution found.")

solutiondfs = dfs_solver(initial_state)
if solutiondfs:
    print("DFS Solution:", solutiondfs)
else:
    print("No DFS solution found.")
