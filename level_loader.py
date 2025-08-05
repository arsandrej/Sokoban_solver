import pygame
import os

def load_level(file_path):
    with open(file_path) as f:
        lines = [line.rstrip('\n') for line in f]
    return lines

def load_images():
    base_path = "images"
    return {
        "wall": pygame.image.load(os.path.join(base_path, "wall.png")),
        "goal": pygame.image.load(os.path.join(base_path, "goal.png")),
        "box": pygame.image.load(os.path.join(base_path, "box.png")),
        "box_on_goal": pygame.image.load(os.path.join(base_path, "box_on_goal.png")),
        "player": pygame.image.load(os.path.join(base_path, "player.png")),
        "floor": pygame.image.load(os.path.join(base_path, "floor.png")),
    }


def apply_solution(state, solution):
    current_state = state
    for move in solution:
        for direction, new_state in current_state.get_successors():
            if direction == move:
                current_state = new_state
                break
    return current_state

def run_solver(name, solver_func, initial_state):
    print(f"--- {name} ---")
    path, stats = solver_func(initial_state)
    if path:
        print(f"{name} Solution: {path}")
        final_state = apply_solution(initial_state, path)
        print(f"Final {name} State:")
        print(final_state)
        print(f"{name} Stats: Time = {stats['execution_time']:.4f}s, Explored Nodes = {stats['explored_nodes']}, Steps: {len(path)}")

    else:
        print(f"No {name} solution found.")
        print(f"{name} Stats: Time = {stats['execution_time']:.4f}s, Explored Nodes = {stats['explored_nodes']}")

    print()
    return path, stats
