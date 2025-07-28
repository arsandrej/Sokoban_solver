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