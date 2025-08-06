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
        self.empty_spaces = self.find_empty_spaces()
        self.heuristic_type = heuristic_type
        self.dead_squares = ()
        self.compute_dead_squares()

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

    def find_empty_spaces(self):
        spaces = []
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == " ":
                    spaces.append((x, y))
        return set(spaces)

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
        for x,y in self.empty_spaces:
            if(x, y) in self.goals:
                continue

            if (x, y) in self.boxes:
                continue

            if self.is_corner(x,y):
                self.dead_squares.add((x,y))

            if self.is_tunnel_deadlock(x, y):
                self.dead_squares.add((x,y))

    def is_tunnel_deadlock(self, x, y):
        # Count available directions
        exits = 0
        for dx, dy in DIRECTIONS.values():
            if not self.is_wall(x + dx, y + dy):
                exits += 1

        # Single-exit tunnel with no goal in line
        if exits == 1:
            # Find the open direction
            for dx, dy in DIRECTIONS.values():
                if not self.is_wall(x + dx, y + dy):
                    # Check if there's a goal in this direction
                    nx, ny = x + dx, y + dy
                    while self.is_inside_bounds(nx, ny) and not self.is_wall(nx, ny):
                        if (nx, ny) in self.goals:
                            return False
                        nx += dx
                        ny += dy
                    return True
        return False

    def is_corner(self, x, y):
        if (
                (self.is_wall(x + 1, y) and self.is_wall(x, y + 1)) or
                (self.is_wall(x - 1, y) and self.is_wall(x, y + 1)) or
                (self.is_wall(x + 1, y) and self.is_wall(x, y - 1)) or
                (self.is_wall(x - 1, y) and self.is_wall(x, y - 1))
        ):
            # print("Corner")
            return True
        return False

    def freeze_deadlock(self):
        for x, y in self.boxes:
            # Skip if on goal
            if (x, y) in self.goals:
                continue

            # Horizontal pair (x, y) and (x+1, y)
            if (x + 1, y) in self.boxes and (x + 1, y) not in self.goals:
                # Check if both boxes are against top or bottom wall
                top_wall = self.is_wall(x, y - 1) and self.is_wall(x + 1, y - 1)
                bottom_wall = self.is_wall(x, y + 1) and self.is_wall(x + 1, y + 1)

                if top_wall or bottom_wall:
                    return True

            # Vertical pair (x, y) and (x, y+1)
            if (x, y + 1) in self.boxes and (x, y + 1) not in self.goals:
                # Check if both boxes are against left or right wall
                left_wall = self.is_wall(x - 1, y) and self.is_wall(x - 1, y + 1)
                right_wall = self.is_wall(x + 1, y) and self.is_wall(x + 1, y + 1)

                if left_wall or right_wall:
                    return True

        return False

    def is_deadlocked(self):
        for box in self.boxes:
            if box in self.dead_squares:
                return True
        if self.freeze_deadlock():
            return True

        return False

    def clone(self):
        new_state = SokobanState([''.join(row) for row in self.grid])
        new_state.player = self.player
        new_state.boxes = self.boxes.copy()
        new_state.goals = self.goals.copy()
        new_state.dead_squares = self.dead_squares
        return new_state

    def get_successors(self, skip_deadlock_check=False):
        successors = []

        px, py = self.player

        for direction, (dx, dy) in DIRECTIONS.items():
            nx, ny = px + dx, py + dy # Adjacent tile
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
                    if skip_deadlock_check or not new_state.is_deadlocked():
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
        # Use sorted boxes for invariant state representation
        return hash((self.player, tuple(sorted(self.boxes))))

    def __eq__(self, other):
        return (self.player == other.player and
                sorted(self.boxes) == sorted(other.boxes))

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
