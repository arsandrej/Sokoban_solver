import heapq

def astar_solver(initial_state):
    open_list = []
    heapq.heappush(open_list, (initial_state.heuristic(), 0, initial_state, ""))
    visited = set()

    while open_list:
        f, g, current_state, path = heapq.heappop(open_list)

        if current_state in visited:
            continue
        visited.add(current_state)

        if current_state.is_goal():
            return path

        for direction, successor in current_state.get_successors():
            if successor not in visited:
                new_g = g + 1
                new_f = new_g + successor.heuristic()  # Use class method
                heapq.heappush(open_list, (new_f, new_g, successor, path + direction))

    return None
