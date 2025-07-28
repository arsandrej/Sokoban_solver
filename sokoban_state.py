DIRECTIONS = {
    'U': (0, -1),
    'D': (0, 1),
    'L': (-1, 0),
    'R': (1, 0),
}

class SokobanState:
    def __init__(self, grid):

        self.grid = [list(row) for row in grid]
        self.height = len(self.grid)
        self.width = len(self.grid[0]) if self.grid else 0
        self.player = self.find_player()
        self.boxes = self.find_boxes()
        self.goals = self.find_goals()

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
                if self.grid[y][x] == "$":
                    box.append((x, y))
        return set(box)

    def find_goals(self):
        goal = []
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == ".":
                    goal.append((x, y))
        return set(goal)

    def is_wall(self, x, y):
        return self.grid[y][x] == "#"

    def is_inside_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def is_goal(self):
        return self.boxes == self.goals

    def is_frozen(self, x, y):

        def is_blocked(x, y, axis):

            if axis == 'horizontal':
                directions = [(-1, 0), (1, 0)]
            else:
                directions = [(0, -1), (0, 1)]

            visited = set()
            queue = [(x, y)]

            while queue:
                bx, by = queue.pop()
                visited.add((bx, by))

                for dx, dy in directions:
                    nx, ny = bx + dx, by + dy

                    if self.is_wall(nx, ny):
                        continue

                    if (nx, ny) in self.boxes:
                        if (nx, ny) not in visited:
                            queue.append((nx, ny))
                            break  # Need to investigate this box before deciding anything
                    else:
                        #Box not blocked since it can move
                        return False

            return True  #All paths are blocked

        blocked_horizontally = is_blocked(x, y, 'horizontal')
        blocked_vertically = is_blocked(x, y, 'vertical')

        if blocked_horizontally and blocked_vertically:
            return (x, y) not in self.goals #Check if its maybe on goal

        return False

    def is_deadlocked(self):
        for box in self.boxes:
            if box in self.goals:
                continue  #if its on goal it cant be deadlocked

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
            if self.is_frozen(x, y):
                return True

        return False #No deadlocks detected

    def clone(self):
        new_state = SokobanState([''.join(row) for row in self.grid])
        new_state.player = self.player
        new_state.boxes = self.boxes.copy()
        new_state.goals = self.goals.copy()
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
                if not new_state.is_deadlocked():
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
        # Sum of Manhattan distances from boxes to their closest goals
        total = 0
        for box in self.boxes:
            total += min(abs(box[0] - goal[0]) + abs(box[1] - goal[1]) for goal in self.goals)
        return total

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
