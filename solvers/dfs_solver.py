def dfs_solver(initial_state, max_depth=1000):
    visited = set()
    stack = [(initial_state, "")]

    while stack:
        state, path = stack.pop()

        if state.is_goal():
            return path

        if len(path) > max_depth:
            continue  #no infinite search

        if hash(state) in visited:
            continue

        visited.add(hash(state))

        for move, successor in reversed(state.get_successors()):
            stack.append((successor, path + move))

    return None
