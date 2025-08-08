from sokoban_state import SokobanState
from solvers.astar_solver import astar_solver
from solvers.bfs_solver import bfs_solver
from solvers.dfs_solver import dfs_solver
from level_loader import load_level
from level_loader import run_solver
from visualize import run_game
from menu import run_menu
from solo_game import run_solo_game

level = load_level("levels/level12.txt")

choice, path = run_menu()
if choice is None:
    print("User quit the menu")
    exit(0)
if path is not None:
    level = load_level(path)

initial_state = SokobanState(level)
initial_state.print_dead_squares()

while True:
    if choice == "solo":
        result = run_solo_game(initial_state, astar_solver)
        if result is None:
            break
        choice, path = run_menu()
        if path is not None:
            level = load_level(path)
        initial_state = SokobanState(level)

    elif choice == "ai":
        astar_solution, astar_stats = run_solver("A*", astar_solver, initial_state)
        bfs_solution, bfs_stats = run_solver("BFS", bfs_solver, initial_state)
        dfs_solution, dfs_stats = run_solver("DFS", dfs_solver, initial_state)
        result = run_game(initial_state, astar_solution, astar_stats, bfs_solution, bfs_stats, dfs_solution, dfs_stats)
        if result is None:
            break
        choice, path = run_menu()
        if path is not None:
            level = load_level(path)
        initial_state = SokobanState(level)


    elif choice == "settings":
        choice, path = run_menu()
        if path is not None:
            level = load_level(path)
        initial_state = SokobanState(level)
