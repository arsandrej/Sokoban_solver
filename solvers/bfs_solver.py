from collections import deque
import time

def bfs_solver(initial_state):
    start_time = time.time()
    explored_nodes = 0
    visited = set()
    queue = deque()

    # The quese holds the current grid of the map and the path it took to get there
    queue.append((initial_state, ""))
    visited.add(hash(initial_state))

    while queue:
        state, path = queue.popleft()
        explored_nodes += 1

        if state.is_goal():
            end_time = time.time()
            return path, {
                "execution_time": end_time - start_time,
                "explored_nodes": explored_nodes
            }

        for move, successor in state.get_successors():
            h = hash(successor)
            if h not in visited:
                visited.add(h)
                queue.append((successor, path + move))

    return None, {
        "execution_time": time.time() - start_time,
        "explored_nodes": explored_nodes
    }
