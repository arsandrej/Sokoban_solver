from sokoban_state import SokobanState
from solvers.astar_solver import astar_solver
from solvers.bfs_solver import bfs_solver
from solvers.dfs_solver import dfs_solver
from level_loader import load_level
from level_loader import run_solver
from visualize import run_game
from menu import run_menu
from solo_game import run_solo_game

level = load_level("levels/level8.txt")

choice = run_menu()
if choice is None:
    print("User quit the menu")
    exit(0)


initial_state = SokobanState(level)
initial_state.print_dead_squares()

if choice == "solo":
    run_solo_game(initial_state, astar_solver)
elif choice == "ai":
    astar_solution, astar_stats = run_solver("A*", astar_solver, initial_state)
    bfs_solution, bfs_stats = run_solver("BFS", bfs_solver, initial_state)
    dfs_solution, dfs_stats = run_solver("DFS", dfs_solver, initial_state)

    run_game(initial_state, astar_solution, astar_stats, bfs_solution, bfs_stats, dfs_solution, dfs_stats)


