from collections import deque

def bfs_solver(initial_state):
    visited = set()
    queue = deque()

    # The quese holds the current grid of the map and the path it took to get there
    queue.append((initial_state, ""))
    visited.add(hash(initial_state))

    while queue:
        state, path = queue.popleft()

        if state.is_goal():
            return path

        for move, successor in state.get_successors():
            h = hash(successor)
            if h not in visited:
                visited.add(h)
                queue.append((successor, path + move))

    return None  # Returns None if no solution is found.
