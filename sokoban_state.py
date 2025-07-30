from scipy.optimize import linear_sum_assignment
import numpy as np
import math
from collections import deque

DIRECTIONS = {
    'U': (0, -1),
    'D': (0, 1),
    'L': (-1, 0),
    'R': (1, 0),
}


class SokobanState:
    def __init__(self, grid, heuristic_type="manhattan"):

        self.grid = [list(row) for row in grid]
        self.height = len(self.grid)
        self.width = len(self.grid[0]) if self.grid else 0
        self.player = self.find_player()
        self.boxes = self.find_boxes()
        self.goals = self.find_goals()
        self.heuristic_type = heuristic_type
        self.dead_squares = None
        self.compute_dead_squares()
        # self.print_dead_squares()

    def print_dead_squares(self):
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                if (x, y) in self.dead_squares:
                    row += "X"
                else:
                    row += self.grid[y][x]
            print(row)

    def find_player(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == '@':
                    return (x, y)
        return None

    def find_boxes(self):
        box = []
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == "$" or self.grid[y][x] == "*":
                    box.append((x, y))
        return set(box)

    def find_goals(self):
        goal = []
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == "." or self.grid[y][x] == "*":
                    goal.append((x, y))
        return set(goal)

    def is_wall(self, x, y):
        return self.grid[y][x] == "#"

    def is_inside_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def is_goal(self):
        return self.boxes == self.goals


    def compute_dead_squares(self):
        self.dead_squares = set()

        for x in range(self.width):
            # Top edge
            if self.grid[0][x] != '#' and (x, 0) not in self.goals:
                self.dead_squares.add((x, 0))
            # Bottom edge
            if self.grid[self.height - 1][x] != '#' and (x, self.height - 1) not in self.goals:
                self.dead_squares.add((x, self.height - 1))

        for y in range(self.height):
            # Left edge
            if self.grid[y][0] != '#' and (0, y) not in self.goals:
                self.dead_squares.add((0, y))
            # Right edge
            if self.grid[y][self.width - 1] != '#' and (self.width - 1, y) not in self.goals:
                self.dead_squares.add((self.width - 1, y))

    def is_free(self, x, y):
        return (not self.is_wall(x, y)) and ((x, y) not in self.boxes) # Helper to check if cell is empty

    def is_frozen(self):
        # Initially: boxes on goals are NOT frozen
        frozen = {box: False for box in self.boxes}
        for box in self.boxes:
            if box in self.goals:
                frozen[box] = False

        changed = True
        while changed:
            changed = False

            for box in self.boxes:
                if frozen[box]:
                    continue  # Already frozen

                x, y = box
                movable = False

                for dx, dy in DIRECTIONS.values():
                    dest = (x + dx, y + dy)
                    behind = (x - dx, y - dy)

                    # Check bounds
                    if not self.is_inside_bounds(*dest) or not self.is_inside_bounds(*behind):
                        continue

                    # Destination must be free (no wall, no box)
                    if not self.is_free(*dest):
                        continue

                    # Player must stand behind box (behind cell)
                    if self.is_wall(*behind):
                        continue

                    if behind in self.boxes:
                        # Box behind must NOT be frozen for current box to be movable
                        if frozen.get(behind, True):
                            continue
                        else:
                            movable = True
                            break
                    else:
                        # Behind cell is free floor/goal for player to stand
                        movable = True
                        break

                if not movable:
                    frozen[box] = True
                    changed = True

        # If any box off goal is frozen, then freeze deadlock exists
        for box in self.boxes:
            if box not in self.goals and frozen[box]:
                return True

        return False

    def is_deadlocked(self):
        for box in self.boxes:
            if box in self.goals:
                continue  #if its on goal it cant be deadlocked
            if box in self.dead_squares:
                return True

            x, y = box
            #Check if box is in a corner -> it cant be pushed in any case scenario
            if (
                    (self.is_wall(x + 1, y) and self.is_wall(x, y + 1)) or
                    (self.is_wall(x - 1, y) and self.is_wall(x, y + 1)) or
                    (self.is_wall(x + 1, y) and self.is_wall(x, y - 1)) or
                    (self.is_wall(x - 1, y) and self.is_wall(x, y - 1))
            ):
                # print("Corner")
                return True

        #
        if self.is_frozen():
            return True

        return False #No deadlocks detected

    def clone(self):
        new_state = SokobanState([''.join(row) for row in self.grid])
        new_state.player = self.player
        new_state.boxes = self.boxes.copy()
        new_state.goals = self.goals.copy()
        new_state.dead_squares = self.dead_squares
        return new_state

    def get_successors(self):
        successors = []

        px, py = self.player

        for direction, (dx, dy) in DIRECTIONS.items():
            nx, ny = px + dx, py + dy      # Adjacent tile
            bx, by = px + 2*dx, py + 2*dy  # Beyond box tile

            if not self.is_inside_bounds(nx, ny):
                continue
            target = self.grid[ny][nx]

            # Move in an empty/goal direction
            if target in " .":
                new_state = self.clone()
                new_state.grid[py][px] = " "
                new_state.grid[ny][nx] = "@"
                new_state.player = (nx, ny)
                new_state.boxes = new_state.find_boxes()

                successors.append((direction, new_state))

            # Move in box direction
            elif target == "$":
                if not self.is_inside_bounds(bx, by):
                    continue
                beyond = self.grid[by][bx]
                if beyond in " .":
                    new_state = self.clone()
                    new_state.grid[py][px] = " "
                    new_state.grid[ny][nx] = "@"
                    new_state.grid[by][bx] = "$"
                    new_state.player = (nx, ny)
                    new_state.boxes = new_state.find_boxes()
                    if not new_state.is_deadlocked():
                        successors.append((direction, new_state))

        return successors

    def heuristic(self):
        num_boxes = len(self.boxes)
        num_goals = len(self.goals)


        cost_matrix = np.zeros((num_boxes, num_goals)) # Matrix of of cost (boxes x goals)

        for i, box in enumerate(self.boxes):
            for j, goal in enumerate(self.goals):
                if self.heuristic_type == "manhattan":
                    dist = abs(box[0] - goal[0]) + abs(box[1] - goal[1])
                elif self.heuristic_type == "euclidean":
                    dist = math.hypot(box[0] - goal[0], box[1] - goal[1])
                else:
                    raise ValueError(f"Unknown heuristic: {self.heuristic_type}")
                cost_matrix[i][j] = dist  # Add values to matrix

        row_ind, col_ind = linear_sum_assignment(cost_matrix) # Find the optimal assignment of boxes to unique goals using the Hungarian algorithm

        distances = cost_matrix[row_ind, col_ind]
        total_distance = distances.sum()


        max_distance = distances.max() # Farthest box to goal distance
        total_distance += 0.2 * max_distance  # Weight far boxes more


        player_box_distance = min(
            abs(self.player[0] - box[0]) + abs(self.player[1] - box[1]) #Add the distance from player to closest box to encourage movement towards boxes
            for box in self.boxes
        )
        total_distance += 0.5 * player_box_distance  # Weighted influence
        #Using higher weight seems to slightly improve in exploring the solution

        return total_distance

    def __lt__(self, other):
        return (self.player, self.boxes) < (other.player, other.boxes)

    def __hash__(self):
        return hash((self.player, frozenset(self.boxes)))

    def __eq__(self, other):
        return isinstance(other, SokobanState) and \
               self.player == other.player and \
               self.boxes == other.boxes

    def __str__(self):
        display = [row.copy() for row in self.grid]

        for x, y in self.goals:
            if (x, y) in self.boxes:
                display[y][x] = '*'
            elif (x, y) == self.player:
                display[y][x] = '+'
            else:
                display[y][x] = '.'

        for x, y in self.boxes:
            if (x, y) not in self.goals:
                display[y][x] = '$'

        px, py = self.player
        if (px, py) not in self.goals:
            display[py][px] = '@'

        return '\n'.join(''.join(row) for row in display)
