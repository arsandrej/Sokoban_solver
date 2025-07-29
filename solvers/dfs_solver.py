import time

def dfs_solver(initial_state, max_depth=1000):
    start_time = time.time()
    explored_nodes = 0
    visited = set()
    stack = [(initial_state, "")]

    while stack:
        state, path = stack.pop()

        if state.is_goal():
            end_time = time.time()
            return path, {
                "execution_time": end_time - start_time,
                "explored_nodes": explored_nodes,
            }

        if len(path) > max_depth:
            continue  #no infinite search

        state_hash = hash(state)
        if state_hash in visited:
            continue

        visited.add(state_hash)
        explored_nodes += 1

        for move, successor in reversed(state.get_successors()):
            stack.append((successor, path + move))

    return None, {
        "execution_time": time.time() - start_time,
        "explored_nodes": explored_nodes
    }
