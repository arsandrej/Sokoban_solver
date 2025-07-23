import heapq

def heuristic(state):
    total_distance = 0
    for box in state.boxes:
        min_distance = min(
            abs(box[0] - goal[0]) + abs(box[1] - goal[1]) # Manhattan distance to the closest goal
            for goal in state.goals
        )
        total_distance += min_distance
    return total_distance

def astar_solver(initial_state):
    open_list = [] #Priority queue
    heapq.heappush(open_list, (heuristic(initial_state), 0, initial_state, ""))
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
                new_g = g + 1 #Cost per move
                new_f = new_g + heuristic(successor)# f = g + h -> calculating the distance to evaluate heuristic
                heapq.heappush(open_list, (new_f, new_g, successor, path + direction))

    return None
