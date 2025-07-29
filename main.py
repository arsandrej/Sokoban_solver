from sokoban_state import SokobanState
from solvers.astar_solver import astar_solver
from solvers.bfs_solver import bfs_solver
from solvers.dfs_solver import dfs_solver
from level_loader import load_level
from level_loader import run_solver
from visualize import run_game


level = load_level("levels/level2.txt")
initial_state = SokobanState(level)

solution_astar = run_solver("A*", astar_solver, initial_state)
solution_bfs = run_solver("BFS", bfs_solver, initial_state)
solution_dfs = run_solver("DFS", dfs_solver, initial_state)

run_game(initial_state, solution_astar, solution_bfs, solution_dfs)

