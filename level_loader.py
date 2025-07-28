def load_level(file_path):
    with open(file_path) as f:
        lines = [line.rstrip('\n') for line in f]
    return lines

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
    path = solver_func(initial_state)
    if path:
        print(f"{name} Solution: {path}")
        final_state = apply_solution(initial_state, path)
        print(f"Final {name} State:")
        print(final_state)
    else:
        print(f"No {name} solution found.")
    print()
    return path
