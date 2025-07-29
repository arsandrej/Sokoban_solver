import heapq
import time

def astar_solver(initial_state):
    start_time = time.time()
    explored_nodes = 0
    open_list = []
    heapq.heappush(open_list, (initial_state.heuristic(), 0, initial_state, ""))
    visited = set()

    while open_list:
        f, g, current_state, path = heapq.heappop(open_list)

        if current_state in visited:
            continue
        visited.add(current_state)
        explored_nodes += 1

        if current_state.is_goal():
            end_time = time.time()
            return path,  {
                "execution_time": end_time - start_time,
                "explored_nodes": explored_nodes
            }

        for direction, successor in current_state.get_successors():
            if successor not in visited:
                new_g = g + 1
                new_f = new_g + successor.heuristic()
                heapq.heappush(open_list, (new_f, new_g, successor, path + direction))

    return None, {
        "execution_time": time.time() - start_time, #Even if no solution is found return the time it took to compute
        "explored_nodes": explored_nodes
    }
