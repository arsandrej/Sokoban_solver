from sokoban_state import SokobanState
from solvers.astar_solver import astar_solver
from solvers.bfs_solver import bfs_solver
from solvers.dfs_solver import dfs_solver
from level_loader import load_level
from level_loader import apply_solution
from visualize import run_game


level = load_level("levels/level2.txt")
initial_state = SokobanState(level)

solution = astar_solver(initial_state)
if solution:
    print("A* Solution:", solution)
    final_state = apply_solution(initial_state, solution)
    print("Final A* State:")
    print(final_state)
else:
    print("No A* solution found.")

print()

solutionbfs = bfs_solver(initial_state)
if solutionbfs:
    print("BFS Solution:", solutionbfs)
    final_state_bfs = apply_solution(initial_state, solutionbfs)
    print("Final BFS State:")
    print(final_state_bfs)
else:
    print("No BFS solution found.")

print()

solutiondfs = dfs_solver(initial_state)
if solutiondfs:
    print("DFS Solution:", solutiondfs)
    final_state_dfs = apply_solution(initial_state, solutiondfs)
    print("Final DFS State:")
    print(final_state_dfs)
else:
    print("No DFS solution found.")

solution_astar = astar_solver(initial_state)
solution_bfs = bfs_solver(initial_state)
solution_dfs = dfs_solver(initial_state)

run_game(initial_state, solution_astar, solution_bfs, solution_dfs)

